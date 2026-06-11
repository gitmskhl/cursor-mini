import os
import sys
import argparse
from colorama import Fore

class WorkspaceError(Exception):
    """Исключение, если путь выходит за границы WORKSPACE."""
    pass

def _get_workspace() -> str:
    """
    Определяет путь WORKSPACE в порядке приоритета:
    1. Аргумент командной строки --workspace (если указан и является валидной существующей директорией).
    2. Переменная WORKSPACE в окружении (или файле .env).
    3. По умолчанию: текущая директория (./).
    """
    # 1. Проверка аргументов командной строки
    # add_help=False и parse_known_args() нужны, чтобы не ломать парсинг аргументов в main.py
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--workspace', type=str, help='Путь к рабочей директории')
    args, _ = parser.parse_known_args()
    
    if args.workspace:
        candidate = args.workspace
        # Проверяем, что путь существует и является директорией
        if os.path.exists(candidate) and os.path.isdir(candidate):
            return os.path.abspath(candidate)
        else:
            print(Fore.LIGHTRED_EX, f"Предупреждение: Неверный путь WORKSPACE в аргументах ('{candidate}'). Переходим к чтению из окружения.", Fore.RESET)

    # 2. Проверка переменной окружения
    # (Для продакшена рекомендуется использовать библиотеку python-dotenv: `from dotenv import load_dotenv`)
    if os.environ.get("WORKSPACE"):
        return os.path.abspath(os.environ.get("WORKSPACE")) # type: ignore

    # 3. По умолчанию ./
    return os.path.abspath('./')

# Инициализация WORKSPACE при импорте модуля
WORKSPACE = _get_workspace()

def save_path(path: str) -> str:
    """
    Приводит переданный путь к безопасному относительному пути внутри WORKSPACE.
    - Если путь относительный, он интерпретируется относительно WORKSPACE.
    - Если путь абсолютный, он проверяется на принадлежность WORKSPACE.
    В любом случае бросает исключение, если итоговый путь выходит за пределы WORKSPACE.
    
    Возвращает:
        Нормализованный относительный путь от корня WORKSPACE.
        
    Исключения:
        RuntimeError – если WORKSPACE не задан.
        WorkspaceError – если путь выходит за WORKSPACE.
    """
    if not WORKSPACE:
        raise RuntimeError("WORKSPACE is not set. Set WORKSPACE to an absolute path.")

    workspace_root = os.path.realpath(os.path.abspath(WORKSPACE))

    if os.path.isabs(path):
        full_path = os.path.realpath(path)
    else:
        full_path = os.path.realpath(os.path.join(workspace_root, path))

    # Проверка, что full_path остаётся внутри workspace_root
    # os.path.commonpath корректно работает, так как оба пути абсолютные и нормализованные
    if os.path.commonpath([workspace_root, full_path]) != workspace_root:
        raise WorkspaceError(f"Path escapes workspace: {path}")

    return os.path.relpath(full_path, workspace_root)