
import streamlit as st
from google.genai import types
import os
from functions.visualization import generate_image
from functions.executefunc import load_css

def advisor(client):

    st.title("AI Financial Advisor")
    st.write("Get personalized financial insights powered by Gemini AI")

    system_prompt = """You are a professional AI Financial Advisor.

Analyze the user's financial data and give structured advice.
"""

    config = types.GenerateContentConfig(
        system_instruction=system_prompt
    )

    st.subheader("Enter Your Financial Details")

    income = st.number_input("Monthly Income (₹)", min_value=0)
    expenses = st.number_input("Monthly Expenses (₹)", min_value=0)
    savings = st.number_input("Current Savings (₹)", min_value=0)
    debt = st.number_input("Outstanding Debt (₹)", min_value=0)

    goal = st.text_input(
        "Financial Goal (optional)",
        placeholder="Example: Save ₹5,00,000 in 3 years"
    )

   

    generate_chart = st.checkbox("Generate Financial Diagram")

    chart_prompt = None

    if generate_chart:
        chart_prompt = st.text_input(
            "Describe the chart you want",
            placeholder="Example: pie chart of my finances"
        )

    

    if st.button("Generate Financial Plan"):

        user_prompt = f"""
User Financial Details:

Monthly Income: ₹{income}
Monthly Expenses: ₹{expenses}
Savings: ₹{savings}
Debt: ₹{debt}
Goal: {goal}
"""

        with st.spinner("Analyzing your finances..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=config
            )

        st.subheader("📊 AI Financial Advice")
        st.write(response.text)

       

        if generate_chart and chart_prompt:

            st.subheader("📈 Financial Visualization")

            path = generate_image(
                prompt=chart_prompt,
                income=income,
                expenses=expenses,
                savings=savings,
                debt=debt
            )

            if os.path.exists(path):
                st.image(path, use_container_width=True)

