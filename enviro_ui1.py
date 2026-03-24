import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, MarkerCluster
from util import output_pollution_source, log_transform
import joblib

st.set_page_config(layout="wide", page_title="Pollution Source Identifier")
st.title("Pollution Source Dashboard")
st.write('Interactive map with pollution souce labels.')

df = pd.read_csv('df_final.csv')
x = df.drop('Pollution Source encoded', axis = 1)
model = joblib.load('decision_tree_model.pkl')
predictions = model.predict(x)
prediction_labels = output_pollution_source(predictions)
x['predicted_labels'] = prediction_labels
x = x.dropna(subset=['pm25', 'latitude', 'longitude'])
m = folium.Map(location=[x.latitude.mean(), x.longitude.mean()], zoom_start=4, tiles='CartoDB positron')

heat_data = x[['latitude', 'longitude', 'pm25']].values.tolist()
HeatMap(heat_data, radius=15, blur=20, name="Pollution Heatmap").add_to(m)

source_layers = {}
for source_type in x['predicted_labels'].unique():
    source_layers[source_type] = folium.FeatureGroup(name=f"Source: {source_type}")

icon_map = {
    'industrial': {'icon': 'industry', 'color': 'darkred'},
    'vehicular': {'icon': 'car', 'color': 'blue'},
    'agricultural': {'icon': 'leaf', 'color': 'green'},
    'burning': {'icon': 'fire', 'color': 'orange'},
    'natural': {'icon': 'tree', 'color': 'lightgreen'}
}

for idx, row in x.iterrows():
    style = icon_map.get(row['predicted_labels'].lower(), {'icon': 'info-sign', 'color': 'gray'})
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        icon=folium.Icon(color=style['color'], icon=style['icon'], prefix='fa'),
        popup=f"<b>Source:</b> {row['predicted_labels']}<br><b>PM2.5:</b> {row['pm25']}"
    ).add_to(source_layers[row['predicted_labels']])

for layer in source_layers.values():
    layer.add_to(m)

folium.LayerControl(position='topright', collapsed=True).add_to(m)

c1, c2, c3 = st.columns([1, 4, 1])
with c2:
    st_folium(m, width=900, height=500)

st.divider()
st.subheader("Data Preview")
st.dataframe(x.head(), use_container_width=True)
st.divider()
st.subheader("Data Plot")

numeric_cols = x.select_dtypes(['float64', 'int64']).columns
c1_choice = st.sidebar.selectbox("X axis", numeric_cols, index=0)
c2_choice = st.sidebar.selectbox("Y axis", numeric_cols, index=1)

if c1_choice and c2_choice:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fig, ax = plt.subplots()
        ax.scatter(x[c1_choice], x[c2_choice], s=5, alpha=0.5, color='teal')
        ax.set_xlabel(c1_choice)
        ax.set_ylabel(c2_choice)
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)

st.divider()
st.subheader("Predict Pollution Source")
st.write("Input pollution and weather parameters")
st.markdown("## **Input Features**")
col1, col2, col3 = st.columns(3)
with col1:
    latitude = st.slider("Latitude", -90.0, 90.0, 0.0)
    longitude = st.slider("Longitude", -180.0, 180.0, 0.0)
    temperature_owm = st.slider("Temperature", 10.0, 50.0, 0.0)
    humidity_owm = st.slider("Humidity", 0, 100, 0)
    farm_influence = st.slider("Farm Influence Factor", 0.0, 50.0, 0.0)
    wind_speed_owm = st.slider("Wind Speed", 0.0, 10.0, 0.0)
with col2:
    wind_direction_owm = st.slider("Wind Direction", 0, 360, 0)
    pm10 = st.slider("pm10 level", 0.0, 1000.0, 0.0)
    o3 = st.slider("03 level", 0.0, 500.0, 0.0)
    no = st.slider("no level", 0.0, 300.0, 0.0)
    dumpsite_influence = st.slider("Dumpsite Influence Factor", 0.0, 5.0, 0.0)
    no2 = st.slider("no2 level", 0.0, 500.0, 0.0)
with col3:
    so2 = st.slider("so2 level", 0.0, 200.0, 0.0)
    co = st.slider("co level", 0.0, 25000.0, 0.0)
    pm25 = st.slider("pm2.5 level", 0.0, 500.0, 0.0)
    nox = st.slider("nox level", 0.0, 0.5, 0.0)
    road_influence = st.slider("Road Influence Factor", 0.0, 500.0, 0.0)
    industry_influence = st.slider("Industry Influence Factor", 0.0, 200.0, 0.0)


st.divider()
st.subheader("Predict")
if st.button("Predict Pollution Source", type="primary", use_container_width=False):
    
    input_values = [latitude, longitude, temperature_owm, humidity_owm,
                    wind_speed_owm, wind_direction_owm, pm10, o3, no,
                    no2, so2, co, pm25, nox, road_influence, industry_influence,
                    farm_influence, dumpsite_influence]
    
    feature_order = ['latitude', 'longitude', 'temperature_owm', 'humidity_owm',
                    'wind_speed_owm', 'wind_direction_owm', 'pm10', 'o3', 'no',
                    'no2', 'so2', 'co', 'pm25', 'nox', 'road_influence', 'industry_influence',
                    'farm_influence', 'dumpsite_influence']

    input_df = pd.DataFrame([input_values], columns=feature_order)

    try:
        prediction = model.predict(input_df)
        prediction_prob = model.predict_proba(input_df)
        confidence = prediction_prob[0].max()
        # st.balloons()
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="Pollution Source",value=str(output_pollution_source(prediction[0])))
        with res_col2:
            st.metric(label="Confidence Score:",value=f"{confidence:.2%}")
    except Exception as e:
        st.error(f"Prediction Failed")
        st.write(f"Error Details:{e}")
st.divider()