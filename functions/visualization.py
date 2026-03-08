
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from google.genai import types


def generate_image(prompt, income, expenses, savings, debt):

    os.makedirs("generated_images", exist_ok=True)
    destination = os.path.join("generated_images", "generated_image.png")

    data = {
        "Income": income,
        "Expenses": expenses,
        "Savings": savings,
        "Debt": debt
    }


    filtered = {k: v for k, v in data.items() if v != 0}

    df = pd.DataFrame({
        "Category": list(filtered.keys()),
        "Amount": list(filtered.values())
    })

    sns.set_theme(style="whitegrid")

    prompt_lower = prompt.lower()

    plt.figure(figsize=(8, 6))

    months = [
        "jan","feb","mar","apr","may","jun",
        "jul","aug","sep","oct","nov","dec"
    ]

    years = [str(y) for y in range(1900, 2101)]

    time_labels = []

    for m in months:
        if m in prompt_lower:
            time_labels.append(m.capitalize())

    for y in years:
        if y in prompt_lower:
            time_labels.append(y)

    # TIME BASED GRAPH
    if time_labels:

        if "line" in prompt_lower:

            sns.lineplot(
                x=time_labels,
                y=list(filtered.values())[:len(time_labels)],
                marker="o"
            )

            plt.xlabel("Time")
            plt.ylabel("Amount")
            plt.title("Financial Trend Over Time")

        else:

            sns.barplot(
                x=time_labels,
                y=list(filtered.values())[:len(time_labels)]
            )

            plt.xlabel("Time")
            plt.ylabel("Amount")
            plt.title("Financial Values Over Time")

    elif "pie" in prompt_lower:

        plt.pie(
            df["Amount"],
            labels=df["Category"],
            autopct="%1.1f%%"
        )
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

