from typing import List
import csv
import io

Filename = 'export.csv'

def get_fieldnames(data):
    return set().union(*(d.keys() for d in data))

def make(data: List[dict]) -> str:
    with io.StringIO() as csvfile:
        fieldnames = get_fieldnames(data)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return csvfile.getvalue()

