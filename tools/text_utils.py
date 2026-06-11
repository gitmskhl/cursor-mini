from fnmatch import fnmatch
from pathlib import Path
from typing import Iterator


BINARY_CHECK_BYTES = 8192
PATHIGNORE_FILE = ".pathignore"
TEXT_ENCODINGS_WITH_NULL_BYTES = {
    "utf-16",
    "utf-16-be",
    "utf-16-le",
    "utf-32",
    "utf-32-be",
    "utf-32-le",
}


def load_pathignore_patterns(base_dir: Path | None = None) -> list[str]:
    ignore_file = (base_dir or Path.cwd()) / PATHIGNORE_FILE

    if not ignore_file.is_file():
        return []

    patterns: list[str] = []
    for line in ignore_file.read_text(encoding="utf-8").splitlines():
        pattern = line.strip()
        if not pattern or pattern.startswith("#"):
            continue
        patterns.append(pattern)

    return patterns


def is_path_ignored(path: Path, patterns: list[str], base_dir: Path | None = None) -> bool:
    if not patterns:
        return False

    root = (base_dir or Path.cwd()).resolve()
    resolved_path = path.resolve()

    try:
        relative_path = resolved_path.relative_to(root)
    except ValueError:
        relative_path = path

    path_parts = relative_path.parts
    normalized_path = relative_path.as_posix()
    is_dir = path.is_dir()

    for pattern in patterns:
        normalized_pattern = pattern.replace("\\", "/").strip("/")

        if not normalized_pattern:
            continue

        if pattern.endswith("/"):
            if normalized_pattern in path_parts:
                return True
            continue

        if fnmatch(normalized_path, normalized_pattern):
            return True

        if "/" not in normalized_pattern and any(
            fnmatch(part, normalized_pattern) for part in path_parts
        ):
            return True

        if is_dir and fnmatch(f"{normalized_path}/", pattern.replace("\\", "/")):
            return True

    return False


def iter_unignored_paths(directory: Path, patterns: list[str]) -> Iterator[Path]:
    for item in sorted(directory.iterdir(), key=lambda entry: str(entry).lower()):
        if is_path_ignored(item, patterns):
            continue

        yield item

        if item.is_dir():
            yield from iter_unignored_paths(item, patterns)


def is_binary_file(path: Path, encoding: str = "utf-8") -> bool:
    with path.open("rb") as file:
        chunk = file.read(BINARY_CHECK_BYTES)

    if b"\0" not in chunk:
        return False

    return encoding.lower().replace("_", "-") not in TEXT_ENCODINGS_WITH_NULL_BYTES


def read_text_file(path: Path, encoding: str = "utf-8") -> str:
    return path.read_text(encoding=encoding)
