import streamlit as st

from modelui import app, data

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    df_predictions = data.get_predictions()
    df_matches = data.get_matches()

    # SIDEBAR
    st.title("Target image: Shoe for which we are predicting")
    sku = st.sidebar.selectbox("SKU", df_predictions.index.drop_duplicates().to_list())
    app.display_target_shoe(df_predictions.loc[sku])

    # SIDEBAR
    st.title("Target matches: Matched products from previous season")
    app.display_matches(df_matches.query(f"freeport_sku == '{sku}'"))
