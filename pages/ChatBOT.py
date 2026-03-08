
import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()


def main():

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    st.set_page_config(page_title="AI Assistant")

    st.title("💬 AI Finance Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_chat = st.text_input("Ask me anything about finance")

    if st.button("Send") and user_chat:

        with st.spinner("Thinking..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_chat
            )

        reply = response.text

        st.session_state.chat_history.append(("user", user_chat))
        st.session_state.chat_history.append(("bot", reply))

    for role, message in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**AI:** {message}")


if __name__ == "__main__":
    main()

