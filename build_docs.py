from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

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
    subprocess.run(["make", "docs-build"], check=True)  # noqa: S603 S607

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir.joinpath(".nojekyll").touch(exist_ok=True)
    output_dir.joinpath("index.html").write_text(REDIRECT_TEMPLATE.format(target="latest"))

    docs_src_path = Path("Doc/build/html")
    shutil.copytree(docs_src_path, output_dir / "latest", dirs_exist_ok=True)


if __name__ == "__main__":
    build("docs-build")
