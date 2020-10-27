import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL = "Motor_Vehicle_Collisions_-_Crashes.csv"

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This application is a Streamlit dashboard that can be used to analyze motor vehicle collisions in "
            "New York City 🗽💥🚗.")
st.markdown("Data courtesy of the "
            "[City of New York](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)")


@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x : str(x).lower()
    data.rename(lowercase, axis = 'columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)

    return data

st.sidebar.header("How many entries would you like to load?")
nrows = st.sidebar.selectbox('Note: Loading more entries requires more time',
             ('5000', '10000', '25000', '50000', '100000', '200000', '400000'))

data = load_data(int(nrows))
original_data = data

st.subheader("Where are the most people injured in NYC?")

st.sidebar.header("Map 1: Number of persons injured in vehicle collision?")
injured_people = st.sidebar.slider("Map 1 displays accidents with the selected amount of people injured.", 0, 19, 4)

midpoint = (np.average(data['latitude']), np.average(data['longitude']))
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.sidebar.header("Map 2: How many collisions occur during a given time of day?")
hour = st.sidebar.slider("Map 2 displays accidents that occured at the hour selected.", 0, 23)
data = data[data['date/time'].dt.hour == hour]

st.subheader("Number of collisions that occured between %i:00 and %i:00:" % (hour, (hour + 1) % 24))

st.write(pdk.Deck(
    map_style = "mapbox://styles/mapbox/light-v9",
    initial_view_state = {
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers = [
        pdk.Layer(
        "HexagonLayer",
        data = data[['date/time', 'latitude', 'longitude']],
        get_position = ['longitude', 'latitude'],
        radius = 100,
        extruded = True,
        pickable = True,
        elevation_scale = 4,
        elevation_range = [0, 1000],
        ),
    ],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour <= (hour + 1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

st.markdown("From this, we can conclude that motor vehicle collisions are significantly more likely"
            "to occur during the nighttime. Between 0:00 and 6:00 is the peak time for collisions.")

st.header("Top 5 dangerous streets by affected type")
select = st.selectbox('Affected type of people', ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]].sort_values(by=["injured_pedestrians"], ascending=False).dropna(how="any")[:5])
elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]].sort_values(by=["injured_cyclists"], ascending=False).dropna(how="any")[:5])
else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]].sort_values(by=["injured_motorists"], ascending=False).dropna(how="any")[:5])

st.markdown("From this, we can conclude that motor vehicle collisions involving pedestrians are"
            "significantly more likely to result in injuries.")

st.sidebar.text("\n")
if st.sidebar.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
