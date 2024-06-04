from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
import os

REDIRECT_TEMPLATE = """
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <title>Page Redirection</title>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0; url={target}">
        <script type="text/javascript">window.location.href = "{target}"</script>
    </head>
    <body>
        You are being redirected. If this does not work, click <a href='{target}'>this link</a>
    </body>
</html>
"""


def build(output_dir: str) -> None:
    doc_path = Path("Doc")
    if not doc_path.is_dir():
        raise FileNotFoundError(f"{doc_path} directory not found")

    original_cwd = Path.cwd()
    os.chdir(doc_path)

    try:
        result = subprocess.run(["make", "html"], check=True, capture_output=True, text=True)  # noqa: S603 S607
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error running make command:", e.stderr)
        raise
    finally:
        os.chdir(original_cwd)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir.joinpath(".nojekyll").touch(exist_ok=True)
    output_dir.joinpath("index.html").write_text(REDIRECT_TEMPLATE.format(target="latest"))

    docs_src_path = Path("Doc/build/html")
    if not docs_src_path.is_dir():
        raise FileNotFoundError(f"{docs_src_path} directory not found")

    shutil.copytree(docs_src_path, output_dir / "latest", dirs_exist_ok=True)


if __name__ == "__main__":
    build("docs-build")
