import pandas as pd

# LA Crime Analysis 2020–2024
# Data Analyst: Manuel Marrocco
# Purpose: Analyze crime trends, geographic patterns,
# and demographic patterns for the Public Safety Department.

# 1. DATA LOADING

# loading dataset.
file_path = r"C:\Users\manue\Documents\Manuel\Data Analytics\Esercitazioni Data Analysis\2_LA_crimes\crime_data_from_2020_to_2024_v1.csv"
df = pd.read_csv(file_path)

# setting display visualization.
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.2f}'.format)

# 2. DATA EXPLORATION

# dataset size.
print(df.shape)
# (1004894 rows, 28 columns).

# Identify the variables and data types of each variable.
print(df.dtypes)

# DR_NO               int64
# Date Rptd             str
# DATE OCC              str
# TIME OCC            int64
# AREA                int64
# AREA NAME             str
# Rpt Dist No         int64
# Part 1-2            int64
# Crm Cd              int64
# Crm Cd Desc           str
# Mocodes               str
# Vict Age            int64
# Vict Sex              str
# Vict Descent          str
# Premis Cd         float64
# Premis Desc           str
# Weapon Used Cd    float64
# Weapon Desc           str
# Status                str
# Status Desc           str
# Crm Cd 1          float64
# Crm Cd 2          float64
# Crm Cd 3          float64
# Crm Cd 4          float64
# LOCATION              str
# Cross Street          str
# LAT               float64
# LON               float64

# 3. DATA QUALITY VALIDATION

# Create new datetime columns converted from the original date string columns.
df['Date Rptd DT'] = pd.to_datetime(df['Date Rptd'],
                                    format='%m/%d/%Y %I:%M:%S %p',
                                    errors='coerce')

df['DATE OCC DT'] = pd.to_datetime(df['DATE OCC'],
                                   format='%m/%d/%Y %I:%M:%S %p',
                                   errors='coerce')

# Normalize time column from int64 to timedelta in order to create a single timestamp column.
df['TIME OCC STR'] = df['TIME OCC'].astype(str).str.zfill(4)

df['TIME OCC TD'] = pd.to_timedelta(df['TIME OCC STR'].str[:2] +
                                    ':' +
                                    df['TIME OCC STR'].str[2:] + ':00')

df['Timestamp OCC DT'] = df['DATE OCC DT'] + df['TIME OCC TD']

# check time coverage of the dataset
print("Dataset time coverage:")
print("Start:", df['Timestamp OCC DT'].min())
print("End  :", df['Timestamp OCC DT'].max())
# first date: 2020-01-01 00:01:00
# last date : 2024-12-30 23:00:00

# creating copy of the original dataset for data quality validation.
crime_analysis = df[['DR_NO',
                     'Date Rptd DT',
                     'Timestamp OCC DT',
                     'AREA',
                     'AREA NAME',
                     'Rpt Dist No',
                     'Part 1-2',
                     'Crm Cd',
                     'Crm Cd Desc',
                     'Vict Age',
                     'Vict Sex',
                     'Weapon Used Cd',
                     'Weapon Desc',
                     'Status Desc',
                     'LOCATION',
                     'LAT',
                     'LON'
                     ]].copy()

# Verify that each crime incident ID is unique
duplicates_dr_no = crime_analysis[crime_analysis.duplicated(subset='DR_NO',
                                                            keep=False)]

print("Duplicate DR_NO:", len(duplicates_dr_no))
# Duplicate DR_NO: 0

# 4. DATA CLEANING

# Missing Values Check
crime_analysis.info()

#  #   Column            Non-Null Count    Dtype
# ---  ------            --------------    -----
#  0   DR_NO             1004894 non-null  int64
#  1   Date Rptd DT      1004894 non-null  datetime64[us]
#  2   Timestamp OCC DT  1004894 non-null  datetime64[us]
#  3   AREA              1004894 non-null  int64
#  4   AREA NAME         1004894 non-null  str
#  5   Rpt Dist No       1004894 non-null  int64
#  6   Part 1-2          1004894 non-null  int64
#  7   Crm Cd            1004894 non-null  int64
#  8   Crm Cd Desc       1004894 non-null  str
#  9   Vict Age          1004894 non-null  int64
#  10  Vict Sex          860263 non-null   str
#  11  Weapon Used Cd    327216 non-null   float64
#  12  Weapon Desc       327216 non-null   str
#  13  Status Desc       1004894 non-null  str
#  14  LAT               1004894 non-null  float64
#  15  LON               1004894 non-null  float64
# dtypes: datetime64[us](2), float64(3), int64(6), str(5)

