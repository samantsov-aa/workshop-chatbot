"""Спільні налаштування для всіх кроків. Тут нічого міняти не треба."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Щоб емодзі й кирилиця не ламали ввід і вивід у будь-якому терміналі
for stream in (sys.stdin, sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
MATERIALS = ROOT / "materials"
STORE_FILE = ROOT / "store_name.txt"  # сюди step3 записує назву сховища

EXIT_WORDS = ("вихід", "exit", "quit", "q")


def read_question() -> str | None:
    """Питає користувача. Повертає None, якщо він хоче вийти."""
    while True:
        try:
            question = input("\nТи: ").strip()
        except (EOFError, KeyboardInterrupt):  # Ctrl+C або кінець вводу
            return None
        if question.lower() in EXIT_WORDS:
            return None
        if question:
            return question


_client: genai.Client | None = None


def get_client() -> genai.Client:
    """Повертає клієнта Gemini. Ключ береться з файлу .env."""
    global _client
    if not os.getenv("GEMINI_API_KEY"):
        sys.exit("❌ Немає ключа GEMINI_API_KEY. Перевір файл .env або поклич учителя.")
    # Один клієнт на всю програму: якщо його «загубити», SDK закриває з'єднання
    if _client is None:
        _client = genai.Client()
    return _client
