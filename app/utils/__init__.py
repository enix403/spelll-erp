import pathlib

__BASE_DIR = pathlib.Path(__file__).parent.parent.parent

def resolve_root(relpath: str='.') -> str:
    """
    Resolves a relative path relative to the project root
    """
    abspath = __BASE_DIR / relpath
    return str(abspath.resolve())


def to_int(num, default = 0) -> int:
    try:
        return int(num)
    except:
        return default
