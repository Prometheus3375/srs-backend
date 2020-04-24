from typing import List
import csv
import io
import re

Filename = 'export.csv'
_re_spaces = re.compile(r'\s+')


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


def make(itemlist: List[dict]) -> str:
    # set newline to None to make newlines are written as \n on all platforms
    with io.StringIO() as csvfile:
        fieldnames = set().union(*(obj.keys() for obj in itemlist))
        fieldnames = sorted(fieldnames)
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

        writer.writeheader()
        for obj in itemlist:
            for key, value in obj.items():
                if value is None:
                    value = ''
                elif isinstance(value, list):
                    vals = []
                    for v in value:
                        v = replace(str(v), _re_spaces, ' ').strip()
                        if v: vals.append(v)
                    value = '\n'.join(vals)
                else:
                    value = replace(str(value), _re_spaces, ' ').strip()
                obj[key] = value
            writer.writerow(obj)
        return csvfile.getvalue()
