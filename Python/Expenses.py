import pandas as pd

# Read the CSV file with ";" separator and "," as decimal point
df = pd.read_csv(r'C:\Users\reneb\Downloads\expenses.csv', sep=";", decimal=",")

categories = {"eten", "luxe artikelen"}

# Define the rows to select
rows_to_select = {
    "TINQ": {"category": "eten", "string": "TINQ"},
    "AH": {"category" : "eten", "string": "AH"}
}

# Initialize selected_rows to empty DataFrames for each row_name
category_rows = {category: pd.DataFrame() for category in categories}

# Filter the rows and compute the total amounts
for row_name, row_data in rows_to_select.items():
    category_rows[row_data["category"]] = pd.concat([category_rows[row_data["category"]], df[df["Naam / Omschrijving"].str.contains(row_data["string"], case=False)]])


# Initialize total_amounts to zero for each row_name
total_amounts = {category: 0 for category in categories}
# Calculate total_amounts and print the selected rows and total amounts
for row_name in categories:
    category_df = category_rows[row_name]
    if not category_df.empty:
        total_amounts[row_name] = category_rows[row_name]["Bedrag (EUR)"].astype(float).sum()
        print(f"Total amount for {row_name}: €{total_amounts[row_name]:.2f}")
        print()
    
# Compute the unselected rows and count their amount
selected_indexes = pd.Index([])
for row_name, row_data in category_rows.items():
    selected_indexes = selected_indexes.union(row_data.index)
unselected_rows = df.drop(selected_indexes)
num_unselected_rows = len(unselected_rows)

# Print the unselected rows and their count
print(f"Number of unselected rows: {num_unselected_rows}")
print("Unselected rows:")
print(unselected_rows)