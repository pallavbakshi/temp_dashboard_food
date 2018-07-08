# -*- coding: utf-8 -*-
import sys
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime

from food_utils import (
    load_data,
    create_quantity_statistics_graph,
    create_prediction_radar_chart,
    create_wastage_radar_chart,
    create_combine_item_wastage_graph,
    create_per_item_usage_graph,
    create_purchase_item_ticker,
    combine_wastage_by_item_purchased,
    combine_usage_for_item_purchased,
    create_subset_of_samples_based_on_user_inputs)
from food_constants import FOOD_ITEMS, PURCHASED_COLOR, RAW_WASTE_COLOR

samples_df, ticker = load_data()

if samples_df is None:
    print("Loading dataframe failed. Specify the correct folder.")
    sys.exit(1)

food_types = [{"label": food, "value": food} for food in FOOD_ITEMS]

app = dash.Dash()
app.css.append_css({'external_url': 'https://codepen.io/plotly/pen/EQZeaW.css'})


app.layout = html.Div(
    style={"background-color": "white"},
    children=[
        html.Div(
            children=[
                html.Div(
                    style={"margin-bottom": "8px", "width": "20vw"},
                    className="4 columns",
                    children=[
                        html.Div(
                            children=dcc.Dropdown(
                                id="food-item",
                                options=food_types,
                                placeholder="item",
                                searchable=True,
                                value=FOOD_ITEMS[0]
                            )
                        ),
                    ]
                ),
                html.Div(
                    style={"margin-bottom": "8px", "width": "35vw", "color": PURCHASED_COLOR, "font-size": 20},
                    className="4 columns",
                    children=[
                        html.Div(
                            id="prediction-tip"
                            )
                    ]
                ),
                html.Div(
                    style={"margin-bottom": "8px", "width": "35vw", "color": RAW_WASTE_COLOR, "font-size": 20},
                    className="4 columns",
                    children=[
                        html.Div(
                            id="storage-tip"
                        ),
                    ]
                )
            ],
            className="row"
        ),

        # dcc.Interval(id='my-interval', interval=1*10**3, n_intervals=0),
        html.Div(
            [
                html.Div([dcc.Graph(id="quantity-stats")], className="6 columns", style={"margin": 0, "width": "60vw", "height": "100vh"}),
                html.Div([dcc.Graph(id="prediction-radar-chart"),],
                         style={"margin": 0, "width": "36vw"},
                         className="3 columns"
                         ),
                html.Div(
                    [dcc.Graph(id="wastage-radar-chart")],
                    style={"margin": 0, "width": "36vw"},
                    className="3 columns"
                ),
            ],
            style={"height": "100vh"},
            className="row"
        ),
        html.Div(
            style={"height": "50vh"},
            className="row",
            children=[
                html.Div([dcc.Graph(id="combine-item-wastage-pie-chart")], style={"width": "30vw"}, className="4 columns"),
                html.Div([dcc.Graph(id="per-item-usage-pie-chart")], style={"width": "30vw",}, className="4 columns"),
                html.Div([dcc.Graph(id="purchase-item-price-ticker")], style={"width": "30vw"}, className="4 columns"),
            ]
        )
    ]
)


@app.callback(
    dash.dependencies.Output("quantity-stats", "figure"),
    [
        dash.dependencies.Input("food-item", "value"),
    ],
)
def update_graph(food_item):
    if food_item is not "" and food_item is not None:
        new_samples = create_subset_of_samples_based_on_user_inputs(samples_df, food_item)

        if not new_samples.empty:
            figure = create_quantity_statistics_graph(new_samples)
            return figure
        else:
            print("Empty")
            go.Figure()
    else:
        return go.Figure()


@app.callback(
    dash.dependencies.Output("prediction-radar-chart", "figure"),
    [
        dash.dependencies.Input("food-item", "value"),
    ],
)
def update_graph(food_item):
    if food_item is not "" and food_item is not None:
        return create_prediction_radar_chart(food_item)
    else:
        return go.Figure()


@app.callback(
    dash.dependencies.Output("wastage-radar-chart", "figure"),
    [
        dash.dependencies.Input("food-item", "value"),
    ],
)
def update_graph(food_item):
    if food_item is not "" and food_item is not None:
        return create_wastage_radar_chart(food_item)
    else:
        return go.Figure()


@app.callback(
    dash.dependencies.Output("combine-item-wastage-pie-chart", "figure"),
    [
        dash.dependencies.Input("food-item", "value"),
    ],
)
def update_graph(food_item):
    if food_item is not "" and food_item is not None:
        new_samples = combine_wastage_by_item_purchased(samples_df)

        if not new_samples.empty:
            figure = create_combine_item_wastage_graph(new_samples)
            return figure
        else:
            go.Figure()
    else:
        return go.Figure()


@app.callback(
    dash.dependencies.Output("per-item-usage-pie-chart", "figure"),
    [
        dash.dependencies.Input("food-item", "value"),
    ],
)
def update_graph(food_item):
    if food_item is not "" and food_item is not None:
        new_samples = combine_usage_for_item_purchased(samples_df, food_item)

        if not new_samples.empty:
            figure = create_per_item_usage_graph(new_samples, food_item)
            return figure
        else:
            go.Figure()
    else:
        return go.Figure()


@app.callback(
    dash.dependencies.Output("purchase-item-price-ticker", "figure"),
    [
        dash.dependencies.Input("food-item", "value"),
    ],
    # events=[dash.dependencies.Event('my-interval', 'interval'),]
)
def update_graph(food_item,):
    if food_item is not "" and food_item is not None:
        new_samples = ticker.loc[ticker["timestamp"] <= datetime.utcnow()]
        if not new_samples.empty:
            figure = create_purchase_item_ticker(new_samples, food_item)
        else:
            figure = go.Figure()
        return figure
    else:
        return go.Figure()


@app.callback(
    dash.dependencies.Output("prediction-tip", "children"),
    [
        dash.dependencies.Input("food-item", "value"),
    ],
)
def update_graph(food_item,):
    if food_item is not "" and food_item is not None:
        if food_item == "cheese":
            tip = "Buy 12 kg less Cheese."
        elif food_item == "tomato":
            tip = "Buy 10 kg less Tomato."
        elif food_item == "onion":
            tip = "Buy 14 kg less Onion."
        else:
            tip = ""
        return tip
    else:
        return ""


@app.callback(
    dash.dependencies.Output("storage-tip", "children"),
    [
        dash.dependencies.Input("food-item", "value"),
    ],
)
def update_graph(food_item,):
    if food_item is not "" and food_item is not None:
        print(RAW_WASTE_COLOR)
        if food_item == "cheese":
            tip = "Store cheese at 16 Degree Celsius with 42 Humidity."
        elif food_item == "tomato":
            tip = "Store tomato at 23 Degree Celsius with 49 Humidity."
        elif food_item == "onion":
            tip = "Store onion at 25 Degree Celsius with 49 Humidity."
        else:
            tip = ""
        return tip
    else:
        return ""


if __name__ == "__main__":
    app.run_server(debug=True)