# Creates a table showing, for each dataset column,
# the total number and percentage of missing values (NaN).
missing_value_table = pd.DataFrame({'Missing Values n.': crime_analysis.isnull().sum(),
                                    'Missing Value %': round(crime_analysis.isnull().mean() * 100, 2),
                                    })
print(missing_value_table.sort_values(by='Missing Values n.',
                                      ascending=False))

#                   Missing Values n.  Missing Value %
# Weapon Desc                  677678            67.44
# Weapon Used Cd               677678            67.44
# Vict Sex                     144631            14.39

# Missing values were identified in Weapon Used Cd and Weapon Desc (67.44%),
# which likely indicates incidents where no weapon was involved.
# Missing values in Vict Sex represent 14.39% of the dataset and may correspond
# to cases where victim information was unavailable or not recorded.

print(crime_analysis.describe())

#  LAT        LON        Vict Age
# 1004894.00 1004894.00  1004894.00
#      34.00    -118.09       28.92
#       0.00    -118.67       -4.00
#      34.01    -118.43        0.00
#      34.06    -118.32       30.00
#      34.16    -118.27       44.00
#      34.33       0.00      120.00
#       1.61       5.58       21.99

# Some records in the dataset contained missing geographic coordinates (LAT = 0, LON = 0).
# To address this issue, records with zero coordinates were matched with other records sharing
# the same LOCATION that contained valid latitude and longitude. The most frequent coordinate
# pair for each location was then used to replace the missing values.
# After the replacement, a validation check was performed to identify any remaining records
# with zero coordinates, which may require exclusion from geographic visualizations.

# The LOCATION field in the dataset represents street names
# or street segments rather than unique geographic points.
# As a result, the same LOCATION may appear with different
# latitude and longitude values across multiple records.
# To assess the spatial stability of LOCATION values,
# the number of distinct latitude and longitude coordinates
# associated with each LOCATION was calculated.

location_coord_check = (
    crime_analysis
    .groupby('LOCATION')[['LAT', 'LON']]
    .nunique()
)

# Identify locations associated with the highest number of
# distinct coordinates. These typically correspond to long
# streets that span multiple geographic points in the city.
print(location_coord_check.sort_values('LAT', ascending=False).head())

#                                  LAT  LON
# LOCATION
# FIGUEROA                     ST  295  156
# VERMONT                      AV  272   68
# FIGUEROA                         270  160
# BROADWAY                         254  163
# WESTERN                      AV  251   65
# MAIN                         ST  238  122
# VERMONT                          219   57
# WESTERN                          194   57
# CENTRAL                      AV  189   90
# VENICE                       BL  188  231
# HOOVER                       ST  181   33
# VENICE                           178  218
# SEPULVEDA                    BL  173  106
# 8TH                          ST  161  203
# SAN PEDRO                    ST  161   85
# 6TH                          ST  158  227
# VAN NUYS                     BL  158   97
# NORMANDIE                    AV  156   45
# VENTURA                      BL  150  163
# 3RD                          ST  148  221

# Summary statistics describing coordinate variability per LOCATION.
# For each LOCATION, the number of distinct latitude and longitude
# values is calculated and summarized using descriptive statistics.
# This helps evaluate whether a location is associated with stable
# coordinates or with multiple geographic points (e.g., long streets).
print((crime_analysis.groupby('LOCATION')[['LAT', 'LON']]
       .nunique()
       .describe()
       ))

#            LAT      LON
# count 66566.00 66566.00
# mean      2.12     2.17
# std       5.78     5.89
# min       1.00     1.00
# 25%       1.00     1.00
# 50%       1.00     1.00
# 75%       2.00     2.00
# max     295.00   231.00

