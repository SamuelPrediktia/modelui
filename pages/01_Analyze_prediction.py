import streamlit as st

from modelui import data, plot


@st.cache_data(persist=True)
def load_thumbnail(sku):
    return data.load_thumbnail(sku=sku)


def display_matches(df_matches):
    for _, match in df_matches.iterrows():
        col_image, col_table = st.columns([1, 4])
        col_image.image([load_thumbnail(sku=match.freeport_sku_match)])

        col_table.write(
            match.drop(["image_uri", "freeport_sku", "closest_image_filename", "brand"])
            .rename(match.freeport_sku_match)
            .to_frame()
            .T.to_html(escape=False),
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    st.set_page_config(layout="wide")

    df_predictions = data.get_predictions()
    df_matches = data.get_matches()

    # SIDEBAR
    st.title("Target image: Shoe for which we are predicting")
    sku = st.sidebar.selectbox("SKU", df_predictions.index.drop_duplicates().to_list())
    prediction = df_predictions.loc[sku]
    matches = df_matches.query(f"freeport_sku == '{sku}'")

    st.dataframe(prediction.rename(sku).to_frame().T)
    col_image, col_plot = st.columns([1, 6])
    col_image.image([load_thumbnail(sku=sku).resize((170, 170))])
    col_plot.plotly_chart(
        plot.plot_prediktion_with_matches(
            prediction=prediction,
            matches=matches,
        ),
        use_container_width=True,
    )

    # SIDEBAR
    st.title("Target matches: Matched products from previous season")
    display_matches(matches)
