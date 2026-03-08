
import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from ai_advisor import advisor

load_dotenv()


def main():

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    st.set_page_config(page_title="AI Financial Advisor", layout="wide")

    # Main financial advisor page
    advisor(client)


if __name__ == "__main__":
    main()

