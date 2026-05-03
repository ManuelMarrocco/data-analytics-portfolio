# ======================================================
# CO2 EMISSIONS ANALYSIS
# ======================================================
# Obiettivo:
# 1. Pulire il dataset
# 2. Verificare la qualità dei dati
# 3. Identificare i principali emettitori
# 4. Analizzare il trend delle emissioni per paese
# ======================================================


# ================================
# 1. LIBRERIE
# ================================

import pandas as pd
import numpy as np

# ================================
# 2. CONFIGURAZIONE OUTPUT
# ================================

pd.set_option("display.max_columns", None)
pd.options.display.float_format = "{:,.2f}".format

# ================================
# 3. CARICAMENTO DATASET
# ================================

df = pd.read_csv(
    "Co2_EDA - CO2 (kt) RAW DATA.csv",
    decimal=","
)

print("\nDataset preview")
print(df.head())

print("\nDataset shape")
print(df.shape)

print("\nDataset structure")
print(df.info())

# ================================
# 4. DATA QUALITY CHECK
# ================================

print("\nMissing values per column")
print(df.isnull().sum())

# ================================
# 5. DATA CLEANING
# ================================

# rimozione colonna vuota generata dallo spreadsheet
df = df.drop(columns=["Unnamed: 29"])

# rimozione riga di controllo creata nello spreadsheet
df = df[df["Country Name"] != "tot anno Mondiale"]

print("\nColumns after cleaning")
print(df.columns)

# ================================================================
# 6. DATA TRANSFORMATION
# WIDE → LONG (passaggio solo didattico, ai fini del lavoro svolto
# e' un passaggio inutile)
# ================================================================

df_long = df.melt(
    id_vars=[
        "Country Name",
        "Country Code",
        "Indicator Name",
        "Indicator Code"
    ],
    var_name="Year",
    value_name="CO2"
)

# ================================
# 7. DATA INTEGRITY CHECK
# ogni paese deve avere 25 anni
# ================================

years_check = df_long.groupby("Country Name").size()

print("\nCountries with missing years")
print(years_check[years_check != 25])

# ================================
# 8. DATA TYPE CORRECTION
# ================================

df_long["Year"] = df_long["Year"].astype(int)

# rimozione colonne non utili
df_long = df_long.drop(columns=[
    "Indicator Name",
    "Indicator Code"
])

print("\nClean dataset preview")
print(df_long.head())

print("\nDataset structure after cleaning")
print(df_long.info())

# elimninare il limite di visualizzazione dati delle righe del dataset
pd.set_option("display.max_rows", None)

# ================================
# 9. ANALYSIS 1
# TOP EMITTER COUNTRIES
# ================================

top_emitters = (
    df_long
    .groupby("Country Name")["CO2"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 20 CO2 emitters (1987–2011)")
print(top_emitters.head(20))

# ================================
# 10. ANALYSIS 2
# EMISSION TREND PER COUNTRY
# (linear regression slope)
# ================================

slopes = (
    df_long
    .groupby("Country Name")
    .apply(lambda g: np.polyfit(g["Year"], g["CO2"], 1)[0])
)

# ======================================
# 11. PRINT ANALYSIS
# stampare gli out put delle classifiche
# richieste, seguendo le indicazioni
# della mail di risposta
# ======================================

slopes_sorted = slopes.sort_values(ascending=False)

print("\nCountries with emission growth")
print(slopes_sorted.head(10))

print("\nCountries with emission reduction")
print(slopes_sorted.tail(10))

print("\nCountries with stable emissions")
zero = slopes[(slopes >= 0) & (slopes < 1)]
pos = slopes[slopes >= 1].sort_values().head(4)
neg = slopes[slopes < 0].sort_values(ascending=False).head(4)
stable = pd.concat([pos, zero, neg]).sort_values(ascending=False)
print(stable)

# =============================
# 12. SAVE TABLES
# Salvare le tabelle in csv per
# Data Visualization
# =============================

top_emitters.head(20).to_csv("top_emitters.csv", float_format="%.2f")
slopes.head(10).to_csv('Countries with emission growth'.replace(' ', '_') + '.csv', float_format="%.2f")
slopes.tail(10).to_csv('Countries with emission reduction'.replace(' ', '_') + '.csv', float_format="%.2f")
stable.to_csv('Countries with stabel_emission'.replace(' ', '_') + '.csv', float_format="%.2f")

stable_emissions = top_emitters.loc[stable.index]
print(stable_emissions.head(10))
stable_emissions.to_csv('Countries with stabel_emission CO2'.replace(' ', '_') + '.csv', float_format="%.2f")

top10 = top_emitters.head(10).index
df_long_top10 = df_long[df_long["Country Name"].isin(top10)]
df_long_top10.to_csv("co2_trend_top10.csv", index=False)

check = (
    df_long[df_long["Country Name"]=="Japan"]
    .sort_values("Year")[["Year","CO2"]]
)
print(check)
print("Sum 1987–2011:", check["CO2"].sum())

# # versione alternativa
#
# # ======================================
# # FUNZIONE: CARICAMENTO DATI
# # ======================================
#
# def load_data(path):
#     df = pd.read_csv(path, decimal=",")
#     return df
#
#
# # ======================================
# # FUNZIONE: DATA CLEANING
# # ======================================
#
# def clean_data(df):
#
#     # rimozione colonna inutile
#     df = df.drop(columns=["Unnamed: 29"])
#
#     # rimozione riga totale creata nello spreadsheet
#     df = df[df["Country Name"] != "tot anno Mondiale"]
#
#     return df
#
#
# # ======================================
# # FUNZIONE: TRASFORMAZIONE WIDE → LONG
# # ======================================
#
# def transform_data(df):
#
#     df_long = df.melt(
#         id_vars=[
#             "Country Name",
#             "Country Code",
#             "Indicator Name",
#             "Indicator Code"
#         ],
#         var_name="Year",
#         value_name="CO2"
#     )
#
#     df_long["Year"] = df_long["Year"].astype(int)
#
#     df_long = df_long.drop(columns=[
#         "Indicator Name",
#         "Indicator Code"
#     ])
#
#     return df_long
#
#
# # ======================================
# # FUNZIONE: TOP EMITTERS
# # ======================================
#
# def get_top_emitters(df_long):
#
#     return (
#         df_long
#         .groupby("Country Name")["CO2"]
#         .sum()
#         .sort_values(ascending=False)
#         .head(20)
#     )
#
#
# # ======================================
# # FUNZIONE: TREND ANALYSIS
# # ======================================
#
# def compute_trend(df_long):
#
#     slopes = (
#         df_long
#         .groupby("Country Name")
#         .apply(lambda g: np.polyfit(g["Year"], g["CO2"], 1)[0])
#         .sort_values(ascending=False)
#     )
#
#     return slopes
#
#
# # ======================================
# # MAIN ANALYSIS
# # ======================================
#
# df = load_data("Co2_EDA - CO2 (kt) RAW DATA.csv")
#
# df = clean_data(df)
#
# df_long = transform_data(df)
#
# top_emitters = get_top_emitters(df_long)
#
# slopes = compute_trend(df_long)
#
# print("\nTop 20 emitters")
# print(top_emitters)
#
# print("\nStrongest growth")
# print(slopes.head(20))
#
# print("\nStrongest reductions")
# print(slopes.tail(20))
