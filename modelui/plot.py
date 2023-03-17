import numpy as np
import pandas as pd
import plotly.express as px
import scipy.stats as stats


def plot_prediktion_with_matches(prediction, matches, suffix: str):
    xmin = 0
    xmax = (
        max(
            prediction[f"recommended_sales_over_margin{suffix}"],
            prediction[f"prediction_over_margin{suffix}"],
            prediction.stock_in,
            matches[f"recommended_sales_over_margin{suffix}"].max(),
        )
        * 1.1
    )

    matches = matches.assign(
        label=lambda df: df.apply(
            lambda row: f"{int(row.order)}-{row.freeport_sku_match}: {row.score: 0.2f}",
            axis=1,
        ),
    )

    if prediction[f"alpha{suffix}"] != 0:
        scale = 1 / prediction[f"beta{suffix}"]
        matches = matches.assign(
            pdf=lambda df: stats.gamma.pdf(
                df[f"recommended_sales_over_margin{suffix}"],
                a=prediction[f"alpha{suffix}"],
                scale=scale,
            ),
        )

    else:
        matches = matches.assign(pdf=0)

    fig = px.scatter(
        matches,
        x=f"recommended_sales_over_margin{suffix}",
        y="pdf",
        hover_data=["freeport_sku_match", "score", "order", "brand"],
        hover_name="label",
        text="label",
        symbol_sequence=["x"],
    ).update_traces(mode="markers+text", marker_size=10, textposition="top center")

    if prediction[f"alpha{suffix}"] != 0:
        df_dist = (
            pd.Series(np.linspace(xmin, xmax, 1000), name="x")
            .to_frame()
            .assign(
                y=lambda df: stats.gamma.pdf(
                    df.x, a=prediction[f"alpha{suffix}"], scale=scale
                )
            )
        )

        fig.add_trace(
            px.line(
                df_dist,
                x="x",
                y="y",
                hover_data={
                    "x": False,
                    "y": False,
                },
            ).data[0]
        )
    fig.add_vrect(
        x0=xmin,
        x1=prediction[f"recommended_sales_over_margin{suffix}"],
        annotation_text=f"underbuy: {prediction[f'underweight{suffix}'].round()}",
        annotation_position="bottom left",
        fillcolor="orange",
        opacity=0.25,
        line_width=0,
    )
    fig.add_vrect(
        x0=prediction[f"recommended_sales_over_margin{suffix}"],
        x1=xmax,
        annotation_text=f"overbuy: {prediction[f'overweight{suffix}'].round()}",
        annotation_position="bottom right",
        fillcolor="blue",
        opacity=0.25,
        line_width=0,
    )
    fig.add_vline(
        x=prediction[f"recommended_sales_over_margin{suffix}"],
        line_width=3,
        line_dash="dash",
        line_color="green",
        annotation_text=f"Recommended Sales: {prediction[f'recommended_sales_over_margin{suffix}']}",
        annotation_position="top right",
        annotation_textangle=90,
    )
    fig.add_vline(
        x=prediction[f"prediction_over_margin{suffix}"],
        line_width=2,
        line_dash="dot",
        line_color="red",
        annotation_text=f"Prediktion: {prediction[f'prediction_over_margin{suffix}']}",
        annotation_position="top right",
        annotation_textangle=90,
    )
    fig.add_vline(
        x=prediction.stock_in,
        line_width=2,
        line_dash="dot",
        line_color="red",
        annotation_text=f"Human: {prediction.stock_in}",
        annotation_position="top right",
        annotation_textangle=90,
    )
    return fig
