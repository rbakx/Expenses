import pandas as pd
from datetime import datetime

# Read the CSV file with ";" separator and "," as decimal point
df = pd.read_csv(r'C:\Users\reneb\Downloads\expenses.csv', sep=";", decimal=",")

# Extract the start and end dates from the first and last rows of the DataFrame
start_date_str = str(df.iloc[-1]['Datum'])
end_date_str = str(df.iloc[0]['Datum'])
# Convert the start and end date strings to datetime objects
start_date = datetime.strptime(start_date_str, '%Y%m%d')
end_date = datetime.strptime(end_date_str, '%Y%m%d')
# Calculate the number of days between the start and end dates
num_days = (end_date - start_date).days
# Print the number of days between the start and end dates
print(f'Number of days between {start_date_str} and {end_date_str}: {num_days}')
AVERAGE_LENGTH_MOMTH = 30.44

categories = ["food", "non-food", "inboedel", "gas-water-licht", "auto", "huisdieren", "abonnementen", "zorgverzekering"]

# Define the rows to select
rows_to_select = {
    "AH": {"category" : "food", "string": "AH"},
    "Albert Heijn": {"category" : "food", "string": "Albert Heijn"},
    "Jumbo": {"category" : "food", "string": "Jumbo"},
    "Lidl": {"category" : "food", "string": "Lidl"},
    "Sligro": {"category" : "food", "string": "Sligro"},
    "TooGoodToGo": {"category" : "food", "string": "TooGoodToGo"},
    "Ekoplaza": {"category" : "food", "string": "Ekoplaza"},
    "IZMIR": {"category" : "food", "string": "IZMIR"},
    "NETTORAMA": {"category" : "food", "string": "NETTORAMA"},
    "Action": {"category" : "non-food", "string": "Action"},
    "Kruidvat": {"category" : "non-food", "string": "Kruidvat"},
    "RitualsCosmetics": {"category" : "non-food", "string": "RitualsCosmetics"},
    "TINQ": {"category": "auto", "string": "TINQ"},
    "Pierre Beelen": {"category": "huisdieren", "string": "Pierre Beelen"},
    "Praxis": {"category": "inboedel", "string": "Praxis"},
    "Zilveren Kruis": {"category": "zorgverzekering", "string": "Zilveren Kruis"},
    "ANWB Energie": {"category": "gas-water-licht", "string": "ANWB Energie"},
    "Vandebron": {"category": "gas-water-licht", "string": "Vandebron"},
    "PLINQ": {"category": "abonnementen", "string": "PLINQ"},
}

# Initialize selected_rows to empty DataFrames for each row_name
category_rows = {category: pd.DataFrame() for category in categories}

# Filter the rows and compute the total amounts
for row_name, row_data in rows_to_select.items():
    category_df = df[df["Naam / Omschrijving"].str.startswith(row_data["string"])]
    # Get the "Bij Af" column for the selected rows
    bij_af = category_df["Af Bij"].apply(lambda x: 1 if x == "Af" else -1)
    # Multiply the "Bedrag (EUR)" column by the "Af Bij" column
    category_df["Bedrag (EUR)"] = bij_af * category_df["Bedrag (EUR)"].astype(float)
    category_rows[row_data["category"]] = pd.concat([category_rows[row_data["category"]], category_df])

# Initialize total_amounts to zero for each row_name
total_amounts = {category: 0.0 for category in categories}
# Calculate total_amounts and print the selected rows and total amounts
total_amount_all = 0.0
print("****************************************")
for row_name in categories:
    category_df = category_rows[row_name]
    if not category_df.empty:
        total_amounts[row_name] = category_rows[row_name]["Bedrag (EUR)"].astype(float).sum()
        total_amount_all += total_amounts[row_name]
        print(f"Monthly amount for {row_name}: €{total_amounts[row_name] / AVERAGE_LENGTH_MOMTH:.2f}")
print(f"TOTAL PER MONTH: €{total_amount_all / AVERAGE_LENGTH_MOMTH:.2f}")
print("****************************************")
    
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