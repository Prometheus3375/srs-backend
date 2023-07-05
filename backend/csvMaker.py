import csv
import io
from typing import Dict, List, Union

Filename = 'export.csv'


def make(itemlist: List[Dict[str, Union[str, List[str]]]]) -> str:
    with io.StringIO(newline = None) as csvfile:
        fieldnames = set().union(*(obj.keys() for obj in itemlist))
        fieldnames = sorted(fieldnames)
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

        writer.writeheader()
        for obj in itemlist:
            obj = obj.copy()
            for key, value in obj:
                if isinstance(value, list):
                    obj[key] = '\n'.join(value)
            writer.writerow(obj)
        return csvfile.getvalue()
