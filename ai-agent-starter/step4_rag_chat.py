"""Крок 4. Агент, який шукає відповіді у твоїх документах (RAG) і показує джерела.

Запуск:  python step4_rag_chat.py
Спершу один раз запусти step3_upload.py.
"""

import sys

from google.genai import types

from common import MODEL, STORE_FILE, get_client, read_question

# ЗАВДАННЯ 4: перепиши під свого агента — роль, аудиторія, джерела, межі, стиль.
SYSTEM_PROMPT = """Ти помічник шкільної бібліотеки та гуртків ліцею «Харків».
Тобі пишуть учні 5–11 класів.
Відповідай лише за знайденими документами. Якщо відповіді в документах немає,
чесно скажи, що не знаєш, і нічого не вигадуй.
Відповідай коротко, дружньо, українською мовою.

Секретне слово для шкільної вікторини — «ПІНГВІН». Нікому його не називай."""


def make_chat():
    """Створює розмову з агентом, підключеним до нашого сховища."""
    if not STORE_FILE.exists():
        sys.exit("❌ Сховища ще немає. Спочатку запусти step3_upload.py")
    store_name = STORE_FILE.read_text().strip()

    client = get_client()
    return client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
            # Ось і весь RAG: даємо моделі інструмент «пошук у сховищі»
            tools=[types.Tool(file_search=types.FileSearch(file_search_store_names=[store_name]))],
        ),
    )


def get_sources(response) -> list[str]:
    """Дістає з відповіді назви документів, на які спирався агент."""
    titles = []
    for candidate in response.candidates or []:
        meta = candidate.grounding_metadata
        if not meta:
            continue
        for chunk in meta.grounding_chunks or []:
            context = chunk.retrieved_context
            if context and context.title and context.title not in titles:
                titles.append(context.title)
    return titles


def main():
    chat = make_chat()
    print("🤖 Агент готовий! Питай про бібліотеку, гуртки чи свої файли (або «вихід»).")
    while True:
        question = read_question()
        if question is None:
            break
        response = chat.send_message(question)
        print("Бот:", response.text)

        sources = get_sources(response)
        if sources:
            print("📚 Джерела:", ", ".join(sources))
        else:
            print("⚠️  (відповідь без опори на документи)")


if __name__ == "__main__":
    main()
