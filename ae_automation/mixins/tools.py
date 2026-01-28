from __future__ import annotations

import subprocess
from slugify import slugify
from PIL import ImageColor
import webbrowser
import tempfile
import os

class ToolsMixin:
    """
    ToolsMixin
    """

    def process_exists(self, process_name: str) -> bool:
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        # use buildin check_output right away
        output = subprocess.check_output(call).decode()
        # check in last line for process name
        last_line = output.strip().split('\r\n')[-1]
        # because Fail message could be translated
        return last_line.lower().startswith(process_name.lower())

    def file_get_contents(self, filename: str) -> str:
        #Convert filename to absolute path
        filename = os.path.abspath(filename)
        with open(filename, encoding='utf-8') as f:
            return f.read()

    def slug(self, _str: str) -> str:
        return slugify(str(_str).lower())

    def hexToRGBA(self, hex: str) -> str:
        _h=ImageColor.getcolor(hex, "RGB")
        #return str(_h[0])
        return str(_h[0]/255)+","+str(_h[1]/255)+","+str(_h[2]/255)+",1"

    def previewLogs(self, logs: str) -> None:
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.txt',encoding="utf-8") as f:
            urlFile = 'file://' + f.name
            f.write(logs)
        webbrowser.open(urlFile)
