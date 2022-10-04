import streamlit as st

st.set_page_config(page_title="INRO", page_icon=None, initial_sidebar_state="auto", menu_items=None)

st.info("First comment")

header = st.container()
main_page = st.container()

delete = st.button("DELETE", key = "delete", disabled = False) 
undo = st.button("UNDO", key = "undo", disabled = False)
update = st.button("UPDATE", key = "update", disabled = False)

cols = st.columns([1, 4, 2])
for i, col in enumerate(cols):
    with col:
        st.text(f"col {i}")

with main_page:
    info_placeholder = st.expander("INFO : ")

with info_placeholder:

    for key, value in st.session_state.items():
        st.write(f"{key} : {value}")

with header:
    st.markdown("# HEAD")

if delete:
    st.info("Submit updates for saving ones later")  
    st.warning("The bbox hasn't saved yet. Please save it before")   

st.checkbox("Add bbox on the image", key = 'checkbox', value=False)

sidebar = st.sidebar
with sidebar:
    st.markdown("### Preprocess: ")
    contrast = st.slider("Contrast of the image", 0.01, 1.0, 1.0, 0.01)
    brightness = st.slider("Brightness of the image", 0.01, 1.0,0.01, 0.01)