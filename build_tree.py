from pathlib import Path
from tree_format import format_tree

SKIP = {
    'venv', '.venv',
    '__pycache__',
    '.git', '.pytest_cache', '.mypy_cache',
    'node_modules', 'build_tree.py'
}

def build_tree(path: Path):
    def _children(p: Path):
        if not p.is_dir():
            return []
        try:
            kids = [c for c in p.iterdir()
                    if c.name not in SKIP and not c.name.startswith('.')]
            return sorted(kids)
        except PermissionError:
            return []

    def _name(p: Path):
        return p.name + ('/' if p.is_dir() else '')

    return format_tree(node=path, format_node=_name, get_children=_children)

print(build_tree(Path('.')))