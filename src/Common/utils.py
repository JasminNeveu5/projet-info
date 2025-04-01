def read_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        header = lines[0].strip().split(",")
        return [dict(zip(header, line.strip().split(",")))
                for line in lines[1:]]


def merge(table1, table2, key):
    table2_dict = {row[key]: row for row in table2}

    merged_table = []

    for row in table1:
        key_value = row.get(key)
        if key_value in table2_dict:
            merged_row = {**row, **table2_dict[key_value]}
            merged_table.append(merged_row)

    return merged_table


def convert_to_human_readable(milliseconds):
    minutes = milliseconds // 60000
    seconds = (milliseconds % 60000) // 1000
    return f"{minutes}m {seconds}s"


def human_readable_formatter(x,pos):
    return convert_to_human_readable(int(x))
