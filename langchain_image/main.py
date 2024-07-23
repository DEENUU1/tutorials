import base64
import os
from typing import Any

from langchain.chains import TransformChain
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import chain
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"


class ImageInformation(BaseModel):
    car: bool = Field(
        ...,
        example=True,
        description="Set to True if image contains car else return False.",
    )
    color: str = Field(
        ...,
        example="red",
        description="The color of the car. Possible values are: 'red', 'black', 'white', or 'none' if no car is detected.",
    )


parser = JsonOutputParser(pydantic_object=ImageInformation)


def load_image(inputs: dict) -> dict:
    image_path = inputs["image_path"]

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    image_base64 = encode_image(image_path)
    return {"image": image_base64}


load_image_chain = TransformChain(
    input_variables=["image_path"], output_variables=["image"], transform=load_image
)


@chain
def image_model(inputs: dict) -> str | list[str | dict[Any, Any]]:
    model: ChatOpenAI = ChatOpenAI(
        temperature=0.5,
        model="gpt-4o-2024-05-13",
        max_tokens=1024,
    )
    msg = model.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": inputs["prompt"]},
                    {"type": "text", "text": parser.get_format_instructions()},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{inputs['image']}"
                        },
                    },
                ]
            )
        ]
    )
    return msg.content


def get_image_information(image_path: str) -> dict:
    vision_prompt = """Return the color of a car and value if car was found.
    You can only return values: red, black, white or none.
    # Example 1
    color: red
    car: True
    # Example 2
    color: none
    car: False
    # Example 3 - There is a car but none of the valid colors
    color: none
    car: True
    """
    vision_chain = load_image_chain | image_model | parser
    try:
        return vision_chain.invoke(
            {"image_path": f"{image_path}", "prompt": vision_prompt}
        )
    except OutputParserException as e:
        return {
            "car": False,
            "color": "none",
        }
    except Exception as e:
        return {
            "car": False,
            "color": "none",
        }


if __name__ == "__main__":
    black_car = get_image_information("black.jpeg")
    print("Black car")
    print(black_car)

    red_car = get_image_information("red.jpg")
    print("Red car")
    print(red_car)

    white = get_image_information("white.jpg")
    print("White car")
    print(white)

    racing_bike = get_image_information("racing_bike.jpeg")
    print("Racing bike")
    print(racing_bike)
