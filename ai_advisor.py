
import streamlit as st
from google.genai import types
import os
from functions.visualization import generate_image_tool, generate_image


def advisor(client):
    """
    Handles the financial advisor workflow using Gemini
    """

    st.title("💰 AI Financial Advisor")
    st.write("Get personalized financial insights powered by Gemini AI")

    system_prompt = """You are a professional AI Financial Advisor.

Analyze the user's financial data and give structured advice.

You may generate visual diagrams or charts if it helps explain financial planning.
"""

    available_functions = types.Tool(
        function_declarations=[generate_image_tool]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions],
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

    if st.button("Generate Financial Plan"):

        user_prompt = f"""
User Financial Details:

Monthly Income: ₹{income}
Monthly Expenses: ₹{expenses}
Savings: ₹{savings}
Debt: ₹{debt}
Goal: {goal}
"""

        messages = [
            types.Content(
                role="user",
                parts=[types.Part(text=user_prompt)]
            )
        ]

        with st.spinner("Analyzing your finances..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=config
            )

        candidate = response.candidates[0]
        part = candidate.content.parts[0]

        if response.function_calls:

            for function_call in response.function_calls:

                if function_call.name == "generate_image":

                    args = function_call.args

                    generate_image(
                        prompt=args.get("prompt"),
                        width=args.get("width", 1024),
                        height=args.get("height", 1024)
                    )

        st.subheader("📊 AI Financial Advice")
        st.write(part.text)

        image_path = "generated_images/generated_image.png"

        if os.path.exists(image_path):
            st.subheader("📈 Financial Visualization")
            st.image(image_path, use_container_width=True)