# A consistency check on geographic coordinates showed that most LOCATION
# values are associated with one or two latitude–longitude pairs, indicating
# relatively stable spatial encoding. A limited number of major streets are
# linked to many coordinate pairs due to their geographic extent across the city.
# Since the majority of locations exhibit stable coordinates, using the most
# frequent latitude–longitude pair observed for each LOCATION was considered
# a reasonable approach to recover records with missing geographic values.
# Replace missing coordinates (LAT = 0, LON = 0)
# using valid coordinates from the same LOCATION
# Extract valid coordinates per LOCATION (most frequent pair)

location_coords = (
    crime_analysis[
        (crime_analysis['LAT'] != 0) & (crime_analysis['LON'] != 0)
        ]
    .groupby('LOCATION')[['LAT', 'LON']]
    .agg(lambda x: x.mode().iloc[0])
    .reset_index()
)

# Merge valid coordinates back into the dataset
crime_analysis = crime_analysis.merge(
    location_coords,
    on='LOCATION',
    how='left',
    suffixes=('', '_ref')
)

# Replace rows where coordinates are zero
crime_analysis.loc[
    (crime_analysis['LAT'] == 0) & (crime_analysis['LON'] == 0),
    ['LAT', 'LON']
] = crime_analysis.loc[
    (crime_analysis['LAT'] == 0) & (crime_analysis['LON'] == 0),
    ['LAT_ref', 'LON_ref']
].values

# Remove temporary reference columns
crime_analysis = crime_analysis.drop(columns=['LAT_ref', 'LON_ref'])

# Check remaining rows with missing coordinates
remaining_zero_coords = crime_analysis[
    (crime_analysis['LAT'] == 0) | (crime_analysis['LON'] == 0)
    ]

# every lat and lon have his value
print("Rows still containing zero coordinates:")
print(remaining_zero_coords[['AREA', 'AREA NAME', 'LOCATION', 'LAT', 'LON']])
print("Total remaining rows:", remaining_zero_coords.shape[0])

# Invalid values check for victim age
print(f'''Check age outliers:
min age recorded: {crime_analysis['Vict Age'].min()},
max age recorded: {crime_analysis['Vict Age'].max()}.
''')

# During the data quality validation phase, several anomalous values were identified
# in the Vict Age variable. Some records contain negative age values
# Vict Age Anomalous Values
#  120         1
#  0      269178
# -1         100
# -2          28
# -3           6
# -4           3
# which are not logically valid and likely represent
# data entry errors.

age_outlier = [120, 0, -1, -2, -3, -4]

print(
    crime_analysis[
        crime_analysis['Vict Age'].isin(age_outlier)
    ]['Vict Age']
    .value_counts()
    .sort_index(ascending=False)
)

age_outliers = crime_analysis[crime_analysis['Vict Age'].isin(age_outlier)]
print(age_outliers.groupby(['Vict Age',
                            'Crm Cd',
                            'Crm Cd Desc'])
      .size()
      .sort_index(ascending=False)
      )

# An extreme value of Vict Age equal to 120 was identified in a single record
# associated with the crime category "Assault with Deadly Weapon".
# Given its rarity and the presence of other data entry anomalies (negative ages),
# this value was treated as a potential outlier.

assault_deadly_weapon = crime_analysis[crime_analysis['Crm Cd'].isin([230])]
print(assault_deadly_weapon
      .groupby(['Vict Age',
                'Crm Cd',
                'Crm Cd Desc'])
      .size()
      .sort_index(ascending=False))

# Vict Age values equal to 0 are likely to represent missing or unknown information
# rather than valid age values, and should be reviewed before final treatment in the analysis.
#
# The remaining anomalous age values (−1 to −4)
# will be presented during the stakeholder update meeting
# in order to determine how they should be handled in the analysis.

# Verify Victim Sex categories are consistent
victim_sex_cat = crime_analysis['Vict Sex'].value_counts()
print(victim_sex_cat)

# Vict Sex
# M    403842 Male
# F    358553 Female
# X     97753 Unknow / Not reported
# H       114 Rare category in dataset
# -         1 apparent data entry error

# check crimes where vict sex = X
victim_sex_cat_x = crime_analysis[crime_analysis['Vict Sex'] == 'X']
print(victim_sex_cat_x
      .groupby(['Crm Cd',
                'Crm Cd Desc'])
      .size()
      .sort_values(ascending=False)
      )

