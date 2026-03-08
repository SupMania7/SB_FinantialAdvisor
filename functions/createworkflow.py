from gradio_client import Client
from huggingface_hub import login
import base64
from google.genai import types
import os
import shutil
login(os.getenv("HUGGINGFACE_TOKEN"))

client = Client("mrfakename/Z-Image-Turbo")


def generate_image(prompt, width=1024, height=1024):

    result = client.predict(
        prompt=prompt,
        height=height,
        width=width,
        num_inference_steps=9,
        seed=42,
        randomize_seed=True,
        api_name="/generate_image"
    )

    image_path = result[0]

    os.makedirs("generated_images", exist_ok=True)
    destination = os.path.join("generated_images", "generated_image.png")

    shutil.copy(image_path, destination)

    return destination

generate_image_tool = types.FunctionDeclaration(
    name="generate_image",
    description=(
        "Generate an image based on a text prompt using the Z-Image-Turbo "
        "image generation model hosted on Hugging Face Spaces. "
        "Returns the file path of the generated image."
    ),
    parameters=types.Schema(
        type="object",
        properties={
            "prompt": types.Schema(
                type="string",
                description="Detailed description of the image to generate"
            ),
            "width": types.Schema(
                type="integer",
                description="Width of the generated image in pixels",
                default=1024
            ),
            "height": types.Schema(
                type="integer",
                description="Height of the generated image in pixels",
                default=1024
            ),
        },
        required=["prompt"]
    )
)
#print(generate_image(prompt="financial budget planning infographic with charts"))
