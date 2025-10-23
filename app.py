import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="CO₂ Emission Dashboard", page_icon="🌍", layout="wide")


@st.cache_data
def load_data():
    url = "https://github.com/owid/co2-data/raw/master/owid-co2-data.csv"
    df = pd.read_csv(url)
    df = df[df["year"] >= 1950]
    return df

df = load_data()


st.sidebar.title("🌎 CO₂ Emission Dashboard")
countries = st.sidebar.multiselect(
    "Select countries:",
    options=sorted(df["country"].unique()),
    default=["Sweden", "United States", "China"]
)

metric_list = ["co2", "co2_per_capita", "share_global_co2"]
metric = st.sidebar.selectbox(
    "Select metric:",
    metric_list,
    index=0
)

metric_names = {
    "co2": "Total CO₂ emissions (million tonnes)",
    "co2_per_capita": "CO₂ emissions per capita (tonnes)",
    "share_global_co2": "Share of global CO₂ emissions (%)"
}



st.title("🌍 CO₂ Emission Dashboard")
st.markdown("Data source: [Our World in Data](https://ourworldindata.org/co2-emissions)")

min_year, max_year = int(df["year"].min()), int(df["year"].max())
year_range = st.slider(
    "Select year range:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year) 
)
st.markdown(f"**Showing data from {year_range[0]} to {year_range[1]}**")



filtered = df[(df["country"].isin(countries) &
    df["year"].between(year_range[0], year_range[1]))]

fig = px.line(
    filtered,
    x="year",
    y=metric,
    color="country",
    title=f"{metric_names[metric]} ({year_range[0]}–{year_range[1]})"
)
fig.update_layout(legend_title_text="Country", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)
