#!!!!!!DON'T RENAMEEEE!!!!!!!
import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from ai_advisor import advisor
from functions.executefunc import load_css


load_dotenv()

st.set_page_config(
    page_title="FinancePlan",
    page_icon="💰",
    layout="wide"
)


def main():

   
    theme = st.sidebar.toggle("Light Mode", key="theme_toggle")

    if theme:
        load_css("light")
    else:
        load_css("dark")

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    advisor(client)


if __name__ == "__main__":
    main()
