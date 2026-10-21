"""Крок 0. Перевіряємо, що все встановлено і ключ працює.

Запуск:  python check_setup.py
"""

import sys

print("Python", sys.version.split()[0])
if sys.version_info < (3, 10):
    sys.exit("❌ Потрібен Python 3.10 або новіший.")

try:
    import dotenv  # noqa: F401
    from google import genai  # noqa: F401
except ImportError:
    sys.exit("❌ Бібліотеки не встановлені. Виконай: pip install -r requirements.txt")

from common import MODEL, get_client

client = get_client()
print("Модель:", MODEL)
response = client.models.generate_content(
    model=MODEL,
    contents="Скажи «привіт» одним словом.",
)
print("Модель відповіла:", response.text.strip())
print("✅ Все готово!")
