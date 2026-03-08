from functions.visualization import generate_image
from google.genai import types


def call_function(function_call_part, verbose=False):

    if verbose:
        print("Function call:", function_call_part.name)
        print("Arguments:", function_call_part.args)
    else:
        print("Calling function:", function_call_part.name)

    result = None

   
    if function_call_part.name == "generate_image":
        result = generate_image(**function_call_part.args)

    
    if result is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={
                        "error": f"Unknown function: {function_call_part.name}"
                    }
                )
            ],
        )

    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result}
            )
        ],
    )