# check crimes where vict sex = H
victim_sex_cat_h = crime_analysis[crime_analysis['Vict Sex'] == 'H']
print(victim_sex_cat_h
      .groupby(['Crm Cd',
                'Crm Cd Desc'])
      .size()
      .sort_values(ascending=False)
      )

# check crimes where vict sex = -
victim_sex_cat_ = crime_analysis[crime_analysis['Vict Sex'] == '-']
print(victim_sex_cat_
      .groupby(['Crm Cd',
                'Crm Cd Desc'])
      .size()
      .sort_values(ascending=False)
      )

# verify if the same crimes normally contain valid Vict Sex values
VANDALISM_FELONY = crime_analysis[crime_analysis['Crm Cd Desc'] == 'VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)']
print(VANDALISM_FELONY
      .groupby('Vict Sex')
      .size()
      )

# Result:
# '-' appears only once while the same crime category contains tens of thousands
# of records with valid Vict Sex values (M, F, X).
# This strongly suggests '-' is a data entry anomaly rather than a valid category.

# check Weapon Desc and Crm Cd Desc categories for duplicates, synonyms,
# spelling variations or inconsistent capitalization

print(crime_analysis['Weapon Desc'].value_counts().sort_index())
print(crime_analysis['Crm Cd Desc'].value_counts().sort_index())

# Result:
# No duplicates, synonyms, spelling variations, or inconsistent capitalization
# were identified in the Weapon Desc and Crm Cd Desc categories.

# Check that AREA codes correspond to a single AREA NAME.
# This validation ensures there are no inconsistencies between the numeric area code
# and the textual area name (e.g., the same AREA code linked to multiple names).
# If the result is 1 for every AREA, the mapping is consistent and safe to use
# for grouping and geographic analysis.

area_check = crime_analysis.groupby('AREA')['AREA NAME'].nunique()
print(area_check)

# AREA
# 1     1
# 2     1
# 3     1
# 4     1
# 5     1
# 6     1
# 7     1
# 8     1
# 9     1
# 10    1
# 11    1
# 12    1
# 13    1
# 14    1
# 15    1
# 16    1
# 17    1
# 18    1
# 19    1
# 20    1
# 21    1

# Data Format Validation
# Note: several of these checks were already implicitly verified during the
# data preparation phase when converting and structuring the dataset.
# 1. Verify date columns follow a consistent format
# Date Rptd DT and Timestamp OCC DT were converted to datetime format during preprocessing.
# 2. Confirm numeric fields are stored as numbers
# Numeric variables are stored as int64 or float64 as confirmed during dataset inspection.
# 3. Confirm categorical variables are stored as text categories
# Categorical variables are stored as string values.
# 4. Check that geographic identifiers (AREA / AREA NAME) are aligned
# Each AREA code corresponds to a single AREA NAME; no inconsistencies were detected.

# Data Cleaning Plan (stakeholder email resume about anomalous values):
# Variable	    Issue				    Treatment Rule
# Vict Age		Values −1, −2, −3, −4	Treat as missing (unknown age)
# Vict Age		Value = 0		        Treat as missing (unknown age)
# Vict Age		Value = 120		        Retain as valid outlier; flag in documentation
# Vict Sex		Value = X		        Treat as Unknown / Not reported
# Vict Sex		Value = H		        Recode as Unknown
# Vict Sex		Value = "-"		        Treat as data entry error and recode as Unknown

# recode anomalous Vict Sex values (X, H, "-") into a single Unknown category (X)
crime_analysis['Vict Sex'] = crime_analysis['Vict Sex'].replace(['H',
                                                                 '-'], 'X')
# Vict Sex before modification
# M    403842 Male
# F    358553 Female
# X     97753 Unknown / Not reported
# H       114 Rare category in dataset
# -         1 apparent data entry error

# Vict Sex after modification
# F    358553
# M    403842
# X     97868

# 5. ANALYSIS

# Identify the most frequent crime types by count with %
most_frequent_crime = (
    crime_analysis
    .groupby('Crm Cd')['Crm Cd Desc']
    .value_counts()
    .reset_index(name='Count')
    .sort_values(by='Count', ascending=False)
)
most_frequent_crime['%'] = round(most_frequent_crime['Count'] / most_frequent_crime['Count'].sum() * 100, 2)
most_frequent_crime.set_index('Crm Cd', inplace=True)
print(most_frequent_crime)

