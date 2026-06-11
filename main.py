from dotenv import load_dotenv

load_dotenv()
from email import message

from llm import send_to_llm
from tool_registry import TOOLS_SCHEMA, FUNCTIONS
from colorama import Fore
import json

MAX_MESSAGES = 30
MAX_STEPS = 30

SYSTEM_PROMPT = """
You are a coding assistant with access to tools.

Use tools whenever information is needed.

Available tools:
- list_files: list files and directories
- get_file_info: inspect file metadata
- search_text: search text in project files
- read_file: read text files, optionally from start_line to end_line
- write_file: create or overwrite files
- replace_text: replace exact text in files
- write_chunk: insert text at a line number
- replace_chunk: replace a line range with text
- append_file: append text to files
- execute_python: execute Python programs with optional args
- execute_bash: execute Bash scripts

Rules:
- Never invent tool results.
- Base answers on tool outputs.
- Use search_text before opening many files.
- Use get_file_info before reading large files.
- If read_file says a file is too large, call read_file again with start_line and end_line.
- Prefer replace_text, write_chunk, replace_chunk, or append_file for small edits instead of rewriting an entire file.
- When fixing code:
  1. inspect files
  2. modify code
  3. execute code
  4. analyze errors
  5. try again if possible
"""

messages: list[dict] = []

messages.append({
    "role": "system",
    "content": SYSTEM_PROMPT
})

system_prompt_msg = messages[0]

error = False

while not error:
    query = input("(`q` to quit) > ")
    if query.lower() in ('q', 'quit', 'exit'):
        ans = input('Are you sure you want to quit? (Y/n): ')
        if ans.lower() in ('y', 'yes', ''):
            break
    
    if len(messages) > MAX_MESSAGES:
        messages = [
            system_prompt_msg,
            *messages[-(MAX_MESSAGES - 1):]
        ]
    
    messages.append({
        "role": "user",
        "content": query
    })
    
    for step in range(MAX_STEPS):
        llm_response = send_to_llm(messages, tools=TOOLS_SCHEMA)
        if not llm_response:
            error = True
            break
        
        assistant_message = llm_response.choices[0].message
        
        messages.append(assistant_message.model_dump(exclude_none=True))
        
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name # type: ignore
                tool_args = json.loads(tool_call.function.arguments or "{}") # type: ignore
                args_text = ', '.join([f"{name}={val}" for name, val in tool_args.items()])
                print(Fore.GREEN, f"\t{tool_name}(", args_text, ")")
                if tool_name in FUNCTIONS:
                    try:
                        tool_result = FUNCTIONS[tool_name](**tool_args)
                    except Exception as e:
                        print(Fore.RED, "Error: ", e, Fore.RESET)
                        tool_result = str(e)
                else:
                    tool_result = f"Unknown tool: {tool_name}"
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                })
            if step == MAX_STEPS - 1:
                print(Fore.RED, "Agent reached maximum number of steps!", Fore.RESET)
        else:
            print(Fore.MAGENTA, assistant_message.content, Fore.RESET)
            break
