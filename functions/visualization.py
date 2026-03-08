
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from google.genai import types


def generate_image(prompt, income, expenses, savings, debt):

    os.makedirs("generated_images", exist_ok=True)
    destination = os.path.join("generated_images", "generated_image.png")

    data = {
        "Category": ["Income", "Expenses", "Savings", "Debt"],
        "Amount": [income, expenses, savings, debt]
    }

    df = pd.DataFrame(data)

    sns.set_theme(style="whitegrid")

    prompt_lower = prompt.lower()

    plt.figure(figsize=(8, 6))

    if "pie" in prompt_lower:
        plt.pie(df["Amount"], labels=df["Category"], autopct="%1.1f%%")
        plt.title("Financial Distribution")

    elif "line" in prompt_lower:
        sns.lineplot(x="Category", y="Amount", data=df, marker="o")
        plt.title("Financial Trend")

    else:
        sns.barplot(x="Category", y="Amount", data=df)
        plt.title("Financial Overview")

    plt.tight_layout()
    plt.savefig(destination)
    plt.close()

    return destination


generate_image_tool = types.FunctionDeclaration(
    name="generate_image",
    description="Generate financial charts from user financial data",
    parameters=types.Schema(
        type="object",
        properties={
            "prompt": types.Schema(type="string"),
        },
        required=["prompt"]
    )
)

