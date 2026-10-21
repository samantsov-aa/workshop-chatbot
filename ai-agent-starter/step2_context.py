"""Крок 2. Даємо боту знання найпростішим способом: вставляємо весь файл у промпт.

Запуск:  python step2_context.py
"""

from google.genai import types

from common import MATERIALS, MODEL, get_client, read_question

# Можеш підставити будь-який файл із папки materials
FILE = MATERIALS / "school_library.md"
knowledge = FILE.read_text(encoding="utf-8")

SYSTEM_PROMPT = f"""Ти помічник шкільної бібліотеки.
Відповідай лише на основі тексту нижче.
Якщо відповіді в тексті немає, чесно скажи, що не знаєш.

--- ТЕКСТ ---
{knowledge}
--- КІНЕЦЬ ТЕКСТУ ---"""

client = get_client()
chat = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.2),
)

print(f"🤖 Бот прочитав файл {FILE.name}. Питай (або «вихід»).")
while True:
    question = read_question()
    if question is None:
        break
    response = chat.send_message(question)
    print("Бот:", response.text)
    # Скільки тексту (токенів) модель прочитала, щоб відповісти.
    # Зверни увагу: весь файл надсилається з КОЖНИМ питанням.
    print(f"   (прочитано токенів: {response.usage_metadata.prompt_token_count})")
