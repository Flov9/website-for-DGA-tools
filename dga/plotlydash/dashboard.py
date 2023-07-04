import calendar

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, dcc
from .dash import Dash
import plotly.graph_objs as go

from .data import create_dataframe


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix="/graph/",
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
        ],
    )

    # def init_dynamic_list():
    #     # TODO (enhance): Dynamic dropdown list
    #     df = create_dataframe()
    #     tf_dropdown = []
    #     for tf in df["transformerList"]:
    #         tf_dropdown.append({"label": tf, "value": tf})
    #     return tf_dropdown
    # testtttt
    def init_month_list():
        month_dropdown = []
        mth = 0
        while mth < 12:
            month_name = calendar.month_name[mth+1]
            month_dropdown.append({"label": month_name, "value": mth+1})
            mth += 1
        return month_dropdown

    # Create Dash Layout using Bootstrap components
    dash_app.layout = dbc.Container([
        dbc.Row([
            html.H4(
                "Graph of Gas Concentration against Date",
                className="text-center mt-3 mb-5"
            )
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Pick Transformer", className="text-secondary text-center d-block fs-5 my-1"),
                dcc.Dropdown(
                    id="tx_dropdown",
                    options=[
                        {"label": "TX1", "value": "TX1"},
                        {"label": "TX2", "value": "TX2"},
                        {"label": "TX3", "value": "TX3"},
                        {"label": "TX4", "value": "TX4"},
                        {"label": "TX5", "value": "TX5"}
                    ],
                    # options=init_dynamic_list(),
                    value="TX1",
                    clearable=False
                )
            ], width=2),
            dbc.Col([
                dbc.Label("Pick Month", className="text-secondary text-center d-block fs-5 my-1"),
                dcc.Dropdown(
                    id="month_dropdown",
                    # options=[
                    #     {"label": "January", "value": "1"},
                    #     {"label": "February", "value": "2"},
                    #     {"label": "March", "value": "3"},
                    #     {"label": "April", "value": "4"},
                    #     {"label": "May", "value": "5"},
                    #     {"label": "June", "value": "6"},
                    #     {"label": "July", "value": "7"},
                    #     {"label": "August", "value": "8"},
                    #     {"label": "September", "value": "9"},
                    #     {"label": "October", "value": "10"},
                    #     {"label": "November", "value": "11"},
                    #     {"label": "December", "value": "12"},
                    # ],
                    options=init_month_list(),
                    value=init_month_list()[0]["value"],
                    clearable=False
                )
            ], width=2),
            dbc.Col([
                dbc.Label("Pick Gas", className="text-secondary text-center d-block fs-5 my-1"),
                dcc.Dropdown(
                    id="gas_dropdown",
                    options=[
                        {"label": "Acetylene", "value": "Acetylene"},
                        {"label": "Carbon Dioxide", "value": "Carbon Dioxide"},
                        {"label": "Carbon Monoxide", "value": "Carbon Monoxide"},
                        {"label": "Ethane", "value": "Ethane"},
                        {"label": "Ethylene", "value": "Ethylene"},
                        {"label": "Hydrogen", "value": "Hydrogen"},
                        {"label": "Methane", "value": "Methane"},
                    ],
                    value="Acetylene",
                    clearable=False
                )
            ], width=2)
        ], justify="evenly"),
        # dbc.Row([
        #     html.H2(
        #         "Transformer TX1",
        #         className="text-primary text-center fs-5 fw-3 mt-10",
        #         id="tfHeader"
        #     )
        # ]),
        dbc.Row([
            dcc.Graph(id="time-series-graph"),
        ]),
        # dbc.Row(
        #     [
        #         html.Div(
        #             dcc.RangeSlider(
        #                 min=None,
        #                 max=None,
        #                 value=None,
        #                 id="time-series-slider",
        #             ),
        #             style={
        #                 "width": "100%",
        #                 "height": "50px",
        #                 "margin-top": "1rem",
        #                 "padding": "0rem .3rem .3rem .3rem",
        #             },
        #         ),
        #     ]
        # ),
        dbc.Row([
            dbc.Alert(
                "Drag across the graph to zoom in. Drag across the timeline to jump back/ahead. Double click to reset.",
                color="info",
                className="mt-2 text-center",
            )
        ]),
    ])
    # dash_app.scripts.append_script("""
    #     document.addEventListener('DOMContentLoaded', function() {
    #         var tfDropdown = document.querySelector('#tx_dropdown');
    #         var tfHeader = document.querySelector('#tfHeader');
    #         tfDropdown.addEventListener('change', function(event) {
    #             tfHeader.textContent = 'Transformer ' + tfDropdown.value;
    #         });
    #     });
    # """)

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(
        Output("time-series-graph", "figure"),
        [Input("tx_dropdown", "value"), Input("month_dropdown", "value"), Input("gas_dropdown", "value")]
    )
    def update_output(tx_dropdown, month_dropdown, gas_dropdown):
        df = create_dataframe()
        # Filter the DataFrame based on the selected fault type
        filtered_graph = df[["Transformer", "Date", "Gas Concentration % ({})".format(gas_dropdown)]]
        # filtered_graph = df.loc[:, ["Date ({})".format(month_dropdown), "Gas Concentration ({})".format(gas_dropdown)]]

        print(filtered_graph)
        for i in range(0, len(filtered_graph)):
            if filtered_graph.at[i, "Transformer"] != tx_dropdown:
                filtered_graph.drop(i, inplace=True)
                continue
            if filtered_graph.at[i, "Date"].month != month_dropdown:
                filtered_graph.drop(i, inplace=True)
                continue

        colors = {"text": "#7FDBFF"}

        # Create the time series graph
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=filtered_graph["Date"],
                y=filtered_graph["Gas Concentration % ({})".format(gas_dropdown)],
                mode="lines+markers",
                name="Fault Type",
                marker=dict(color='#bc2128', line=dict(color='#bc2128')),
                # hovertemplate="Record: %{customdata[0]}<br>"
                # + "Acetylene: %{customdata[1]}%<br>"
                # + "Hydrogen: %{customdata[2]}%<br>"
                # + "Methane: %{customdata[3]}%<br>"
                # + "Ethylene: %{customdata[4]}%<br>"
                # + "Ethane: %{customdata[5]}%<br>"
                # + "Carbon dioxide: %{customdata[6]}%<br>"
                # + "Carbon monoxide: %{customdata[7]}%<br>",
                # customdata=df[
                #     [
                #         "Record",
                #         "Acetylene",
                #         "Hydrogen",
                #         "Methane",
                #         "Ethylene",
                #         "Ethane",
                #         "Carbon dioxide",
                #         "Carbon monoxide",
                #     ]
                # ].values,
            )
        )

        fig.layout.plot_bgcolor = "#f8f8f8"

        fig.update_traces(
            marker=dict(size=14, line=dict(width=2), symbol="circle"),
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Gas Concentration % ({})".format(gas_dropdown),
            xaxis=dict(
                showline=True,
                showgrid=True,
            ),
            font=dict(size=14),
            hovermode="closest",
        )

        return fig

    # @dash_app.callback(
    #     [
    #         Output("time-series-slider", "min"),
    #         Output("time-series-slider", "max"),
    #         Output("time-series-slider", "value"),
    #         Output("time-series-slider", "marks"),
    #     ],
    #     [Input("fault-type-dropdown", "value")],
    # )
    # def update_slider_properties(value):
    #     df = create_dataframe()

    #     min_value = df["Timestamp"].min()
    #     max_value = df["Timestamp"].max()
    #     value_range = [min_value, max_value]
    #     marks = {str(timestamp): timestamp for timestamp in df["Timestamp"].unique()}

    #     return min_value, max_value, value_range, marks

    # @dash_app.callback(
    #     Output("time-series-graph", "figure"),
    #     [Input("fault-type-dropdown", "value"), Input("time-series-slider", "value")],
    # )
    # def update_output(fault_type, time_range):
    #     df = create_dataframe()

    #     # Filter the DataFrame based on the selected fault type and time range
    #     filtered_df = df[
    #         (df["Timestamp"] >= time_range[0]) & (df["Timestamp"] <= time_range[1])
    #     ]
    #     filtered_df = filtered_df[["Timestamp", "Fault Type ({})".format(fault_type)]]

    #     # Create the time series graph
    #     # ... (rest of the code remains the same)
