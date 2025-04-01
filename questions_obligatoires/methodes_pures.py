import os

# Helper function to read and parse CSVs manually
def read_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        header = lines[0].strip().split(",")
        return [dict(zip(header, line.strip().split(","))) for line in lines[1:]]
