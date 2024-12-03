from functools import lru_cache

from needle import STATIC_PATH


@lru_cache(maxsize=128)
def load_css(filename: str) -> str:
    """
    Load the CSS file from the static folder

    Args:
    ----
        filename (str): CSS filename

    Returns:
    -------
        str: CSS content

    """
    path = STATIC_PATH / "css" / f"{filename}.css"

    if not path.exists():
        raise FileNotFoundError(f"CSS file not found: '{path}'")

    return path.read_text()


@lru_cache(maxsize=128)
def load_html(filename: str) -> str:
    """
    Load the HTML file from the static folder

    Args:
    ----
        filename (str): HTML filename

    Returns:
    -------
        str: HTML content

    """
    path = STATIC_PATH / "html" / f"{filename}.html"

    if not path.exists():
        raise FileNotFoundError(f"HTML file not found: '{path}'")

    return path.read_text()
