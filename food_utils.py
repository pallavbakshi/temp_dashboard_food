import os
import pickle
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
import pytz
from food_constants import (
    FOOD_ITEMS,
    FOOD_COLOR,
    COOKED_COLOR,
    COOKED_COLOR_LIGHT,
    PURCHASED_COLOR,
    PURCHASED_COLOR_LIGHT,
    RAW_WASTE_COLOR,
    RAW_WASTE_COLOR_LIGHT,
    RAW_WASTE_COLOR_DARK,
    PURCHASED_COLOR_DARK,
    COOKED_COLOR_DARK,
    USED_COLOR,
    TITLE_FONT_SIZE,
    TEXT_FONT_SIZE,
    PREDICTION_FACTORS,
    PREDICTION_FACTORS_CHEESE,
    PREDICTION_FACTORS_TOMATO,
    PREDICTION_FACTORS_ONION,
    WASTAGE_FACTORS,
    WASTAGE_FACTORS_CHEESE,
    WASTAGE_FACTORS_TOMATO,
    WASTAGE_FACTORS_ONION,
)


def get_color_according_to_timestamp(df, main_color_scheme, light_color_scheme):
    color = df["timestamp"].apply(lambda x: main_color_scheme if x < datetime.utcnow() else light_color_scheme)
    return color


def create_subset_of_samples_based_on_user_inputs(samples_df, item_purchased):
    samples_df = samples_df.loc[samples_df["item_purchased"] == item_purchased]
    samples_df["timestamp"] = pd.to_datetime(samples_df["timestamp"])
    samples_df["color_purchased"] = get_color_according_to_timestamp(samples_df, PURCHASED_COLOR, PURCHASED_COLOR_DARK)
    samples_df["color_raw_waste"] = get_color_according_to_timestamp(samples_df, RAW_WASTE_COLOR, RAW_WASTE_COLOR_DARK)
    samples_df["color_cooked"] = get_color_according_to_timestamp(samples_df, COOKED_COLOR, COOKED_COLOR_DARK)
    samples_df["shape"] = "circle"
    samples_df.loc[samples_df["timestamp"] > datetime.utcnow(), "shape"] = "circle-open-dot"
    return samples_df


def combine_wastage_by_item_purchased(samples_df):
    samples_df = samples_df.groupby("item_purchased")[["raw_material_wasted", "cooked_food_wasted"]].sum().reset_index()
    samples_df["total_wasted"] = samples_df["raw_material_wasted"] + samples_df["cooked_food_wasted"]
    return samples_df


def combine_usage_for_item_purchased(samples_df, item_purchased):
    samples_df = samples_df.loc[samples_df["item_purchased"] == item_purchased][["raw_material_wasted", "cooked_food_wasted", "quantity_purchased"]].agg(["sum", "mean"]).reset_index()
    samples_df["used"] = samples_df["quantity_purchased"] - samples_df["raw_material_wasted"] - samples_df["cooked_food_wasted"]
    samples_df = samples_df.drop("quantity_purchased", axis=1)
    samples_df = pd.melt(samples_df, id_vars=["index"], var_name="food_result_type", value_name="food_result_value")
    samples_df = samples_df.loc[samples_df["index"] == "sum"]
    return samples_df


def load_data() -> pd.DataFrame:
    df = pd.read_csv("./data/inventory_dataframe.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    ticker = pd.read_csv("./data/ticker.csv")
    ticker["timestamp"] = pd.to_datetime(ticker["timestamp"])
    return df, ticker


def create_quantity_statistics_graph(df):
    purchased_trace = create_trace_tm(df, "quantity_purchased", "color_purchased", "Purchased", PURCHASED_COLOR_LIGHT)
    raw_waste_trace = create_trace_tm(df, "raw_material_wasted", "color_raw_waste", "Raw Waste", RAW_WASTE_COLOR_LIGHT)
    cooked_trace = create_trace_tm(df, "cooked_food_wasted", "color_cooked", "Cooked Waste", COOKED_COLOR_LIGHT)
    return create_plot_common(f"{df.iloc[0]['item_purchased']} purchase history over time", purchased_trace, raw_waste_trace, cooked_trace)


def create_trace_tm(raw_samples, feature, color, name, line_color):
    trace = go.Scatter(
        x=raw_samples["timestamp"],
        y=raw_samples[feature],
        marker={
            "size": 11, "color": raw_samples[color], "symbol": raw_samples["shape"]
        },
        name=name,
        mode="lines+markers",
        line={
            "color": line_color
        }
    )
    return trace


def create_plot_common(title, trace_humidex, trace_humidity, trace_temp):
    data = [trace_temp, trace_humidex, trace_humidity]
    layout = dict(
        title=title,
        height=920,
        # width=1200,
        titlefont={"size": TITLE_FONT_SIZE},
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=14, label="14d", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=2, label="2m", step="month", stepmode="backward"),
                        dict(count=3, label="3m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(),
            type="date",
        ),
        yaxis=dict(
            title="Quantity in kg",
        ),
    )
    fig = dict(data=data, layout=layout)

    return fig


