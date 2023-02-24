import streamlit as st

from modelui import data


@st.cache_data(persist=True)
def load_thumbnail(sku):
    return data.load_thumbnail(sku=sku)


def display_target_shoe(prediction):
    sku = prediction.name
    col_image, col_table = st.columns([1, 4])
    col_image.image([load_thumbnail(sku=sku).resize((170, 170))])
    col_table.write(
        prediction.rename(sku).to_frame().T.to_html(escape=False),
        unsafe_allow_html=True,
    )
