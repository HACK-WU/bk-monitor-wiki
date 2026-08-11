# -*- coding: utf-8 -*-
"""
Issue 重命名专有状态码（REQ-20260803-001）单元测试。

覆盖链路：
  1. core/errors/issue.py —— 专有错误类 IssueRenameConflictError（code=3327001 / HTTP 409）
  2. kernel_api.views.v4.issue.RenameResource —— 重名时抛专有错误（需 api 角色）
  3. fta_web.issue.resources.RenameIssueResource —— 识别上游 3327001 转中文提示 + 透传 data
  4. kernel_api.exceptions.api_exception_handler —— 渲染契约（HTTP 200 + body code + data 白名单，需 api 角色）

运行方式（复用根目录 hello.py 加载 Django 环境，无需手动配置环境变量，已实际验证）：

  # ── web 角色（默认）：覆盖错误类 + web 端用例，kernel_api 用例自动 skip ──
  bkmonitor/.venv/bin/python -m pytest -p no:django \
      .module-experts/issue专家/test/test_issue_rename_conflict.py -q
  # → 7 passed, 2 skipped（仅 kernel_api RenameResource 用例自动 skip；
  #   api_exception_handler 渲染用例依赖轻量，web 角色下同样可执行）

  # ── api 角色：额外覆盖 kernel_api 用例（import 链需要 monitor_web + alarm_backends
  #    同时注册，见 .module-experts/issue专家/test/known-failures.md 角色选择注意）──
  BK_ISSUE_TEST_ROLE=api BKAPP_DEPLOY_PLATFORM=community \
      bkmonitor/.venv/bin/python -m pytest -p no:django \
      .module-experts/issue专家/test/test_issue_rename_conflict.py -q
  # → 9 passed

说明：
  1. 必须从 workspace 根目录运行：hello.py 在根目录，只有 cwd=根目录时 import hello
     才能加载 Django 环境（sys.path + .env + django.setup()）。
  2. -p no:django 禁用 pytest-django：从根目录运行时它找不到 manage.py/settings 会报
     ImportError: No module named 'settings'；本测试已通过 import hello 手动完成
     django.setup()，无需 pytest-django 再初始化。
  3. BK_ISSUE_TEST_ROLE=api 在 import hello 之前把 DJANGO_CONF_MODULE 切为 api 角色
     （hello.py 的 load_dotenv 默认不覆盖已存在变量，故切换生效）。
  4. 无需 --override-ini "filterwarnings="：从根目录运行时不加载 bkmonitor/pyproject.toml
     的 pytest 配置（其 filterwarnings 引用了 Django 4.2 不存在的 RemovedInDjango51Warning）。
     若从 bkmonitor/ 目录运行则需追加该参数。
"""

import os
import sys
from pathlib import Path

import pytest

# 保证能 import 根目录的 hello.py（加载 Django 环境：sys.path + .env + django.setup）
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# 允许通过环境变量显式切换角色（hello.py 的 load_dotenv 默认不覆盖已存在变量）
if os.environ.get("BK_ISSUE_TEST_ROLE") == "api":
    os.environ["DJANGO_CONF_MODULE"] = "conf.api.development.community"

import hello  # noqa: F401  # noqa: E402 — Django 环境初始化（必须在所有项目 import 之前）


# ── 1. 专有错误类 ────────────────────────────────────────────────────────────
class TestIssueRenameConflictError:
    def test_code_and_status_code(self):
        from core.errors.issue import IssueRenameConflictError

        assert IssueRenameConflictError.code == 3327001
        assert IssueRenameConflictError.status_code == 409

    def test_message_and_data(self):
        from core.errors.issue import IssueRenameConflictError

        err = IssueRenameConflictError(message="已存在同名 Issue，请更换名称", data={"name": "dup"})
        assert err.message == "已存在同名 Issue，请更换名称"
        assert err.data == {"name": "dup"}
        # error_details 携带业务错误码，前端据此识别
        assert err.error_details["code"] == 3327001
        assert err.error_details["type"] == "IssueRenameConflictError"


# ── 2. kernel_api RenameResource（需 api 角色）───────────────────────────────
class TestKernelApiRenameResource:
    def _import(self):
        try:
            from kernel_api.views.v4.issue import RenameResource
            from bkmonitor.documents.issue import IssueNameDuplicatedError
        except Exception as exc:  # pragma: no cover — 依赖角色环境，失败时 skip
            pytest.skip(f"kernel_api.views.v4.issue import 失败（需 api 角色）: {exc}")
        return RenameResource, IssueNameDuplicatedError

    def test_duplicate_name_raises_conflict_error(self, monkeypatch):
        from unittest.mock import MagicMock

        RenameResource, IssueNameDuplicatedError = self._import()

        issue = MagicMock()
        issue.rename.side_effect = IssueNameDuplicatedError(
            "Issue name already exists, bk_biz_id=2, name=dup"
        )
        monkeypatch.setattr(
            "kernel_api.views.v4.issue.IssueDocument.get_issue_or_raise", lambda *a, **k: issue
        )

        from core.errors.issue import IssueRenameConflictError

        with pytest.raises(IssueRenameConflictError) as excinfo:
            RenameResource().perform_request(
                {"issue_id": "1716000000abcdef01", "bk_biz_id": 2, "new_name": "dup", "operator": "alice"}
            )
        err = excinfo.value
        assert err.code == 3327001
        assert err.data == {"name": "dup"}
        assert "Issue name already exists" in err.message

    def test_rename_success_returns_payload(self, monkeypatch):
        from unittest.mock import MagicMock

        RenameResource, _ = self._import()

        issue = MagicMock()
        issue.bk_biz_id = 2
        issue.id = "1716000000abcdef01"
        issue.status = "UNRESOLVED"
        issue.name = "new name"
        issue.update_time = 1716000000
        issue.rename.return_value = [("NAME_CHANGE", "old", "new name", "alice", None)]
        monkeypatch.setattr(
            "kernel_api.views.v4.issue.IssueDocument.get_issue_or_raise", lambda *a, **k: issue
        )

        ret = RenameResource().perform_request(
            {"issue_id": "1716000000abcdef01", "bk_biz_id": 2, "new_name": "new name", "operator": "alice"}
        )
        assert ret["name"] == "new name"
        assert ret["activities"] == [("NAME_CHANGE", "old", "new name", "alice", None)]


