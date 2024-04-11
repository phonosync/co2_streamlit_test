import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# download the data
@st.cache_data
def get_data():
    url='https://drive.switch.ch/index.php/s/BrEq5fWfSW5sUEq/download'
    return pd.read_csv(url, sep=';')

@st.cache_data
def get_regions():
    url='https://drive.switch.ch/index.php/s/hUkzz67kE1YkLE9/download'
    return pd.read_csv(url, sep=';')

df_regions = get_regions()
df_regions = df_regions[['Code', 'World Region according to the World Bank']]
df_regions.columns = ['iso_code', 'region']

df = get_data()

# Some data wrangling

df['gdp_per_capita'] = df['gdp']/df['population']

df = df[['country', 'iso_code', 'year', 'population', 'co2', 'gdp', 'co2_per_capita', 'gdp_per_capita']]

df = pd.merge(df, df_regions, left_on='iso_code', right_on='iso_code', how='left')

df = df[~df['region'].isna()]

st.title(body='CO2-Emissions and GDP')
st.markdown('Exploring the CO2 emission dataset from (Our World in Data)[https://ourworldindata.org/grapher/co2-emissions-vs-gdp]. [Data repository](https://github.com/owid/co2-data/tree/master)')

st.subheader('Dataset overview')
st.markdown('The following table displays a random sample from the dataset:')
st.dataframe(data=df.sample(10, random_state=23), use_container_width=True, hide_index=True,
             column_config={
                'country': st.column_config.TextColumn(
                     'Country',
                    help="Name of the country",
                ),
                'year': st.column_config.NumberColumn(
                    help="Year",
                    min_value=0,
                    max_value=3000,
                    step=1,
                    format="%d"
                )
             }
            )


st.header('CO2 Emissions and GDP in one year')

year_selected = 1964
year_selected = st.slider('Select the year', df.year.min(), df.year.max(), 1964)
df_selected = df[df['year']== year_selected]

st.markdown("""some ideas:  
            - create a slider to select a year  
                - scatterplot: CO2 emissions vs. GDP on all countries for the selected year  
                - bar charts for CO2 emissions and GDP aggregated by region  
            - world map - countries colored by CO2 emissions per capita  
            - ...
            """)


