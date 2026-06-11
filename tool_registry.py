from tools import append_file, execute_bash, execute_python, get_file_info, list_files, read_file, replace_chunk, replace_text, search_text, write_chunk, write_file


TOOLS_SCHEMA = [
    append_file.tool_schema,
    execute_bash.tool_schema,
    execute_python.tool_schema,
    get_file_info.tool_schema,
    list_files.tool_schema,
    read_file.tool_schema,
    replace_chunk.tool_schema,
    replace_text.tool_schema,
    search_text.tool_schema,
    write_chunk.tool_schema,
    write_file.tool_schema
]

FUNCTIONS = {
    "append_file": append_file.append_file,
    "execute_bash": execute_bash.execute_bash,
    "execute_python": execute_python.execute_python,
    "get_file_info": get_file_info.get_file_info,
    "list_files": list_files.list_files,
    "read_file": read_file.read_file,
    "replace_chunk": replace_chunk.replace_chunk,
    "replace_text": replace_text.replace_text,
    "search_text": search_text.search_text,
    "write_chunk": write_chunk.write_chunk,
    "write_file": write_file.write_file
}
