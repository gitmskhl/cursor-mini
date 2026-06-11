# utils.py

MAX_OUTPUT_CHARS = 10000  # лимит по умолчанию, может быть переопределён


def truncate_output(text: str, limit: int = MAX_OUTPUT_CHARS) -> str:
    """
    Возвращает текст, обрезанный до заданного лимита символов, если он длиннее лимита.
    В конец добавляется сообщение с информацией о полной длине и лимите.

    Аргументы:
        text: исходная строка.
        limit: максимальное число символов (по умолчанию MAX_OUTPUT_CHARS).

    Возвращает:
        Исходный текст, если его длина <= limit.
        Иначе: первые `limit` символов, затем строка
        "... [truncated: output was {длина_исходного} chars, limit is {limit}]".
    """
    if len(text) <= limit:
        return text
    return text[:limit] + f"... [truncated: output was {len(text)} chars, limit is {limit}]"