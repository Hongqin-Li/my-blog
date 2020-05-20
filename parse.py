import sys
import os
import re
import toml
import markdown
import json
from datetime import datetime

def read(path):
    with open(path, 'r') as f:
        return f.read()

def parse1(path):
    def parse_title(s):
        return re.search(r"^\s*[#]+(.*?)\n(.*)", s, flags=re.DOTALL).group(1, 2)
    def parse_header(s):
        return re.search(r"^[+]{3}(.*?)^[+]{3}\s*$(.*)", s, flags=re.DOTALL | re.MULTILINE).group(1, 2)
        

    t, md = parse_header(read(path).strip())
    title, md = parse_title(md)

    t = toml.loads(t)
    html = markdown.markdown(md, extensions=[
                              'markdown.extensions.extra',
                              'codehilite',
                            ], extension_configs={
                              'codehilite': {
                                'linenums': True,
                                # 'use_pygments': False,
                              }
                            })

    assert t["tags"] is not None

    global cnt

    mtime = datetime.fromtimestamp(os.path.getmtime(path))

    # t["date"] = mtime.date
    t["title"] = title.strip()
    t["html"] = html
    t["last_modified"] = mtime

    return t

if __name__ == "__main__":
    print(json.dumps(parse1(sys.stdin.read()), ensure_ascii=False, indent=4, sort_keys=True, default=str))

