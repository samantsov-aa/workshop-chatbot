"""Прибирання після заняття: видаляє сховище з хмари Google.

Запуск:  python cleanup.py
"""

from common import STORE_FILE, get_client

if not STORE_FILE.exists():
    print("Сховища немає — прибирати нічого.")
else:
    store_name = STORE_FILE.read_text().strip()
    get_client().file_search_stores.delete(name=store_name, config={"force": True})
    STORE_FILE.unlink()
    print("🗑  Сховище видалено:", store_name)
