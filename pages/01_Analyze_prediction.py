import streamlit as st

from modelui import app, data

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    df_predictions = data.get_predictions()

    # SIDEBAR
    st.title("Freeport image: What we are looking for")
    sku = st.sidebar.selectbox("SKU", df_predictions.index.drop_duplicates().to_list())

    # Freeport image
    prediction = df_predictions.loc[sku]
    app.display_target_shoe(prediction)