# groupby + value_counts is used to verify that each crime code corresponds
# to a single crime description while computing crime frequencies
# Crime distribution is highly concentrated. Approximately twenty crime categories
# represent more than 1 percent of total incidents, while the remaining categories
# individually account for a very small share of the dataset.

major_crime = most_frequent_crime[most_frequent_crime['%'] >= 1]
print(major_crime)

#                                                      Crm Cd Desc   Count     %
# Crm Cd
# 510                                             VEHICLE - STOLEN  115184 11.46
# 624                                     BATTERY - SIMPLE ASSAULT   74821  7.45
# 330                                        BURGLARY FROM VEHICLE   63515  6.32
# 354                                            THEFT OF IDENTITY   62536  6.22
# 740      VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)   61086  6.08
# 310                                                     BURGLARY   57871  5.76
# 440                           THEFT PLAIN - PETTY ($950 & UNDER)   53716  5.35
# 230               ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT   53523  5.33
# 626                            INTIMATE PARTNER - SIMPLE ASSAULT   46712  4.65
# 420              THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)   41311  4.11
# 331          THEFT FROM MOTOR VEHICLE - GRAND ($950.01 AND OVER)   36940  3.68
# 341     THEFT-GRAND ($950.01 & OVER)EXCPT,GUNS,FOWL,LIVESTK,PROD   35149  3.50
# 210                                                      ROBBERY   32315  3.22
# 442                     SHOPLIFTING - PETTY THEFT ($950 & UNDER)   30908  3.08
# 745                     VANDALISM - MISDEAMEANOR ($399 OR UNDER)   25374  2.53
# 930                       CRIMINAL THREATS - NO WEAPON DISPLAYED   19278  1.92
# 888                                                  TRESPASSING   18424  1.83
# 761                                              BRANDISH WEAPON   14532  1.45
# 236                        INTIMATE PARTNER - AGGRAVATED ASSAULT   12656  1.26
# 901                               VIOLATION OF RESTRAINING ORDER   11748  1.17

# crime trend over time
# Aggregate crime incidents by month using the occurrence timestamp.
# pd.Grouper groups all timestamps into monthly periods (freq='M').
# .size() counts the number of incidents (rows) in each month.
# The result is a table with two columns:
#   - Timestamp OCC DT : the month reference
#   - Crime Count      : number of crime incidents in that month

crime_trend_month = (crime_analysis
                     .groupby(pd.Grouper(key='Timestamp OCC DT', freq='ME'))
                     .size()
                     .reset_index(name='Crime Count'))

# identify areas with the highest crime levels
areas_crime_level_avg = (crime_analysis
                         .groupby(['AREA', 'AREA NAME'])
                         .agg({'Crm Cd': 'count',
                               'LAT': 'mean',
                               'LON': 'mean'})
                         .reset_index()
                         .rename(columns={'Crm Cd': 'AREA Count'})
                         .sort_values(by='AREA Count', ascending=False))

areas_crime_level_avg['AREA %'] = round(areas_crime_level_avg['AREA Count'] / areas_crime_level_avg['AREA Count'].sum() * 100, 2)

print(areas_crime_level_avg)

# Aggregate crime incidents by police area and compute representative coordinates.
# The number of incidents is calculated using count(), while the mean latitude and
# longitude are used to approximate a central point for each area. These coordinates
# do not define the official geographic center of the district; they provide a
# representative location to position a single bubble per area in the map visualization.

# AREA    AREA NAME  AREA Count   LAT     LON  AREA %
#    1      Central       69668 33.95 -117.92    6.93
#   12  77th Street       61756 33.90 -118.04    6.15
#   14      Pacific       59513 33.88 -118.08    5.92
#    3    Southwest       57434 33.98 -118.18    5.72
#    6    Hollywood       52429 33.89 -117.60    5.22
#   15  N Hollywood       51106 34.11 -118.17    5.09
#   20      Olympic       50070 33.97 -117.99    4.98
#   18    Southeast       49929 33.84 -117.93    4.97
#   13       Newton       49173 33.94 -118.02    4.89
#    7     Wilshire       48237 33.97 -118.03    4.80
#    2      Rampart       46824 33.99 -118.01    4.66
#    8      West LA       45725 34.02 -118.32    4.55
#   11    Northeast       42951 34.07 -118.12    4.27
#    9     Van Nuys       42881 34.12 -118.25    4.27
#   10  West Valley       42146 34.16 -118.42    4.19
#   17   Devonshire       41743 34.17 -118.27    4.15
#    5       Harbor       41392 33.72 -118.11    4.12
#   21      Topanga       41365 34.17 -118.52    4.12
#   19      Mission       40342 34.16 -118.12    4.01
#    4   Hollenbeck       37081 33.98 -117.94    3.69
#   16     Foothill       33129 34.17 -118.11    3.30

