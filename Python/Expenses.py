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

AVERAGE_LENGTH_MONTH = 30.44

columns_to_check = ["Naam / Omschrijving", "Mededelingen"]

# Define the categories to select
categories_to_select = {
    "food": "Sodexo|BIERENS VOF GEBAK|Miss Bettie|Jan Linders|Mitra|Foodticket|Bakkerij|^AH |Albert Heijn|Jumbo|Lidl|Sligro|Ekoplaza|Hema|IZMIR|Ozturk|NETTORAMA|TooGoodToGo|VieCuri|Maxima MC|Rudolf Vermeulen|De Genneper Hoeve|SumUp|Tonys Chocolonely|INTERMARCHE|Restaurant|RISTORANTE",
    "non-food": "Patisserie|Xenos|Fashion|STRADIVARIUS|Decathlon|Bijenkorf|Bistro|Mouser Electronic|Wibra|PRIMARK|vanHaren|Jewellery|Kadoshop|Techniparts|Planten|Bever|The Sting|Action|Kruidvat|RitualsCosmetics|Praxis|IKEA|Amazon|bol\.*com|123 3D|Bershka|Bruna|Tochgoedkoopnl|^CA|^HM|Hennes .*Mauritz|Pull.*Bear|Amsterdam SAL FO|Lucardi|Favoloso|Nelson|Waterstones|New York Finest shirts|HOD Electronics|Conrad|Eleshop|Reichelt|Muco Amsterdam|Bloemerie|Wehkamp",
    "tikkie": "Tikkie|Betaalverzoek",
    "auto": "Auto|Tankstation|TotalEnergies|EXPRTILBURG|KEIZ3320|TMCPVALKENSWAARD|GARAGE VAN OOL|Shell|TINQ|^BP|TAMOIL|KAMPEN ASSURANTIE|VKG VERZEKERINGEN|MijnAutoOnderdelen|Interparking|ParkBee|Q-Park|QPark|79-KDL-1",
    "huisdieren": "Pierre Beelen|VDierenspeciaalzaak",
    "woning": "BRABANT WATER NV|Gemeente Waalre|hypotheek|van Hest",
    "inboedel": "Planten|Praxis|Matt Sleeps|ABC Webshop|Vloerglijders\.nl|groenovatie|Tuincentrum|Intratuin|vijver",
    "zorgverzekering": "Zilveren Kruis|Infomedics|Apotheek|Al Dente|Pearle",
    "verzekeringen woning": "FBTO",
    "gas-water-licht": "ANWB Energie|^Vandebron",
    "abonnementen": "Piano|PLINQ|DPG MEDIA|Simyo|MICROSOFT|Kosten OranjePakket|Kosten tweede rekeninghouder",
    "studie": "Stichting Eindhovens Christelijk Vo|Lara Baltessen Omschrijving: Collegegeld|Stichting Avans Omschrijving: Collegegeld",
    "zakgeld/gift": "kleedgeld|studiegeld|zakgeld|Theoriecentrum\.nl",
    "kinderbijslag": "KINDERBIJSLAG|VOORSCHOT KIT/Kgb",
    "vakantie-uitjes": "ECOLONIE|Koala Express|BROOD2DAY|Brandweerkantin|Horeca|Pathe|Ijsselhallen|Chidoz|LOODS 61|SMAAKVOL|Bedrijfsrest|Sauna|Cafe|Next Nature Network|A'DAM Six Senses|Sherlocked|Bowling|Plein 4|IJsco Fantastico|De Vooruitgang|Avocado Show|Time4t|Hotel|tourist|Stayokay|Conscious Westerpark|Moon AMSTERDAM|Majestic Amsterdam|Spa Sense|Subway|The Happiness Kitchen|Fifth NRE|CCVSancy Tres|waterreus|t Goude Hooft|Belicio Cheats|Soil Of Amsterdam|Kottmann en AMSTERDAM|alpenpark|Snowworld|Outside Escape|TicketCounter|Cafetaria|STATION OUTDOOR RETIE|INCASSO CREDITCARD|Huttopia|Roompot|Parkhoeve de Middelt|CCVBar Potential|CAMP BEAUREGARD|A J M de Bruijn|Bolier|Erik|Paasen|Venbrux|AGG JANSSEN|Saskia",
    "Gift": "Greenpeace|Rop",
    "Pinnen": "Geldmaat|RABO SALLAND",
    "Onbekend": "CCVBP|NEUAIRserv|Kuipers DEVENTER|BOERSMA APELDOORN|^STG MOLLIE PAYMENTS|BOMA4610|Global Collect|PPRO PAYMENT|TMCPVALKENSWAARD|Pin Pont",
}

