# -*- coding: utf-8 -*-
"""
core/errors/__init__.py 错误基类单元测试（ErrorDetails / Error）。

覆盖：
  - ErrorDetails：默认值 / 自定义值 / to_dict 序列化（含 None → "None" 边界）
  - Error.__init__：context 多种形态（dict 占位符 / 缺键回退模板 / kwargs 合并 / 字符串 / 空值）
  - data / extra / error_details 的传递与自动构建、set_details 覆盖
  - __str__ / __repr__
  - log()：全部 level 映射 + 无效 level 兜底重置

运行方式（复用根目录 hello.py 加载 Django 环境，已实际验证）：
  bkmonitor/.venv/bin/python -m pytest -p no:django \
      .module-experts/issue专家/test/test_core_errors.py -q
  # → 全部 passed（无需角色切换，core.errors 无 kernel_api 依赖）
"""

import logging
import os
import sys
from pathlib import Path

import pytest

# 保证能 import 根目录的 hello.py（加载 Django 环境：sys.path + .env + django.setup）
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import hello  # noqa: F401  # noqa: E402 — Django 环境初始化（必须在所有项目 import 之前）


# ── ErrorDetails ──────────────────────────────────────────────────────────────
class TestErrorDetails:
    def test_default_values(self):
        from core.errors import ErrorDetails

        d = ErrorDetails()
        assert d.exc_type is None
        assert d.exc_code is None
        assert d.overview is None
        assert d.detail is None
        assert d.popup_message == "warning"

    def test_custom_values(self):
        from core.errors import ErrorDetails

        d = ErrorDetails(exc_type="TypeA", exc_code=3301001, overview="overview", detail={"k": 1}, popup_message="error")
        assert d.exc_type == "TypeA"
        assert d.exc_code == 3301001
        assert d.overview == "overview"
        assert d.detail == {"k": 1}
        assert d.popup_message == "error"

    def test_to_dict_mapping(self):
        from core.errors import ErrorDetails

        d = ErrorDetails(exc_type="TypeA", exc_code=3301001, overview="overview", detail={"k": 1}, popup_message="error")
        assert d.to_dict() == {
            "type": "TypeA",
            "code": 3301001,
            "overview": "overview",
            "detail": "{'k': 1}",  # detail 经 str() 序列化
            "popup_message": "error",
        }

    def test_to_dict_none_serializes_to_str_none(self):
        # 边界：overview / detail 为 None 时 str() 输出 "None"（非 None 值）
        from core.errors import ErrorDetails

        d = ErrorDetails().to_dict()
        assert d["overview"] == "None"
        assert d["detail"] == "None"
        assert d["type"] is None
        assert d["code"] is None


# ── Error 类属性默认值 ────────────────────────────────────────────────────────
class TestErrorDefaults:
    def test_class_defaults(self):
        from core.errors import Error

        assert Error.status_code == 500
        assert Error.code == 0
        assert Error.level == logging.ERROR
        assert Error.popup_message == "warning"
        assert Error.error_details is None
        assert issubclass(Error, Exception)


# ── Error.__init__ context 形态 ──────────────────────────────────────────────
class TestErrorInit:
    def test_context_none_uses_template(self):
        from core.errors import Error

        err = Error()
        assert str(err.message) == "系统异常，请联系管理员"  # 默认模板无占位符 → 原样
        assert err.data is None
        assert err.extra == {}

    def test_context_non_empty_string_becomes_message(self):
        from core.errors import Error

        err = Error("custom message")
        assert err.message == "custom message"

    def test_context_empty_string_falls_back_to_template(self):
        # 边界：空字符串为 falsy → 走模板路径
        from core.errors import Error

        err = Error("")
        assert str(err.message) == "系统异常，请联系管理员"

    def test_context_dict_formats_template(self):
        from core.errors import Error

        class TplError(Error):
            message_tpl = "name={name}, code={code}"

        err = TplError(context={"name": "x", "code": 1})
        assert err.message == "name=x, code=1"

    def test_context_dict_missing_key_falls_back_to_template(self):
        # 边界：占位符缺键 → format 抛 KeyError → 回退模板原文（不二次抛异常）
        from core.errors import Error

        class TplError(Error):
            message_tpl = "name={name}"

        err = TplError(context={})
        assert str(err.message) == "name={name}"

    def test_kwargs_merged_into_context(self):
        from core.errors import Error

        class TplError(Error):
            message_tpl = "name={name}"

        err = TplError(name="via_kwarg")
        assert err.message == "name=via_kwarg"

    def test_data_and_extra_passed_through(self):
        from core.errors import Error

        err = Error("m", data={"k": 1}, extra={"x": 2})
        assert err.data == {"k": 1}
        assert err.extra == {"x": 2}

    def test_extra_none_becomes_empty_dict(self):
        from core.errors import Error

        err = Error("m")
        assert err.extra == {}


# ── error_details 构建与覆盖 ──────────────────────────────────────────────────
class TestErrorDetailsBuild:
    def test_error_details_auto_built_on_init(self):
        from core.errors import Error

        err = Error("m")
        assert isinstance(err.error_details, dict)
        assert err.error_details["type"] == "Error"
        assert err.error_details["code"] == 0
        assert err.error_details["overview"] == "m"
        assert err.error_details["detail"] == "None"  # data=None → str(None)
        assert err.error_details["popup_message"] == "warning"

    def test_set_details_override(self):
        from core.errors import Error

        err = Error("m")
        err.set_details(exc_type="Custom", exc_code=999, overview="o", detail="d", popup_message="error")
        assert err.error_details == {
            "type": "Custom",
            "code": 999,
            "overview": "o",
            "detail": "d",
            "popup_message": "error",
        }


# ── __str__ / __repr__ ────────────────────────────────────────────────────────
class TestErrorStrRepr:
    def test_str(self):
        from core.errors import Error

        assert str(Error("hello")) == "hello"

    def test_repr(self):
        from core.errors import Error

        assert repr(Error("hello")) == "hello"


# ── log() ─────────────────────────────────────────────────────────────────────
class TestErrorLog:
    @staticmethod
    def _patch_logger(monkeypatch):
        from unittest.mock import MagicMock

        import core.errors

        mock = MagicMock()
        monkeypatch.setattr(core.errors, "logger", mock)
        return mock

    @pytest.mark.parametrize(
        "level,method",
        [
            (logging.ERROR, "error"),
            (logging.CRITICAL, "critical"),
            (logging.FATAL, "critical"),  # FATAL 与 CRITICAL 同值 → 映射 critical
            (logging.WARNING, "warning"),
            (logging.DEBUG, "debug"),
            ("EXCEPTION", "exception"),
            (logging.INFO, "info"),
            (logging.NOTSET, "info"),  # NOTSET 映射 info
        ],
    )
    def test_log_level_mapping(self, monkeypatch, level, method):
        from core.errors import Error

        mock = self._patch_logger(monkeypatch)
        cls = type("E", (Error,), {"level": level})
        err = cls("m")
        err.log()
        getattr(mock, method).assert_called_once_with(err)

    def test_log_invalid_level_resets_to_error(self, monkeypatch):
        from core.errors import Error

        mock = self._patch_logger(monkeypatch)
        cls = type("E", (Error,), {"level": 99999})
        err = cls("m")
        err.log()
        # 无效 level → 重置为 ERROR，并先打一条告警日志再打错误本身
        assert err.level == logging.ERROR
        calls = mock.error.call_args_list
        assert len(calls) == 2
        assert "is not exists" in str(calls[0])
        assert calls[1].args == (err,)
