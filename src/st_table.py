import streamlit as st
from sklearn.datasets import load_breast_cancer
import plotly.express as px

data  = load_breast_cancer(as_frame = True)
data = data["frame"]


st.set_page_config(page_title="Table data", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

st.title("Data Analyse")
side = st.sidebar

col = "mean perimeter"
with side:
    st.markdown("### FILTER")
    slide_mp = st.slider("MEAN_PERIMETER > ", float(data[col].min()), float(data[col].max()), float(data[col].min()), 1.0)
    st.markdown("### SCATTERPLOT")
    x = st.selectbox("X: ", data.columns, index=0)
    y = st.selectbox("Y: ", data.columns, index=1)

    
col1, col2 = st.columns([3, 1])

filtered_data = data.query(f"`mean perimeter` > {slide_mp}")

with col1:
    fig = px.scatter(filtered_data, x = x, y = y)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    target_data = filtered_data.groupby(["target"])["target"].count().rename("cnt_target").reset_index()
    fig = px.bar(target_data, x = "target", y = "cnt_target")
    st.plotly_chart(fig, use_container_width=True)
st.dataframe(filtered_data.head())