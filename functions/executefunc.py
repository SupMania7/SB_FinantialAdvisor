from functions.visualization import generate_image
from google.genai import types
import streamlit as st
import os


def load_css(theme="dark"):

    css_path = f"styles/{theme}.css"

    css = ""

    # Prevent crash if file missing
    if os.path.exists(css_path):
        with open(css_path) as f:
            css = f.read()
    else:
        st.warning(f"CSS file not found: {css_path}")

    custom_chat_css = """
    [data-testid="stChatInput"] {
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    [data-testid="stChatInput"] textarea {
        border-radius: 20px !important;
        border: 1px solid #444 !important;
        padding: 14px 18px !important;
        background-color: #1e1e1e !important;
        color: white !important;
        font-size: 16px !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        outline: none !important;
        border: 1px solid #666 !important;
        box-shadow: none !important;
    }

    [data-testid="stChatInput"] button {
        border-radius: 50% !important;
        background: #2b2b2b !important;
        border: none !important;
    }

    [data-testid="stChatInput"] button:hover {
        background: #3a3a3a !important;
    }
    """

    st.markdown(
        f"<style>{css}{custom_chat_css}</style>",
        unsafe_allow_html=True
    )


def call_function(function_call_part, verbose=False):

    try:

        if verbose:
            print("Function call:", function_call_part.name)
            print("Arguments:", function_call_part.args)
        else:
            print("Calling function:", function_call_part.name)

        result = None

        if function_call_part.name == "generate_image":
            result = generate_image(**function_call_part.args)

        if result is None:
            raise ValueError(f"Unknown function: {function_call_part.name}")

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result}
                )
            ],
        )

    except Exception as e:

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": str(e)}
                )
            ],
        )