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
metric = st.sidebar.selectbox(
    "Select metric:",
    ["co2", "co2_per_capita", "share_global_co2"]
)


st.title("🌍 CO₂ Emission Dashboard")
st.markdown("Data source: [Our World in Data](https://ourworldindata.org/co2-emissions)")
st.markdown(f"**Showing data from 1950 to {df['year'].max()}**")

filtered = df[df["country"].isin(countries)]

fig = px.line(
    filtered,
    x="year",
    y=metric,
    color="country",
    title=f"{metric.replace('_', ' ').title()} over Time"
)
fig.update_layout(legend_title_text="Country", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)