# ── 4. api_exception_handler 渲染契约（需 api 角色）─────────────────────────
class TestApiExceptionHandlerRendering:
    """锁定链路核心契约：api_exception_handler 将 IssueRenameConflictError 渲染为
    HTTP 200 + body code=3327001，且 data 白名单仅透传 error_code/next_actions。

    该契约是 web 网关走 body 检查分支（而非 HTTPError 分支）识别 code 的命脉——
    若 api_exception_handler 将来返回 409（如给 Response 加 status 参数），web 端
    APIResource 将落入 raise_for_status → HTTPError 分支，e.data 变字符串，识别静默失败。
    """

    @staticmethod
    def _handler():
        try:
            from kernel_api.exceptions import api_exception_handler
        except Exception as exc:  # pragma: no cover — 依赖角色环境，失败时 skip
            pytest.skip(f"kernel_api.exceptions import 失败（需 api 角色）: {exc}")
        return api_exception_handler

    def test_renders_http_200_with_biz_code(self):
        from core.errors.issue import IssueRenameConflictError

        handler = self._handler()
        err = IssueRenameConflictError(
            message="Issue name already exists, bk_biz_id=2, name=dup", data={"name": "dup"}
        )
        resp = handler(err, context={})

        # 关键契约：api role 返回 HTTP 200（非 409），web 网关才走 body 检查分支识别 code
        assert resp.status_code == 200
        body = resp.data
        assert body["result"] is False
        assert body["code"] == 3327001
        assert "Issue name already exists" in body["message"]

    def test_data_whitelist_filters_name(self):
        from core.errors.issue import IssueRenameConflictError

        handler = self._handler()
        err = IssueRenameConflictError(
            message="Issue name already exists, bk_biz_id=2, name=dup", data={"name": "dup"}
        )
        body = handler(err, context={}).data

        # data 白名单仅透传 error_code/next_actions：name 被拦截 → data 恒为 {}
        assert body["data"] == {}


# ── 3. web RenameIssueResource（web / api 角色均可）──────────────────────────
class TestWebRenameIssueResource:
    @staticmethod
    def _conflict_body() -> dict:
        # 模拟 api role 经 api_exception_handler 渲染后的真实响应体（见 kernel_api/exceptions.py）：
        # - data 白名单仅透传 error_code/next_actions，name 被拦截不透出 → data 恒为 {}
        # - failed() 未传 error_name → name 为 None
        return {
            "result": False,
            "code": 3327001,
            "name": None,
            "message": "Issue name already exists, bk_biz_id=2, name=dup",
            "data": {},
            "error_details": {"type": "IssueRenameConflictError", "code": 3327001},
        }

    def test_conflict_code_translates_to_chinese_error(self, monkeypatch):
        from core.errors.api import BKAPIError
        from core.errors.issue import IssueRenameConflictError
        from fta_web.issue.resources import RenameIssueResource

        def fake_rename(**kwargs):
            raise BKAPIError(system_name="issue", url="/app/issue/rename/", result=self._conflict_body())

        monkeypatch.setattr("fta_web.issue.resources.api.issue.rename", fake_rename)

        with pytest.raises(IssueRenameConflictError) as excinfo:
            RenameIssueResource().perform_request({"bk_biz_id": 2, "issue_id": "x", "new_name": "dup"})

        err = excinfo.value
        assert err.code == 3327001
        assert err.status_code == 409
        assert err.message == "已存在同名 Issue，请更换名称"
        # 真实链路中 api_exception_handler 的 data 白名单会拦截 name，web 端透传 data 恒为 {}
        assert err.data == {}

    def test_non_conflict_code_is_passed_through(self, monkeypatch):
        from core.errors.api import BKAPIError
        from fta_web.issue.resources import RenameIssueResource

        upstream_err = BKAPIError(
            system_name="issue",
            url="/app/issue/rename/",
            result={"result": False, "code": 3301001, "message": "some other api error", "data": None},
        )

        def fake_rename(**kwargs):
            raise upstream_err

        monkeypatch.setattr("fta_web.issue.resources.api.issue.rename", fake_rename)

        with pytest.raises(BKAPIError) as excinfo:
            RenameIssueResource().perform_request({"bk_biz_id": 2, "issue_id": "x", "new_name": "dup"})
        # 非重名错误原样抛出（同一实例）
        assert excinfo.value is upstream_err

    def test_serializer_rejects_empty_name(self):
        from fta_web.issue.resources import RenameIssueResource

        s = RenameIssueResource.RequestSerializer(
            data={"bk_biz_id": 2, "issue_id": "x", "new_name": "  "}
        )
        assert not s.is_valid()
        assert "new_name" in s.errors
