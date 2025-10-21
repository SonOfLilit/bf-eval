import os
import logging

import logfire
from dotenv import load_dotenv
from google.genai.client import Client
from google.genai.types import HttpOptions, HttpRetryOptions
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai import ModelSettings
from pydantic_ai.providers.google import GoogleProvider


load_dotenv()

logfire.configure(token=os.environ["PYDANTIC_LOGFIRE_API_KEY"])
logfire.instrument_pydantic_ai()
logfire.instrument_httpx(capture_all=True)
logging.basicConfig(level=logging.DEBUG)


model = GoogleModel(
    "gemini-2.5-flash",
    provider=GoogleProvider(
        client=Client(
            http_options=HttpOptions(
                retry_options=HttpRetryOptions(
                    attempts=3, initial_delay=0.1, max_delay=30
                )
            )
        )
    ),
    settings=GoogleModelSettings(
        max_tokens=5000, google_thinking_config={"thinking_budget": 1024}
    ),
)
# model = AnthropicModel(
#     "claude-sonnet-4-5-20250929",
#     settings=ModelSettings(max_tokens=5000),
# )
