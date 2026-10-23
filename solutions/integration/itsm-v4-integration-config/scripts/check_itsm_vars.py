"""
排查监控平台对接 ITSM V4 的环境变量配置。

用法（在监控平台 Python 容器内，工作目录为 bkmonitor/）：

    python manage.py shell < check_itsm_vars.py

或在容器外手动指定角色：

    DJANGO_CONF_MODULE=conf.web.development.community \
        python manage.py shell < check_itsm_vars.py
"""

from django.conf import settings
import os

APP_CODE = getattr(settings, "APP_CODE", None)
print("APP_CODE =", APP_CODE)
print("-" * 72)

KEYS = ("BK_ITSM_V4_SYSTEM_ID", "BK_ITSM_V4_API_URL", "BK_ITSM_V4_HOST")

for key in KEYS:
    effective = getattr(settings, key, "<settings 中未定义>")
    env_val = os.getenv(key)
    override = os.getenv("BKAPP_SETTINGS_" + key)

    print(key)
    print("  生效值     :", repr(effective))
    print("  环境变量   :", repr(env_val), "" if env_val is not None else "  <- 未设置，走代码默认值")
    print("  BKAPP 覆盖 :", repr(override), "" if override is None else "  <- 已覆盖")
    print()

# ---- 结论判定 ----
sid = getattr(settings, "BK_ITSM_V4_SYSTEM_ID", None)
host = getattr(settings, "BK_ITSM_V4_HOST", None)

print("=" * 72)
if sid == APP_CODE:
    print("[问题A] BK_ITSM_V4_SYSTEM_ID 等于 APP_CODE，极可能未配置而走了默认回退")
    print("        现象：处理套餐服务名称下拉显示「暂无选项」，接口报「系统不存在」")
    print("        解法：python manage.py create_itsm_v4_system --name <名称> --code %s" % sid)
else:
    print("[OK] BK_ITSM_V4_SYSTEM_ID 为显式配置值:", sid)

if not host:
    print("[问题B] BK_ITSM_V4_HOST 为空")
    print("        现象：点「前往IT服务管理中心」跳转到监控自己的 /exception 404 页")
    print("        解法：在部署配置中补 BK_ITSM_V4_HOST=<ITSM 站点地址>，然后重启服务")
else:
    print("[OK] BK_ITSM_V4_HOST:", host)
print("=" * 72)