# The initial version of the crime concentration map used the mean latitude
# and longitude of all incidents within each police area. While mathematically
# correct, this method produced misleading geographic positions. The average
# coordinate represents a centroid of all incidents and may fall in locations
# where crimes did not actually occur, making the map less interpretable.

# First adjustment
# To improve geographic accuracy, the analysis was modified to use the most
# frequent pair of latitude and longitude for each area. This method ensures
# that the representative point corresponds to a real location present in the
# dataset where incidents occur most often.

# However, further inspection showed that even this approach can still produce
# an imprecise representation of crime distribution. A single representative
# point cannot fully describe how incidents are spatially distributed within
# an area.

# Final analytical approach
# Instead of relying on a single coordinate per area, the analysis now examines
# the distribution of all coordinate pairs within each area. By counting how
# often each coordinate pair appears, it becomes possible to observe how crimes
# are spatially dispersed and identify micro-concentrations.

# The final geographic interpretation will therefore rely on:
# - analyzing the frequency of coordinate pairs
# - observing spatial distribution patterns
# - refining the visual representation directly in Power BI
#
#  will be used to customize the map visualization in order to produce
# a more accurate graphical representation of crime concentration across areas.

# Identify the most frequent coordinate pair for each police area
coords_freq = (
    crime_analysis
    .groupby(['AREA', 'AREA NAME', 'LAT', 'LON'])
    .size()
    .reset_index(name='coord_freq')
)

coords_freq_sorted = coords_freq.sort_values(
    by=['AREA', 'coord_freq'],
    ascending=[True, False]
)

# keep the most frequent coordinate pair for each area
area_top_coords = (
    coords_freq_sorted
    .drop_duplicates(subset=['AREA', 'AREA NAME'])
    [['AREA', 'AREA NAME', 'LAT', 'LON']]
)

# Compute total crime counts per area
area_counts = (
    crime_analysis
    .groupby(['AREA', 'AREA NAME'])
    .size()
    .reset_index(name='AREA Count')
)

# Merge representative coordinates with crime counts
areas_crime_level = area_counts.merge(
    area_top_coords,
    on=['AREA', 'AREA NAME'],
    how='left'
)

# Calculate percentage share of crimes per area
areas_crime_level['AREA %'] = round(
    areas_crime_level['AREA Count'] /
    areas_crime_level['AREA Count'].sum() * 100,
    2
)

# Sort areas by crime volume
areas_crime_level_mf = areas_crime_level.sort_values(
    by='AREA Count',
    ascending=False
)

print(areas_crime_level_mf)

# Analyze spatial distribution of crimes within each area
# Instead of relying on one coordinate per area, this measures how crimes
# are distributed across all coordinate pairs.

area_coords_stats = (
    crime_analysis
    .groupby(['AREA', 'AREA NAME', 'LAT', 'LON'])
    .size()
    .reset_index(name='Crime Count')
)

# total crimes per area
area_totals = (
    crime_analysis
    .groupby(['AREA', 'AREA NAME'])
    .size()
    .reset_index(name='Area Total')
)

# merge totals to compute coordinate-level percentages
area_coords_stats = area_coords_stats.merge(
    area_totals,
    on=['AREA', 'AREA NAME'],
    how='left'
)

# percentage contribution of each coordinate pair
area_coords_stats['Crime %'] = round(
    area_coords_stats['Crime Count'] /
    area_coords_stats['Area Total'] * 100,
    2
)

# sort coordinates by frequency within each area
area_coords_stats = area_coords_stats.sort_values(
    ['AREA', 'Crime Count'],
    ascending=[True, False]
)

