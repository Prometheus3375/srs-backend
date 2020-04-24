import re


def replace(text: str, pattern: re, repl: str) -> str:
    it = re.finditer(pattern, text)
    out = ''
    i = 0
    for m in it:
        start = m.start()
        out += text[i:start] + repl
        i = m.end()
    if i < len(text):
        out += text[i:]
    return out