def create_prediction_radar_chart(food_item):
    if food_item == "cheese":
        PREDICTION_FACTORS = PREDICTION_FACTORS_CHEESE
    elif food_item == "tomato":
        PREDICTION_FACTORS = PREDICTION_FACTORS_TOMATO
    elif food_item == "onion":
        PREDICTION_FACTORS = PREDICTION_FACTORS_ONION

    data = [
        go.Scatterpolar(
            r=list(PREDICTION_FACTORS.values()),
            theta=list(PREDICTION_FACTORS.keys()),
            fill='toself',
            name='Prediction Factors',
            fillcolor=PURCHASED_COLOR,
            line=dict(
                color=PURCHASED_COLOR_DARK
            )
        ),
    ]

    layout = go.Layout(
        title="Inventory Forecast Variables",
        titlefont={"size": TITLE_FONT_SIZE},
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=False
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


def create_wastage_radar_chart(food_item):
    if food_item == "cheese":
        WASTAGE_FACTORS = WASTAGE_FACTORS_CHEESE
    elif food_item == "tomato":
        WASTAGE_FACTORS = WASTAGE_FACTORS_TOMATO
    elif food_item == "onion":
        WASTAGE_FACTORS = WASTAGE_FACTORS_ONION

    data = [
        go.Scatterpolar(
            r=list(WASTAGE_FACTORS.values()),
            theta=list(WASTAGE_FACTORS.keys()),
            fill='toself',
            name='Wastage Factors',
            fillcolor=RAW_WASTE_COLOR,
            line=dict(
                color=RAW_WASTE_COLOR_DARK
            )
        ),
    ]

    layout = go.Layout(
        title="Raw Food Wastage Variables",
        titlefont={"size": TITLE_FONT_SIZE},
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=False
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


def create_combine_item_wastage_graph(samples_df):
    samples_df["colors"] = samples_df["item_purchased"].apply(lambda x: FOOD_COLOR.get(x))
    trace = go.Pie(labels=samples_df["item_purchased"], values=samples_df["total_wasted"],
                   hoverinfo='value', textinfo='label+percent',
                   pull=0.04,
                   hole=0.35,
                   textfont=dict(size=TEXT_FONT_SIZE),
                   marker=dict(colors=samples_df["colors"], line=dict(color='#000000', width=2)))
    layout = go.Layout(
        title="Wastage per item (kg)",
        titlefont={"size": TITLE_FONT_SIZE},
        showlegend=False
    )

    fig = go.Figure(data=[trace], layout=layout)

    return fig


def decide_color_based_on_food_result(food_result_type):
    if food_result_type == "used":
        return USED_COLOR
    elif food_result_type == "raw_material_wasted":
        return RAW_WASTE_COLOR
    elif food_result_type == "cooked_food_wasted":
        return COOKED_COLOR
    else:
        return PURCHASED_COLOR


def choose_name_based_on_food_result(food_result_type):
    if food_result_type == "used":
        return "Used"
    elif food_result_type == "raw_material_wasted":
        return "Raw Material Wasted"
    elif food_result_type == "cooked_food_wasted":
        return "Cooked Food Wasted"
    else:
        return "Total Purchase"


def create_per_item_usage_graph(samples_df, item_purchased):
    samples_df["colors"] = samples_df["food_result_type"].apply(lambda x: decide_color_based_on_food_result(x))
    samples_df["food_result_type_name"] = samples_df["food_result_type"].apply(lambda x: choose_name_based_on_food_result(x))
    trace = go.Pie(labels=samples_df["food_result_type_name"], values=samples_df["food_result_value"],
                   hoverinfo='value', textinfo='label+percent',
                   pull=0.04,
                   hole=0.35,
                   textfont=dict(size=TEXT_FONT_SIZE),
                   marker=dict(colors=samples_df["colors"], line=dict(color='#000000', width=2)))
    layout = go.Layout(
        title=f"Usage/Wastage of {item_purchased}",
        titlefont={"size": TITLE_FONT_SIZE},
        showlegend=False
    )

    fig = go.Figure(data=[trace], layout=layout)

    return fig


def create_purchase_item_ticker(samples_df, item_purchased):
    samples_df["color"] = USED_COLOR
    samples_df["shape"] = "circle"
    trace = create_trace_tm(samples_df, item_purchased, "color", item_purchased.title(), USED_COLOR)
    layout = go.Layout(
        title=f"Current price of {item_purchased}",
        titlefont={"size": TITLE_FONT_SIZE},
        showlegend=False,
        yaxis={
            "title": "Price in HKD"
        }

    )
    fig = go.Figure(data=[trace], layout=layout)
    return fig