# keep only coordinate pairs representing at least 1% of crimes within each police area
area_coords_stats = (
    area_coords_stats[area_coords_stats['Crime %'] >= 1]
    .sort_values(['AREA', 'Crime Count'], ascending=[True, False])
)

# Coordinate pairs representing at least 1% of crimes within each police area
# were retained to highlight the most significant spatial concentrations while
# reducing noise from low-frequency locations.

# Treat invalid ages as missing according to stakeholder decision
crime_analysis.loc[
    crime_analysis['Vict Age'] <= 0,
    'Vict Age'
] = pd.NA

# Create age groups for victims

# Define the boundaries of the age bins
age_bins = [2, 10, 13, 18, 21, 25, 35, 50, 65, 121]

# Define the labels corresponding to each age bin
age_labels = [
    '2-9',
    '10-12',
    '13-17',
    '18-20',
    '21-24',
    '25-34',
    '35-49',
    '50-64',
    '65+'
]

# Create the age group column
crime_analysis['Vict Age Group'] = pd.cut(
    crime_analysis['Vict Age'],
    bins=age_bins,
    labels=age_labels,
    right=False
)

# Create numeric column to control ordering in Power BI
age_order = {
    '2-9': 1,
    '10-12': 2,
    '13-17': 3,
    '18-20': 4,
    '21-24': 5,
    '25-34': 6,
    '35-49': 7,
    '50-64': 8,
    '65+': 9
}

crime_analysis['Age Order'] = crime_analysis['Vict Age Group'].map(age_order)

# Normalize age groups to preserve logical order
crime_analysis['Vict Age Group'] = pd.Categorical(
    crime_analysis['Vict Age Group'],
    categories=age_labels,
    ordered=True
)

# Select crimes where a weapon was recorded
weapon_crimes = crime_analysis[
    crime_analysis['Weapon Used Cd'].notna()
]

# Aggregate crimes by age group, sex and weapon
weapon_crime_summary = (
    weapon_crimes
    .groupby([
        'Vict Age Group',
        'Age Order',
        'Vict Sex',
        'Weapon Used Cd',
        'Weapon Desc'
    ])
    .size()
    .reset_index(name='count')
)

# Sort results
# Age group → Sex → Count
weapon_crime_summary = weapon_crime_summary.sort_values(
    by=['Vict Age Group', 'Vict Sex', 'count'],
    ascending=[True, True, False]
)

# Display result
print(weapon_crime_summary)

# Select crimes where a weapon was recorded
weapon_crimes = crime_analysis[
    crime_analysis['Weapon Used Cd'].notna()
]

# Find the top 20 most frequent weapon codes
top20_weapons = (
    weapon_crimes
    .groupby(['Weapon Used Cd', 'Weapon Desc'])
    .size()
    .reset_index(name='count')
    .sort_values('count', ascending=False)
    .head(20)
)

# Keep only crimes involving the top 20 weapons
weapon_top20 = weapon_crimes.merge(
    top20_weapons[['Weapon Used Cd']],
    on='Weapon Used Cd',
    how='inner'
)

# Aggregate by age group, sex and weapon
weapon_top20_summary = (
    weapon_top20
    .groupby([
        'Vict Age Group',
        'Age Order',
        'Vict Sex',
        'Weapon Used Cd',
        'Weapon Desc'
    ])
    .size()
    .reset_index(name='count')
)

# Sort results for Power BI
# Age Order → Sex → Count
weapon_top20_summary = weapon_top20_summary.sort_values(
    by=['Age Order', 'Vict Sex', 'count'],
    ascending=[True, True, False]
)

# Display result
print(weapon_top20_summary)

# 6. EXPORT TABLES FOR POWER BI
# export aggregated table for visualization (Power BI)
# file saved locally and moved to the project data folder

major_crime.to_csv('major_crime.csv')
crime_trend_month.to_csv('crime_trend_month.csv', index=False)
areas_crime_level_avg.to_csv('areas_crime_level.csv', index=False)
areas_crime_level_mf.to_csv('areas_crime_level_mf.csv', index=False)
area_coords_stats.to_csv('area_coords_stats.csv', index=False)
weapon_crime_summary.to_csv('weapon_crime_summary.csv', index=False)
weapon_top20_summary.to_csv('weapon_crime_summary_top20.csv', index=False)
