import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import datetime

st.title("STREAMLIT HW")
st.markdown(
"""
MR.WARACH CHANGWATTHANAKUL
6030821521 SURVEY ENGINEER
""")

START = "timestart"
day = st.slider("Day to look at", 1, 4, step = 1)
if day == 1:
    DATA_URL = ("https://raw.githubusercontent.com/warach7/STREAMLIT_HW/master/20190101.csv")
elif day == 2:
    DATA_URL = ("https://raw.githubusercontent.com/warach7/STREAMLIT_HW/master/20190103.csv")
elif day == 3:
    DATA_URL = ("https://raw.githubusercontent.com/warach7/STREAMLIT_HW/master/20190104.csv")
elif day == 4:
    DATA_URL = ("https://raw.githubusercontent.com/warach7/STREAMLIT_HW/master/20190105.csv")

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[START] = pd.to_datetime(data[START], format = '%d/%m/%Y %H:%M')
    return data

data = load_data(100000)

hour = st.slider("Hour to look at", 0, 23, step = 3)

data = data[data[START].dt.hour == hour]
data = data.drop(data.columns[0], axis=1)
for i in range(5):
    data = data.drop(data.columns[6], axis=1)

st.subheader("Geo data between %i:00 and %i:00" % (hour, (hour + 3) % 24))
midpoint = (np.average(data["latstartl"]), np.average(data["lonstartl"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data,
            get_position=["lonstartl", "latstartl"],
            radius=150,
            elevation_scale=5,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 3) % 24))
filtered = data[
    (data[START].dt.hour >= hour) & (data[START].dt.hour < (hour + 3))
]
hist = np.histogram(filtered[START].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ), use_container_width=True)

if st.checkbox("Show raw data", False):
    st.subheader("Raw data by minute between %i:00 and %i:00" % (hour, (hour + 3) % 24))
    st.write(data)