category_to_ignore = "Woonwenz|Philips|ING Bank|STICHTING FONTYS|Annakloos|Stichting Bitva|BTC Direct Euro|Medipoint|Hockey|Bakx|L\.H\. Baltessen"

# Initialize selected_rows to empty DataFrames for each row_name
category_rows = {category_name: pd.DataFrame() for category_name, _ in categories_to_select.items()}

# Filter the rows and compute the total amounts
for category_name, regexp in categories_to_select.items():
    for column_name in columns_to_check:
        # Use copy to prevent modifying the original df, otherwise the 'SettingWithCopyWarning' can occur.
        category_df = df[df[column_name].str.contains(regexp, case=False, regex=True)].copy()
        # Get the "Bij Af" column for the selected rows
        bij_af_column = category_df["Af Bij"].apply(lambda x: 1 if x == "Af" else -1)
        # Multiply the "Bedrag (EUR)" column by the "Af Bij" column
        category_df["Bedrag (EUR)"] = bij_af_column * category_df["Bedrag (EUR)"].astype(float)
        category_rows[category_name] = pd.concat([category_rows[category_name], category_df]).drop_duplicates()

# Initialize total_amounts to zero for each row_name
total_amounts = {category: 0.0 for category, row_data in categories_to_select.items()}
# Calculate total_amounts and print the selected rows and total amounts
total_amount_all = 0.0
print("\n****************************************")
# Print the number of days between the start and end dates
print(f'Number of days between {start_date_str} and {end_date_str}: {num_days} = {num_days / AVERAGE_LENGTH_MONTH:.2f} months')
print("****************************************")
for category_name, _ in categories_to_select.items():
    category_df = category_rows[category_name]
    if not category_df.empty:
        total_amounts[category_name] = category_rows[category_name]["Bedrag (EUR)"].astype(float).sum()
        total_amount_all += total_amounts[category_name]
        print(f"Monthly amount for {category_name}: €{total_amounts[category_name] / (num_days / AVERAGE_LENGTH_MONTH):.2f}")
print(f"TOTAL PER MONTH: €{total_amount_all / (num_days / AVERAGE_LENGTH_MONTH):.2f}")
print("****************************************")
    
# Compute the unselected rows and count their amount
selected_indexes = pd.Index([])
for _, category_data in category_rows.items():
    selected_indexes = selected_indexes.union(category_data.index)
unhandled_rows_df = df.drop(selected_indexes)

# Exclude rows matching the regular expressions in categories_to_select
for _, category_data in category_rows.items():
    unhandled_rows_df = unhandled_rows_df[~unhandled_rows_df['Naam / Omschrijving'].str.contains(category_to_ignore, case=False, regex=True)]

total_unhandled_amount = 0.0
if not unhandled_rows_df.empty:
    bij_af_column = unhandled_rows_df["Af Bij"].apply(lambda x: 1 if x == "Af" else -1)
    # Multiply the "Bedrag (EUR)" column by the "Af Bij" column
    unhandled_rows_df["Bedrag (EUR)"] = bij_af_column * unhandled_rows_df["Bedrag (EUR)"].astype(float)
    total_unhandled_amount = unhandled_rows_df["Bedrag (EUR)"].astype(float).sum()

num_unhandled_rows = len(unhandled_rows_df)

# Print the unselected rows and their count
print(f"Unhandled amount per month: {total_unhandled_amount / (num_days / AVERAGE_LENGTH_MONTH):.2f}")
print(f"Number of unhandled rows: {num_unhandled_rows}")
print("****************************************")
print("Unhandled rows:")
print(unhandled_rows_df)
print("****************************************")