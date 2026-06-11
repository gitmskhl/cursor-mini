"""
Тесты для модуля workspace.py.

Запуск: pytest tests/test_workspace.py -v
"""

import os
import sys
import pytest
import tempfile

# Добавляем корень проекта в sys.path для импорта workspace.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import workspace
from workspace import _get_workspace, resolve_path, WorkspaceError


class TestGetWorkspace:
    """Тесты для функции _get_workspace() — определения пути WORKSPACE."""

    def test_workspace_from_valid_arg(self, monkeypatch):
        """Извлечение workspace из валидного --workspace аргумента"""
        with tempfile.TemporaryDirectory() as tmpdir:
            monkeypatch.setattr(sys, 'argv', ['main.py', '--workspace', tmpdir])
            result = _get_workspace()
            assert result == os.path.abspath(tmpdir)

    def test_workspace_from_arg_with_equals(self, monkeypatch):
        """Извлечение workspace из аргумента вида --workspace=./path"""
        with tempfile.TemporaryDirectory() as tmpdir:
            monkeypatch.setattr(sys, 'argv', ['main.py', f'--workspace={tmpdir}'])
            result = _get_workspace()
            assert result == os.path.abspath(tmpdir)

    def test_workspace_from_arg_with_other_flags(self, monkeypatch):
        """Извлечение workspace когда есть другие аргументы (parse_known_args)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            monkeypatch.setattr(sys, 'argv', ['main.py', '--port', '8000', '--workspace', tmpdir, '--verbose'])
            result = _get_workspace()
            assert result == os.path.abspath(tmpdir)

    def test_workspace_from_invalid_arg_falls_back_to_env(self, monkeypatch):
        """Невалидный путь в --workspace приводит к fallback на переменную окружения"""
        monkeypatch.setattr(sys, 'argv', ['main.py', '--workspace', '/nonexistent/path/12345'])
        monkeypatch.setenv('WORKSPACE', os.getcwd())
        result = _get_workspace()
        assert result == os.path.abspath(os.getcwd())

    def test_workspace_from_env(self, monkeypatch):
        """Извлечение workspace из переменной окружения WORKSPACE"""
        with tempfile.TemporaryDirectory() as tmpdir:
            monkeypatch.setattr(sys, 'argv', ['main.py'])
            monkeypatch.setenv('WORKSPACE', tmpdir)
            result = _get_workspace()
            assert result == os.path.abspath(tmpdir)

    def test_workspace_default_to_cwd(self, monkeypatch):
        """Если ничего не указано, используется текущая директория"""
        monkeypatch.setattr(sys, 'argv', ['main.py'])
        monkeypatch.delenv('WORKSPACE', raising=False)
        result = _get_workspace()
        assert result == os.path.abspath('./')

    def test_workspace_priority_arg_over_env(self, monkeypatch):
        """Приоритет: --workspace выше чем переменная окружения"""
        with tempfile.TemporaryDirectory() as tmpdir1:
            with tempfile.TemporaryDirectory() as tmpdir2:
                monkeypatch.setattr(sys, 'argv', ['main.py', '--workspace', tmpdir1])
                monkeypatch.setenv('WORKSPACE', tmpdir2)
                result = _get_workspace()
                assert result == os.path.abspath(tmpdir1)


class TestSavePath:
    """Тесты для функции resolve_path() — безопасной работы с путями."""

    def test_resolve_path_relative_inside(self, tmp_path):
        """Относительный путь внутри workspace"""
        workspace.WORKSPACE = str(tmp_path)
        result = resolve_path('subdir/file.txt')
        assert result == os.path.join('subdir', 'file.txt')

    def test_resolve_path_normalized(self, tmp_path):
        """Относительный путь нормализуется (убирается subdir/../)"""
        workspace.WORKSPACE = str(tmp_path)
        result = resolve_path('subdir/../file.txt')
        assert result == 'file.txt'

    def test_resolve_path_absolute_inside(self, tmp_path):
        """Абсолютный путь внутри workspace возвращает относительный"""
        workspace.WORKSPACE = str(tmp_path)
        abs_path = os.path.join(str(tmp_path), 'subdir', 'file.txt')
        result = resolve_path(abs_path)
        assert result == os.path.join('subdir', 'file.txt')

    def test_resolve_path_absolute_outside_raises(self, tmp_path):
        """Абсолютный путь вне workspace вызывает WorkspaceError"""
        workspace.WORKSPACE = str(tmp_path)
        with pytest.raises(WorkspaceError):
            resolve_path('/etc/passwd')

    def test_resolve_path_traversal_raises(self, tmp_path):
        """Path traversal атака (../../) вызывает WorkspaceError"""
        workspace.WORKSPACE = str(tmp_path)
        with pytest.raises(WorkspaceError):
            resolve_path('../../etc/passwd')

    def test_resolve_path_nested_traversal_raises(self, tmp_path):
        """Сложный path traversal внутри относительного пути"""
        workspace.WORKSPACE = str(tmp_path)
        with pytest.raises(WorkspaceError):
            resolve_path('subdir/../../etc/passwd')

    def test_resolve_path_current_dir(self, tmp_path):
        """Текущая директория возвращается как '.'"""
        workspace.WORKSPACE = str(tmp_path)
        result = resolve_path('.')
        assert result == '.'

    def test_resolve_path_with_none_workspace(self):
        """Если WORKSPACE не задан, бросает RuntimeError"""
        workspace.WORKSPACE = None
        with pytest.raises(RuntimeError):
            resolve_path('file.txt')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])