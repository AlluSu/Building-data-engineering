import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sqlalchemy import create_engine

# Code contains some debug prints, which should be removed before production usage
# Data was downloaded in .csv format through QGIS
# Also imported the sqlite format from QGIS but not used in this task for more data engineering related exercise
data = pd.read_csv('rakennukset_piste_rekisteritiedot.csv')

# Drop some unused attributes related to the task for simpler data, convert NaN values to 0 and convert datetime to another format for executing queries
cleaned_data = data.drop(columns=['i_pyraknro', 'c_vtj_prt','c_kiinteistotunnus','i_nkoord', 'i_ekoord','c_julkisivu', 'c_lammtapa',
    'c_poltaine', 'c_rakeaine','c_viemlii', 'c_vesilii', 'c_sahkolii', 'katunimi_suomi', 'katunimi_ruotsi', 'osoitenumero']).fillna(0)
cleaned_data['c_valmpvm'] = pd.to_datetime(cleaned_data['c_valmpvm'], format='%Y/%m/%d %H:%M:%S', errors = 'coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

# db stuff, setting data to sqlite db table
# For more heavy-weight geographical data processing, Postgres with Postgis would be a better option
# Schema could be specified
engine = create_engine('sqlite:///buildings.db')
cleaned_data.to_sql(name='buildings', con=engine, if_exists='replace')

# Computing sums of floor area's of all residential buildings built during 2020-2022
# Putting results in a dataframe and returning it
# According to https://kartta.hel.fi/avoindata/dokumentit/2017-01-10_Rakennusaineisto_avoindata_koodistot.pdf
# residential buildings are codes 011,012,013,021,022,032,039,041
def compute_residential_data(engine):
    floor_area_residential_2020 = pd.read_sql_query("SELECT SUM(i_kokala) AS residential FROM buildings WHERE datetime(c_valmpvm) \
        BETWEEN :start_date AND :end_date AND c_kayttark IN (11.0, 12.0, 13.0, 21.0, 22.0, 32.0, 39.0, 41.0)", engine,
        params={"start_date":'2020-01-01 00:00:00', "end_date":'2020-12-31 23:59:00'})
    floor_area_residential_2021 = pd.read_sql_query("SELECT SUM(i_kokala) AS residential FROM buildings WHERE datetime(c_valmpvm) \
        BETWEEN :start_date AND :end_date AND c_kayttark IN (11.0, 12.0, 13.0, 21.0, 22.0, 32.0, 39.0, 41.0)", engine,
        params={"start_date":'2021-01-01 00:00:00', "end_date":'2021-12-31 23:59:00'})
    floor_area_residential_2022 = pd.read_sql_query("SELECT SUM(i_kokala) AS residential FROM buildings WHERE datetime(c_valmpvm) \
        BETWEEN :start_date AND :end_date AND c_kayttark IN (11.0, 12.0, 13.0, 21.0, 22.0, 32.0, 39.0, 41.0)", engine,
        params={"start_date":'2022-01-01 00:00:00', "end_date":'2022-12-31 23:59:00'})
    res = pd.concat([floor_area_residential_2020, floor_area_residential_2021, floor_area_residential_2022])
    return res

# Computing sums of floor area's of all buildings built during 2020-2022
# Putting results in a dataframe and returning it
def compute_all_building_data(engine):
    floor_area_all_2020 = pd.read_sql_query("SELECT SUM(i_kokala) AS all_data FROM buildings WHERE datetime(c_valmpvm) \
        BETWEEN :start_date AND :end_date", engine, params={"start_date":'2020-01-01 00:00:00', "end_date":'2020-12-31 23:59:00'})
    floor_area_all_2021 = pd.read_sql_query("SELECT SUM(i_kokala) AS all_data FROM buildings WHERE datetime(c_valmpvm) \
        BETWEEN :start_date AND :end_date", engine, params={"start_date":'2021-01-01 00:00:00', "end_date":'2021-12-31 23:59:00'})
    floor_area_all_2022 = pd.read_sql_query("SELECT SUM(i_kokala) AS all_data FROM buildings WHERE datetime(c_valmpvm) \
        BETWEEN :start_date AND :end_date", engine, params={"start_date":'2022-01-01 00:00:00', "end_date":'2022-12-31 23:59:00'})
    res = pd.concat([floor_area_all_2020, floor_area_all_2021, floor_area_all_2022])
    return res

def get_summary():
    all_data_df = compute_all_building_data(engine)
    residential_data_df = compute_residential_data(engine)
    years = ['2020', '2021', '2022']
    final_df = pd.concat([all_data_df, residential_data_df], axis=1)
    final_df = final_df.rename(columns={"all_data": "All buildings", "residential": "Residential buildings"})
    final_df['Year'] = years
    final_df['Fraction'] = final_df.apply(lambda x: compute_fraction(x['All buildings'], x['Residential buildings']), axis=1)
    print(final_df)
    return final_df

# Compute the fraction of residential buildings to all buildings by the three last years
def compute_fraction(all_data, residential_data):
    return residential_data/all_data

# Interesting attributes; when built, how much is the whole floor space, how many floors, how much space per floor
def get_offices_in_centre_and_visualize():
    offices_in_centre = pd.read_sql_query('SELECT c_valmpvm, i_kokala, i_kerrlkm, i_kerrosala FROM buildings WHERE c_kayttark = 151 AND postinumero = 100.0', engine)
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

get_summary()
get_offices_in_centre_and_visualize()