from typing import List
import csv
import io

Filename = 'export.csv'


def make(data: List[dict]) -> str:
    with io.StringIO() as csvfile:
        fieldnames = data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return csvfile.getvalue()

