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
    "Food": "2Bruder|Groente Fruit|Food|Pindakaaswinkel|Too Good To Go|Bakker Bart|Chocolaterie|van Heeswijk Eersel|Patisserie|Xaris Lunet Zorg|Sodexo|BIERENS VOF GEBAK|Miss Bettie|Jan Linders|Mitra|Bakkerij|^AH |Albert Heijn|Jumbo|Lidl|Aldi|Sligro|Ekoplaza|Hema|IZMIR|Ozturk|NETTORAMA|TooGoodToGo|VieCuri|Maxima MC|Rudolf Vermeulen|De Genneper Hoeve|SumUp|Tonys Chocolonely|INTERMARCHE",
    "Non-food": "Dragon Tattoo|Van alles en meer|Secrid|Holland.*Barrett|Perry Sport|Zalando|Interoffice|Intersport|De Paskamer|Etos|Intelbazaar|Schoen|Travelbags|Hunkemoeller|Smartphonehoesjes|YourSurprise|Coolblue|Stichting Kringloo|Dikke Mik|HORNBACH|PANDORA|ONLY |ZEEMAN|Timco|clothing|Clay And Glow|Costes Eindhoven|MINISO|Parfumerie|Cosmetics|Xenos|Fashion|STRADIVARIUS|Decathlon|Bijenkorf|Bistro|Wibra|PRIMARK|vanHaren|Jewellery|Kadoshop|Planten|Bever|The Sting|Action|Kruidvat|RitualsCosmetics|Praxis|IKEA|Amazon|bol\.*com|Bershka|Bruna|Tochgoedkoopnl|^CA|^HM|Hennes .*Mauritz|Pull.*Bear|Amsterdam SAL FO|Lucardi|Favoloso|Nelson|New York Finest shirts|Muco Amsterdam|Bloemerie|Wehkamp",
    "Hobby": "Boekhandel|Waterstones|Paagman|Keyboardcentrum|Zingende Snaar|STRIPSPECIALIST|Techniparts|Goed Gemerkt|TinyTronics|Onlinekabelshop|123 3D|123accu|Otronic|Opencircuit|Mouser Electronic|HOD Electronics|Conrad|Eleshop|Reichelt|RECORD SHOP",
    "Tikkie": "Tikkie|Betaalverzoek",
    "Auto": "Auto|parking|Verkeersboetes|Tankstation|Q8 AIRE|^OK |Esso|TotalEnergies|Total |P Centrum Breda|EXPRTILBURG|KEIZ3320|TMCP|GARAGE VAN OOL|Shell|TINQ|^BP|TAMOIL|abonnementsgelden ANWB|KAMPEN ASSURANTIE|VKG VERZEKERINGEN|MijnAutoOnderdelen|Interparking|ParkBee|Q-Park|QPark|79-KDL-1",
    "Fiets": "Tweewieler|fiets",
    "Huisdieren": "Pierre Beelen|VDierenspeciaalzaak|Dierenkliniek|Verhuisdieren|Doornakker EINDHOVEN",
    "Woning": "BRABANT WATER NV|Gemeente Waalre|hypotheek|van Hest|Gwenny",
    "Inboedel": "Meubella|Planten|Praxis|Matt Sleeps|ABC Webshop|Vloerglijders\.nl|groenovatie|Tuincentrum|Intratuin|TuincentrCoppelmans|Pimpernelzorgkw|vijver|Randijk Bamboe|VenetaBV|boom kappen",
    "Zorg": "Zilveren Kruis|Infomedics|Apotheek|Al Dente|Pearle|R.A. van Hek|Specsavers",
    "Verzekeringen overig": "FBTO|REAAL",
    "Gas-water-licht": "ANWB Energie|^Vandebron|Waterschap de Dommel",
    "Abonnementen": "Piano|PLINQ|DPG MEDIA|Simyo|MICROSOFT|Kosten OranjePakket|Kosten tweede rekeninghouder",
    "Studie": "Stichting Eindhovens Christelijk Vo|Lara Baltessen Omschrijving: Collegegeld|Stichting Avans Omschrijving: Collegegeld|Van.*Dijk",
    "Zakgeld/gift": "kleedgeld|studiegeld|zakgeld|Theoriecentrum|Rijschool",
    "Kinderbijslag": "KINDERBIJSLAG|VOORSCHOT KIT/Kgb",
    "Belasting correctie": "Belastingdienst Apeldoorn|BELASTINGDIENST Omschrijving: 0147312312606013",
    "Vakantie-uitjes": "Viv.*s.*Kitchen|MENEER DE BOER|PULLENS HELVOIRT|Gamified|VENLO|MAASTRICHT|Arcen|GRUBBENVORST|MENNEKE ETEN|ChinInd SingAn|HistOpenluchtmuseum|QUEPASA|CCVT Bello|ZTLMaasakkersHoving|CCVQUEEN|ROMA ITA|Tiqets|AIRPORT|STARBUCKS|THE HAPPINESS CAF|Trafalgar Pub|DTGM standhouders via Stichting GoCredible|SUPER U|STATION U|PIACENZA|Cupola Basilica|SAIS SNACK|BAUME|DIJON|BRICO MARCH|KIABI DOLE|CIAMPINO|39ORGELET|39CLAIRVAUX|FOURNIL DE MANON|BELLECIN|FONTAINE|VALENCE|MERCANTINE|RUOMS|LABEAUME|BARJAC|BALAZUC|DAGNEUX|ST RAMBERT|BIJOUX 34PALAVAS|VALLON PONT|ARDECHE|CCVCarrousel|Het Rondje SGRAVENHAGE|Otravo BV|TAPO TAPONAS|BELLAS ICE|IJssalo|Strandtent|Mc.*Donald|IKEK|bar exploitat|CCVCB Leisure|Waldhoorn BV OTTERLO|theater|Happy Italy|De oude telefooncentra|HappyFood|Locomotion Diner|SOS Sport en Events|Lattes.*Literature|Restaurant|RISTORANTE|Friet|Quan Nguyen|La Providence|SEPt Oude Wandelpark|Efteling|Dunkin|BROWNIES EN DOWNIE|Rest.*Zoet.*Zout|Strandpaviljoen|Brasserie|BIKMIK MARKT|Afghani|HEZEMANS|PAYMagieMaastricht|At the Movies|ZettleMaasakkersHov|ECOLONIE|Koala Express|BROOD2DAY|Brandweerkantin|Horeca|Pathe|Ijsselhallen|Chidoz|LOODS 61|SMAAKVOL|Bedrijfsrest|Sauna|Cafe|Next Nature Network|A'DAM Six Senses|Sherlocked|Bowling|Plein 4|IJsco Fantastico|De Vooruitgang|Avocado Show|Time4t|Hotel|tourist|Stayokay|Conscious Westerpark|Moon AMSTERDAM|Majestic Amsterdam|Spa Sense|Subway|The Happiness Kitchen|Fifth NRE|CCVSancy Tres|waterreus|t Goude Hooft|Belicio Cheats|Soil Of Amsterdam|Kottmann en AMSTERDAM|alpenpark|Snowworld|Outside Escape|TicketCounter|Cafetaria|STATION OUTDOOR RETIE|INCASSO CREDITCARD|Huttopia|Roompot|Parkhoeve de Middelt|CCVBar Potential|CAMP BEAUREGARD|A J M de Bruijn|Bolier|Erik|Paasen|Venbrux|AGG JANSSEN|Saskia",
    "Giften": "Greenpeace|Stichting Universiteitsf|Mantelzorgelijk|Rop",
    "Pinnen": "Geldmaat|RABO SALLAND",
    "Onbekend": "Bayeuxlaan|Payments via Adyen|CCVErgon|Verkadef|Butlaroo Services|CCVKroonenberg|CCVElektrotech Studie|BRAINPTBackWERK|PARK7520|CCVBP|NEUAIRserv|Kuipers DEVENTER|BOERSMA APELDOORN|^STG MOLLIE PAYMENTS|BOMA4610|Global Collect|PPRO PAYMENT|TMCPVALKENSWAARD|Pin Pont",
}

rows_to_ignore = "Woonwenz|Philips|ING Bank|Fontys|Annakloos|Stichting Bitva|BTC Direct Euro|Medipoint|Hockey|Maaltijdservice|Overboeking|Bakx|L\.H\. Baltessen"

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

# Exclude rows matching the regular expression in rows_to_ignore
for column_name in columns_to_check:
    unhandled_rows_df = unhandled_rows_df[~unhandled_rows_df[column_name].str.contains(rows_to_ignore, case=False, regex=True)]

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