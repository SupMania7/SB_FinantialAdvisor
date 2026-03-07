import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()


def main():

    # Create GenAI client
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    st.set_page_config(page_title="AI Financial Advisor", layout="wide")

    st.title("💰 AI Financial Advisor")
    st.write("Get personalized financial insights powered by Gemini AI")

    # Sidebar for system prompt
    st.sidebar.header("System Prompt")

    system_prompt = st.sidebar.text_area(
        "Define AI behaviour",
        value="""You are an expert financial advisor.
Provide practical financial advice based on user income,
expenses, savings, debts, and goals.
Give clear and actionable suggestions."""
    )

    # User financial inputs
    st.subheader("Enter Your Financial Details")

    income = st.number_input("Monthly Income (₹)", min_value=0)
    expenses = st.number_input("Monthly Expenses (₹)", min_value=0)
    savings = st.number_input("Current Savings (₹)", min_value=0)
    debt = st.number_input("Outstanding Debt (₹)", min_value=0)

    goal = st.text_input(
        "Financial Goal (optional)",
        placeholder="Example: Save ₹5,00,000 in 3 years"
    )

    if st.button("Generate Financial Plan"):

        user_prompt = f"""
User Financial Details:

Monthly Income: ₹{income}
Monthly Expenses: ₹{expenses}
Savings: ₹{savings}
Debt: ₹{debt}
Goal: {goal}

Provide:
1. Financial health analysis
2. Budget improvement suggestions
3. Debt management advice
4. Investment suggestions
5. Goal strategy
"""

        final_prompt = system_prompt + "\n\n" + user_prompt

        with st.spinner("Analyzing your finances..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=final_prompt
            )

        st.subheader("📊 AI Financial Advice")
        st.write(response.text)


if __name__ == "__main__":
    main()