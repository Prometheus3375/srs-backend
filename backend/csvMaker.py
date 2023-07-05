from typing import List
import csv
import io

Filename = 'export.csv'


def make(data: List[dict]) -> str:
    # set newline to None to make newlines are written as \n on all platforms
    with io.StringIO() as csvfile:
        fieldnames = set().union(*(d.keys() for d in data))
        fieldnames = sorted(fieldnames)
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return csvfile.getvalue()
