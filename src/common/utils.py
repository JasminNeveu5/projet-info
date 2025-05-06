import csv

def read_csv(filepath):
    """
    Reads a CSV file and returns its contents as a list of dictionaries. Each dictionary
    represents a row in the CSV, using the header row for keys and subsequent rows as values.
    Properly handles quoted fields that may contain commas.

    :param filepath: The path to the CSV file to read.
    :type filepath: str
    :return: A list of dictionaries where each dictionary corresponds to a row in the CSV file.
    :rtype: list[dict[str, str]]
    :raises ValueError: If a row contains too many or too few values compared to the header.
    """
    result = []
    with open(filepath, "r", encoding="utf-8") as f:
        # Create a CSV reader that handles quoted fields properly
        csv_reader = csv.reader(f, quotechar='"', delimiter=',', 
                               quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
        
        # Read header
        try:
            header = next(csv_reader)
        except StopIteration:
            return []
        
        # Process rows
        for line_num, row in enumerate(csv_reader, 2):  # Start at 2 for line numbers (header is line 1)
            if len(row) != len(header):
                raise ValueError(
                    f"Row {line_num} has an incorrect number of values. "
                    f"Expected {len(header)}, got {len(row)}."
                )
            
            result.append(dict(zip(header, row)))
            
    return result


def merge(table1, table2, key):
    """
    Merges two lists of dictionaries based on a shared key. This function assumes that the key column
    exists in both tables and that the values of the key in table2 are unique. The merged output consists
    of dictionaries with data combined from both input tables, where the key matches.

    :param table1: First table to merge. It should be a list of dictionaries where each dictionary
        represents a row of data.
    :param table2: Second table to merge. It should be a list of dictionaries where each dictionary
        represents a row of data. The key column in these dictionaries should have unique values.
    :param key: The key on which the tables should be joined. This should be a string that refers
        to the column name shared by both tables.
    :return: A list of dictionaries representing the merged output of table1 and table2. Each dictionary
        combines data from both tables where the key matches.
    """
    table2_dict = {row[key]: row for row in table2}

    merged_table = []

    for row in table1:
        key_value = row.get(key)
        if key_value in table2_dict:
            merged_row = {**row, **table2_dict[key_value]}
            merged_table.append(merged_row)

    return merged_table


def human_readable_formatter(milliseconds):
    """
    Converts milliseconds into a human-readable format (e.g., minutes:seconds.milliseconds).
    """
    seconds, ms = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02}.{ms:03}"


# Fonction utilitaire pour fusionner deux listes de dictionnaires par une clé
def merge_dicts(left, right, key):
    """
    Merges two lists of dictionaries based on a specified key. For each dictionary
    in the `left` list, it attempts to find a matching dictionary in the `right`
    list using the provided key. If a match is found, the two dictionaries are
    merged with the contents from the `right` dictionary overriding or extending
    those of the `left` dictionary. The result is a new list containing the merged
    dictionaries where matches were found.

    :param left: List of dictionaries to be merged with the `right` list.
    :type left: list[dict]
    :param right: List of dictionaries used to find matches and for merging into
                  the `left` dictionaries.
    :type right: list[dict]
    :param key: The key to be used for matching dictionaries in the `left` and
                `right` lists. Matches occur if the value for this key is the same
                in both dictionaries.
    :type key: str
    :return: A list of dictionaries resulting from merging matching dictionaries
             from the `left` and `right` lists based on the specified key.
    :rtype: list[dict]
    """
    right_lookup = {item[key]: item for item in right}
    return [
        {**item, **right_lookup[item[key]]}
        for item in left
        if item[key] in right_lookup
    ]


def time_to_seconds(time_str):
    """
    Converts a time string in the format "MM:SS.sss" into total seconds as a float.

    The function handles time strings with minutes, seconds, and milliseconds,
    e.g., "01:23.456", and converts them to their equivalent in seconds.
    Malformed or missing time strings will result in None being returned.
    Empty or invalid strings (e.g., "\\N", empty, or wrong format)
    are considered unacceptable inputs and will lead to None as an output.

    :param time_str: A string representation of the time in the format "MM:SS.sss".
    :type time_str: str
    :return: Total time in seconds as a float if conversion is successful, otherwise None.
    :rtype: float | None
    """
    if not time_str or time_str in ("\\N", ""):
        return None
    try:
        minutes, seconds = time_str.split(":")
        seconds, milliseconds = seconds.split(".")
        total_seconds = int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
        return total_seconds
    except ValueError:
        return None


if __name__ == "__main__":
    print(read_csv("/home/victor/Documents/projet-info/data/drivers.csv"))