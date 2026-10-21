"""Бонус. Той самий агент, але у браузері.

Запуск:  streamlit run bonus_web.py
"""

import streamlit as st

from step4_rag_chat import get_sources, make_chat

st.set_page_config(page_title="Шкільний помічник", page_icon="🤖")
st.title("🤖 Шкільний помічник")

# Streamlit перезапускає скрипт на кожну дію, тому розмову зберігаємо в session_state
if "chat" not in st.session_state:
    st.session_state.chat = make_chat()
    st.session_state.history = []

for role, text in st.session_state.history:
    st.chat_message(role).markdown(text)

if question := st.chat_input("Твоє питання"):
    st.chat_message("user").markdown(question)
    with st.spinner("Шукаю в документах…"):
        response = st.session_state.chat.send_message(question)

    answer = response.text
    sources = get_sources(response)
    if sources:
        answer += "\n\n📚 *Джерела:* " + ", ".join(sources)
    st.chat_message("assistant").markdown(answer)

    st.session_state.history += [("user", question), ("assistant", answer)]
