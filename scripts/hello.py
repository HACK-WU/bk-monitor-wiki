import os
import sys
from pathlib import Path

import django
from dotenv import load_dotenv

BASE_DIR = Path(os.path.abspath(__file__)).parent
BKMONITOR_DIR = BASE_DIR / "bkmonitor"
TARGET_URL = "/fta/rest/v3/incidents/"

sys.path.insert(0, str(BKMONITOR_DIR))
sys.path.append(str(BKMONITOR_DIR / "packages"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

load_dotenv(str(BASE_DIR / ".env"))
django.setup()