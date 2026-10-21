"""Крок 1. Перша розмова з моделлю.

Запуск:  python step1_chat.py      (щоб вийти, напиши «вихід»)
"""

from google.genai import types

from common import MODEL, get_client, read_question

# ЗАВДАННЯ 1.2: зміни характер бота.
# Спробуй: «Ти пірат», «Відповідай лише одним реченням»,
# «Ти репетитор, який не дає готових відповідей, а ставить навідні питання».
SYSTEM_PROMPT = """Ти дружній помічник для школярів.
Відповідай коротко і зрозуміло, українською мовою."""

# ЗАВДАННЯ 1.3: регулятор фантазії. 0 — стримано, 2 — максимально творчо.
TEMPERATURE = 0.7

client = get_client()

# chat пам'ятає всю розмову, тому бот «знає», що ти казав раніше
chat = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=TEMPERATURE,
    ),
)

print("🤖 Бот готовий! Напиши питання (або «вихід»).")
while True:
    question = read_question()
    if question is None:
        break
    response = chat.send_message(question)
    print("Бот:", response.text)
