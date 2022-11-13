import pickle
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

app = Dash(__name__,
    external_stylesheets=[dbc.themes.SUPERHERO]
)

app.layout = html.Div([
    html.Br(),
    html.Br(),
    dbc.Row(
        html.H1("Interactive Data Viewer"), justify='center'
    ),

    dbc.Row([
        dbc.Col(
            html.H4("Emission")
        ),
        dbc.Col(
            html.H4("Sticker")
        )
    ], justify='center'),

    dbc.Row([
        dbc.Col(
            html.Div(
                [
                    dbc.Input(type="number", min=0, step=1)
                ],
                id="emission_input",
            )
        ),
        dbc.Col(

            html.Div(
                [
                    dbc.Input(type="number", min=0, step=1)
                ],
                id="reception_input",
            )
        )
    ]),



    dcc.Graph(id="plot")



])


@app.callback(
    Output("plot", "figure"),
    Input("emission_input", "value"),
    Input("reception_input", "value")
)

def show_fig(emission_id, sticker_id):
    df = pd.read_pickle('./plots/pickles/'+str(emission_id)+"_"+str(sticker_id)+".pkl")
    time = df['time']
    signal = df['signal']
    ref = df['ref']
    transformed = df['transformed']

    figure = go.Figure(px.line(df, x="time", y="signal",
                  line_shape="spline", template='plotly_dark'))

    return figure

if __name__ == "__main__":
    app.run_server(debug=True)