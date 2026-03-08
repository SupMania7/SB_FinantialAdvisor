
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from google.genai import types


def generate_image(prompt, width=1024, height=1024):
    """
    Generates a financial chart based on the prompt using matplotlib and seaborn.
    The chart type is inferred from the prompt.
    """

    os.makedirs("generated_images", exist_ok=True)
    destination = os.path.join("generated_images", "generated_image.png")

    # Example financial dataset (can be replaced with real data later)
    data = {
        "Category": ["Income", "Expenses", "Savings", "Debt"],
        "Amount": [50000, 30000, 15000, 5000]
    }

    df = pd.DataFrame(data)

    sns.set_theme(style="whitegrid")

    prompt_lower = prompt.lower()

    plt.figure(figsize=(8, 6))

    # Decide graph type based on prompt
    if "pie" in prompt_lower:
        plt.pie(df["Amount"], labels=df["Category"], autopct="%1.1f%%")
        plt.title("Financial Distribution")

    elif "bar" in prompt_lower:
        sns.barplot(x="Category", y="Amount", data=df)
        plt.title("Financial Overview")

    elif "line" in prompt_lower:
        sns.lineplot(x="Category", y="Amount", data=df, marker="o")
        plt.title("Financial Trend")

    else:
        # Default chart
        sns.barplot(x="Category", y="Amount", data=df)
        plt.title("Financial Overview")

    plt.tight_layout()
    plt.savefig(destination)
    plt.close()

    return destination


generate_image_tool = types.FunctionDeclaration(
    name="generate_image",
    description=(
        "Generate financial charts such as bar charts, pie charts, or line graphs "
        "to visualize financial data."
    ),
    parameters=types.Schema(
        type="object",
        properties={
            "prompt": types.Schema(
                type="string",
                description="Description of the chart to generate"
            ),
            "width": types.Schema(
                type="integer",
                description="Chart width in pixels",
                default=1024
            ),
            "height": types.Schema(
                type="integer",
                description="Chart height in pixels",
                default=1024
            ),
        },
        required=["prompt"]
    )
)

