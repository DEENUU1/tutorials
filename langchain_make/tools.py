import os
from typing import Type, Any

import requests
from dotenv import load_dotenv
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

load_dotenv()


class NotionCreateInput(BaseModel):
    # title: str = Field(description="Short title of a note based on content of a note")
    content: str = Field(description="Body of a note")


class NotionCreateNoteTool(BaseTool):
    name = "notion_create_note_tool"
    description = "Useful when you need to write a note in Notion"
    args_schema: Type[BaseModel] = NotionCreateInput

    def _run(self, content: str, title: str = None):
        try:
            response = requests.post(
                os.getenv("MAKE"),
                data={
                    "title": "AI Note",
                    "content": content
                }

            )
            return response.text
        except Exception as e:
            raise e

    def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Not implemented")
