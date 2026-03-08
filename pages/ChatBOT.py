import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from functions.executefunc import load_css

st.set_page_config(page_title="AI Finance Assistant", layout="wide")

theme = st.sidebar.toggle("Light Mode", key="theme_toggle")

if theme:
    load_css("light")
else:
    load_css("dark")

load_dotenv()


def main():

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    st.title("💬 AI Finance Assistant")

    system_prompt = """
You are a concise and practical AI assistant.

Guidelines for every reply:

1. Write clear, coherent answers that fully address the user's request.
2. Keep responses short and focused, but never cut off sentences or ideas.
3. Avoid unnecessary filler, repetition, or long explanations.
4. Prefer short responses unless the user explicitly asks for detail.
5. If calculations are needed, show them clearly.
6. Ensure the final sentence completes the idea.
7. Never stop mid-sentence or mid-thought.
8. If information is missing, ask one short clarification question.

Tone:
Direct, helpful, and practical.
"""

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        max_output_tokens=400,
        temperature=0.4
    )

   
    if "messages" not in st.session_state:
        st.session_state.messages = []

   
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
    prompt = st.chat_input("Ask me anything about finance")

    if prompt:

        
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                contents = []

                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"

                    contents.append(
                        {
                            "role": role,
                            "parts": [{"text": msg["content"]}]
                        }
                    )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=config
                )

                reply = ""

                try:
                    if response.candidates:
                        parts = response.candidates[0].content.parts
                        reply = "".join(
                            part.text for part in parts if hasattr(part, "text")
                        )
                except:
                    reply = "Sorry, I couldn't generate a response."

                reply = reply.strip()

                if not reply:
                    reply = "I couldn't generate a response."

                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()