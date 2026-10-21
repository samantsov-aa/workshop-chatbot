"""Крок 3. Завантажуємо всі файли з папки materials у сховище (File Search store).

Запуск:  python step3_upload.py
Запускай щоразу, коли додаєш або змінюєш файли в materials.
"""

import shutil
import tempfile
import time
from pathlib import Path

from common import MATERIALS, STORE_FILE, get_client

ALLOWED = {".md", ".txt", ".pdf", ".docx", ".html"}

client = get_client()

# Старе сховище видаляємо, щоб файли не дублювалися
if STORE_FILE.exists():
    old_store = STORE_FILE.read_text().strip()
    try:
        client.file_search_stores.delete(name=old_store, config={"force": True})
        print("🗑  Старе сховище видалено")
    except Exception:  # noqa: BLE001 — якщо його вже немає, нічого страшного
        pass

store = client.file_search_stores.create(config={"display_name": "school-agent"})
STORE_FILE.write_text(store.name)
print("📦 Створено сховище:", store.name)

files = sorted(p for p in MATERIALS.iterdir() if p.suffix.lower() in ALLOWED)
for i, path in enumerate(files):
    print(f"⬆️  {path.name} ...", end=" ", flush=True)
    # Завантажуємо копію з латинською назвою: кирилиця в імені файлу ламає завантаження.
    # Справжня назва їде в display_name — її й покаже бот у «Джерелах».
    with tempfile.TemporaryDirectory() as tmp:
        safe_copy = Path(tmp) / f"file{i}{path.suffix.lower()}"
        shutil.copyfile(path, safe_copy)
        operation = client.file_search_stores.upload_to_file_search_store(
            file=str(safe_copy),
            file_search_store_name=store.name,
            config={"display_name": path.stem},
        )
    # Google розрізає файл на шматки й індексує їх — чекаємо, поки закінчить
    while not operation.done:
        time.sleep(2)
        operation = client.operations.get(operation)
    print("✅")

print(f"\nГотово! Завантажено файлів: {len(files)}. Тепер запускай step4_rag_chat.py")
