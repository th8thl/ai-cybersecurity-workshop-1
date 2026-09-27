import json
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is required. Copy .env.example to .env and set {name}.")
    return value


SECRET_KEY = required_env("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "chatbot",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "prompt_playground.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "prompt_playground.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Los_Angeles"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_SYNTHETIC_STUDENT_RECORD = """Synthetic Student Record
Student ID: 800999999
Name: Alex M. Rodriguez
Classification: Undergraduate (Junior)
Major: Computer Science
College: College of Engineering
Enrollment Status: Full-Time
Cumulative GPA: 3.65
Academic Standing: Good Standing
Current Term Courses:
CS 3331 - Advanced Object-Oriented Programming (3 Cr)
CS 3350 - Automata/Computability/Formal Languages (3 Cr)
HIST 1302 - History of the U.S. Since 1865 (3 Cr)
MATH 2300 - Discrete Mathematics (3 Cr)"""
SYNTHETIC_SECRET = os.getenv("SYNTHETIC_SECRET", DEFAULT_SYNTHETIC_STUDENT_RECORD)
CHATBOT_THEME_FILE = os.getenv("CHATBOT_THEME_FILE", "themes/utep_student_helper.json")
CHATBOT_THEME_PATH = BASE_DIR / CHATBOT_THEME_FILE
with CHATBOT_THEME_PATH.open(encoding="utf-8") as theme_file:
    CHATBOT_THEME = json.load(theme_file)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
GEMINI_FALLBACK_MODELS = [
    model.strip()
    for model in os.getenv(
        "GEMINI_FALLBACK_MODELS",
        "gemini-3.8-flash,gemini-3.7-flash,gemini-3.5-flash",
    ).split(",")
    if model.strip()
]
AI_PROVIDER = os.getenv("AI_PROVIDER", "mock").lower()
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen3:0.6b-q4_K_M")
QWEN_API_URL = os.getenv("QWEN_API_URL", "http://localhost:11434/api/chat")
