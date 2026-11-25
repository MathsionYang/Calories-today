#!/usr/bin/env python3
"""内联宣传页截图，生成可直接部署的独立 index.html。"""
import base64
import pathlib
import re

HERE = pathlib.Path(__file__).parent
SRC = HERE / "src.html"
OUT = HERE / "index.html"
PHOTO = HERE.parent / "Photo"


def inline(match: re.Match) -> str:
    name, extension = match.group(1), match.group(2)
    data = base64.b64encode((PHOTO / f"{name}.{extension}").read_bytes()).decode()
    mime_type = "image/png" if extension == "png" else "image/jpeg"
    return f'src="data:{mime_type};base64,{data}"'


html = SRC.read_text(encoding="utf-8")
html = re.sub(r'src="Photo/(mock-\d{2}-[\w-]+)\.(png|jpeg)"', inline, html)
assert "Photo/" not in html, "还有未内联的图片引用"
OUT.write_text(html, encoding="utf-8")
print(f"built {OUT.name}  {len(html) // 1024} KB")
