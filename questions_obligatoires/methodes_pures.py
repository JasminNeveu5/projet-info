import csv


def read_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        header = lines[0].strip().split(",")
        return [dict(zip(header, line.strip().split(","))) for line in lines[1:]]


def merge(table1, table2, key):
    table2_dict = {row[key]: row for row in table2}

    merged_table = []

    for row in table1:
        key_value = row.get(key)
        if key_value in table2_dict:
            merged_row = {**row, **table2_dict[key_value]}
            merged_table.append(merged_row)

    return merged_table


def left_join1(left_csv, right_csv, key_column):
    # Read the right CSV file and store its content in a dictionary
    right_dict = csv.DictReader(right_csv)

    # Read the left CSV file and perform the left join
    result = []

    left_reader = csv.DictReader(left_csv)

    for left_row in left_reader:
        key = left_row[key_column]
        # If a matching key exists in the right dictionary, join the row
        if key in right_dict:
            # Merge the left and right rows (dictionary)
            result.append({**left_row, **right_dict[key]})
        else:
            # If no match, keep left row and fill right side with empty values
            result.append({**left_row, **{k: '' for k in right_dict.get(key, {}).keys()}})

    return result  # Returns a list of dictionaries representing the joined result


def left_join(left_csv_path, right_csv_path, key_column):
    # Read the right CSV file and store its content in a dictionary
    right_dict = {}
    with open(right_csv_path, mode='r') as right_file:
        right_reader = csv.DictReader(right_file)
        for row in right_reader:
            key = row[key_column]
            right_dict[key] = row

    # Read the left CSV file and perform the left join
    result = []
    with open(left_csv_path, mode='r') as left_file:
        left_reader = csv.DictReader(left_file)
        for left_row in left_reader:
            key = left_row[key_column]
            # If a matching key exists in the right dictionary, join the row
            if key in right_dict:
                # Merge the left and right rows (dictionary)
                result.append({**left_row, **right_dict[key]})
            else:
                # If no match, keep left row and fill right side with empty values
                result.append({**left_row, **{k: '' for k in right_dict.get(key, {}).keys()}})

    return result  # Returns a list of dictionaries representing the joined result
