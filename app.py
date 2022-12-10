import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sqlalchemy import create_engine

# Code contains some debug prints, which should be removed before production usage
# Data was downloaded in .csv format through QGIS
# Also imported the sqlite format from QGIS but not used in this task
data = pd.read_csv('rakennukset_piste_rekisteritiedot.csv')
#print(data)

# Drop some unused attributes related to the task for simpler data, convert NaN values to 0 and convert datetime to another format
cleaned_data = data.drop(columns=['i_pyraknro', 'c_vtj_prt','c_kiinteistotunnus','i_nkoord', 'i_ekoord','c_julkisivu', 'c_lammtapa', 'c_poltaine', 'c_rakeaine', 'c_hissi','c_viemlii', 'c_vesilii',
    'c_sahkolii', 'katunimi_suomi', 'katunimi_ruotsi', 'osoitenumero']).fillna(0)
cleaned_data['c_valmpvm'] = pd.to_datetime(cleaned_data['c_valmpvm'], format='%Y/%m/%d %H:%M:%S', errors = 'coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
#print(cleaned_data.iloc[0])

# db stuff, setting data to sqlite db table
engine = create_engine('sqlite:///buildings.db')
cleaned_data.to_sql(name='buildings', con=engine, if_exists='replace')

# 2.  calculate how the fraction of residential buildings in all buildings (floor area) has developed over the last three years.
# floor area of all residential buildings from year 2022-2020 / floor area of all buildings from year 2022-2020
# floor area = area of all floors of the building
# According to https://kartta.hel.fi/avoindata/dokumentit/2017-01-10_Rakennusaineisto_avoindata_koodistot.pdf , residential buildings are codes 011,012,013,021,022,032,039,041
residential_building_codes = ['011','012','013','021','022','032','039','041']
office_building_code = '151'

# Beware of copy-paste, should be refactored

def compute_and_print_2020():
    floor_area_2020_residential = pd.read_sql_query("SELECT SUM(i_kokala) FROM buildings WHERE datetime(c_valmpvm) BETWEEN '2020-01-01 00:00:00' AND '2020-12-31 23:59:00' AND \
        c_kayttark IN (11.0, 12.0, 13.0, 21.0, 22.0, 32.0, 39.0, 41.0)", engine)
    print("Floor area of residential buildings built during 2020 in square meters: " + str(floor_area_2020_residential.iloc[0]))
    floor_area_2020_all = pd.read_sql_query("SELECT SUM(i_kokala) FROM buildings WHERE datetime(c_valmpvm) BETWEEN '2020-01-01 00:00:00' AND '2020-12-31 23:59:00' ", engine)
    print("Floor area of all buildings built during 2020 in square meters: " + str(floor_area_2020_all.iloc[0]))
    fraction_2020 = floor_area_2020_residential / floor_area_2020_all
    print("Fraction residential/all of 2020 buildings: " + str(fraction_2020.iloc[0]))

def compute_and_print_2021():
    floor_area_2021_residential = pd.read_sql_query("SELECT SUM(i_kokala) FROM buildings WHERE datetime(c_valmpvm) BETWEEN '2021-01-01 00:00:00' AND '2021-12-31 23:59:00' AND \
        c_kayttark IN (11.0, 12.0, 13.0, 21.0, 22.0, 32.0, 39.0, 41.0)", engine)
    print("Floor area of residential buildings built during 2021 in square meters: " + str(floor_area_2021_residential.iloc[0]))
    floor_area_2021_all = pd.read_sql_query("SELECT SUM(i_kokala) FROM buildings WHERE datetime(c_valmpvm) BETWEEN '2021-01-01 00:00:00' AND '2021-12-31 23:59:00' ", engine)
    print("Floor area of all buildings built during 2021 in square meters: " + str(floor_area_2021_all.iloc[0]))
    fraction_2021 = floor_area_2021_residential / floor_area_2021_all
    print("Fraction residential/all of 2021 buildings: " + str(fraction_2021.iloc[0]))

def compute_and_print_2022():
    floor_area_2022_residential = pd.read_sql_query("SELECT SUM(i_kokala) FROM buildings WHERE datetime(c_valmpvm) BETWEEN '2022-01-01 00:00:00' AND '2022-12-31 23:59:00' AND \
        c_kayttark IN (11.0, 12.0, 13.0, 21.0, 22.0, 32.0, 39.0, 41.0)", engine)
    print("Floor area of residential buildings built during 2022 in square meters: " + str(floor_area_2022_residential.iloc[0]))
    floor_area_2022_all = pd.read_sql_query("SELECT SUM(i_kokala) FROM buildings WHERE datetime(c_valmpvm) BETWEEN '2022-01-01 00:00:00' AND '2022-12-31 23:59:00' ", engine)
    print("Floor area of all buildings built during 2022 in square meters: " + str(floor_area_2022_all.iloc[0]))
    fraction_2022 = floor_area_2022_residential / floor_area_2022_all
    print("Fraction residential/all of 2022 buildings: " + str(fraction_2022.iloc[0]))


compute_and_print_2020()
compute_and_print_2021()
compute_and_print_2022()

# 3. Interesting attributes; when built, how much is the whole floor space, how many floors, how much space per floor
def get_offices_in_centre_and_visualize():
    offices_in_centre = pd.read_sql_query('SELECT c_valmpvm, i_kokala, i_kerrlkm, i_kerrosala FROM buildings WHERE c_kayttark = 151 AND postinumero = 100.0', engine)
    #print(offices_in_centre)
    build_date = pd.to_datetime(offices_in_centre['c_valmpvm'])
    floor_area = offices_in_centre['i_kokala']
    floor_count = offices_in_centre['i_kerrlkm']
    area_by_floor = offices_in_centre['i_kerrosala']

    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.scatter(build_date, floor_area, c='red')
    ax2.scatter(build_date, floor_count, c='blue')
    ax1.set_title('Build date and floor area')
    ax1.set_xlabel('Build date')
    ax1.set_ylabel('Floor area in m²')

    ax2.set_title('Build date and floor count')
    ax2.set_xlabel('Build date')
    ax2.set_ylabel('Amount of floors')
    plt.show()

get_offices_in_centre_and_visualize()