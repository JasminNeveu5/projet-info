import os
import pandas as pd
from options.config import DATA_DIR

def infer_sql_type(dtype):
    """
    Map pandas data types to SQL-compatible types.
    """
    if pd.api.types.is_integer_dtype(dtype):
        return "integer"
    elif pd.api.types.is_float_dtype(dtype):
        return "float"
    elif pd.api.types.is_bool_dtype(dtype):
        return "boolean"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "datetime"
    else:
        return "text"  # Default to text for strings or unknown types

def generate_dbml(df, table_name):
    """
    Generate DBML content from a pandas DataFrame.
    """
    dbml_content = f"Table {table_name} {{\n"
    for column in df.columns:
        sql_type = infer_sql_type(df[column].dtype)
        dbml_content += f"  {column} {sql_type} [note: \"\"]\n"
    dbml_content += "}\n"
    return dbml_content

# Iterate over all CSV files in the DATA_DIR folder
csv_folder_path = f"{DATA_DIR}"
dbml_output_folder = f"{DATA_DIR}/dbml_output"

# Ensure the output folder exists
os.makedirs(dbml_output_folder, exist_ok=True)

for file_name in os.listdir(csv_folder_path):
    if file_name.endswith(".csv"):
        # Read the CSV file
        csv_file_path = os.path.join(csv_folder_path, file_name)
        df = pd.read_csv(csv_file_path)

        # Generate DBML content
        table_name = os.path.splitext(file_name)[0]  # Use the file name (without extension) as the table name
        dbml_content = generate_dbml(df, table_name)

        # Write to a DBML file
        dbml_file_path = os.path.join(dbml_output_folder, f"{table_name}.dbml")
        with open(dbml_file_path, "w") as dbml_file:
            dbml_file.write(dbml_content)

        print(f"DBML file generated: {dbml_file_path}")




# Path to the folder containing DBML files
dbml_output_folder = f"{DATA_DIR}/dbml_output"
final_dbml_file_path = os.path.join(dbml_output_folder, "finale.dbml")

# Ensure the output folder exists
if not os.path.exists(dbml_output_folder):
    raise FileNotFoundError(f"The folder {dbml_output_folder} does not exist.")

# Open the final DBML file for writing
with open(final_dbml_file_path, "w") as final_dbml_file:
    # Loop over all DBML files in the folder
    for file_name in os.listdir(dbml_output_folder):
        if file_name.endswith(".dbml"):
            dbml_file_path = os.path.join(dbml_output_folder, file_name)

            # Read the content of the current DBML file
            with open(dbml_file_path, "r") as dbml_file:
                content = dbml_file.read()

            # Write the content to the final DBML file
            final_dbml_file.write(content)
            final_dbml_file.write("\n")  # Add a newline between files for separation

print(f"Final DBML file generated: {final_dbml_file_path}")
