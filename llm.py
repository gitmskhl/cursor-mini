import os
from openai import OpenAI
from openai.types.chat import ChatCompletion
from colorama import Fore


PROVIDER = os.environ.get("PROVIDER")

client = OpenAI(
    api_key=os.environ.get(f"{PROVIDER}_API_KEY"),
    base_url=os.environ.get(f"{PROVIDER}_BASE_URL")
)

def send_to_llm(messages: list, tools: list) -> (ChatCompletion | None):
    try:
        response = client.chat.completions.create(
            model=os.environ.get(f"{PROVIDER}_MODEL"), # type: ignore
            messages=messages, 
            tools=tools
        )
        return response
    except Exception as e:
        print(Fore.RED + "Error during sending messages to LLM")
        print("\tMessages length:", len(messages))
        print(e)
        print(Fore.YELLOW, '\tMessages:', messages, Fore.RESET)
        return None
        