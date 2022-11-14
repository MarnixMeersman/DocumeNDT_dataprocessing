from backend_code.prophet import prophet

from dash import Dash, dcc, html, Input, Output, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from main import locations
### ADJUST THESE VALUES! These are VELOCITIES
lower_limit_unreasonable = 400
upper_limit_unreasonable = 5000

def get_unreasonable():
    df = pd.read_csv('results/velocities.csv', header=None)
    rows, columns = len(df.axes[0]), len(df.axes[1])

    e_lst = []
    r_lst = []
    for row in range(rows):
        for col in range(columns):
            array = np.asarray(df)

            number = float(array[row][col])
            if lower_limit_unreasonable <= number <= upper_limit_unreasonable:
                pass
            else:
                e_lst.append(locations[row])
                r_lst.append(col)

    str_lst = []
    for e, r in zip(e_lst, r_lst):
        string = str(e)+'_'+str(r)
        str_lst.append(string)
    return str_lst





app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])


app.layout = dbc.Container([
    html.Br(),
    html.H1('DocumeNDT Manual Signal Checker'),
    html.Br(),
    dbc.Row([
        dbc.Col(html.H4('Emission ID')),
        dbc.Col(html.H4('Reception ID'))
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Input(id='emission_id', step=1, value=11, type='number')
        ),
        dbc.Col(
            dbc.Input(id='reception_id', step=1, value=0, type='number')
        ),
    ]),
    html.Br(),

    dcc.Graph(id="graph"),
    dbc.Row(dbc.Col([
        dbc.Button("Predict Vibrometer State with ML (2min)", id='prophet', n_clicks=0,
                   color="primary",
                   outline=False)], width='auto'),
        justify='center'
    ),
    html.Br(),
    dbc.Row(dbc.Col(
        html.H6("Unreasonable points that should be checked are: " + str(get_unreasonable())),
    )),
    html.Br(),
    dbc.Row(html.H4("Manual Adjustments")),
    dbc.Row([
        dbc.Col(html.H5("t0 [s]")),
        dbc.Col(html.H5("t1 [s]")),
        dbc.Col(html.H5(" ")),
    ]),

    dbc.Row([
            dbc.Col(dbc.Input(id='new_t0', value=None, type='number')),
            dbc.Col(dbc.Input(id='new_t1', value=None, type='number')),
            dbc.Col([dbc.Button("Adjust time differences", id='adjust', n_clicks=0,
                   color="success",
                   outline=True), html.Div(id='adjust-output')]),
        ])

])


@app.callback(
    Output("graph", "figure"),
    Input("prophet", "n_clicks"),
    Input("emission_id", "value"),
    Input("reception_id", "value"))

def update_line_chart(btn, e_id, r_id):
    if "prophet" == ctx.triggered_id:
        print("clicked")
        e = str(e_id)
        r = str(r_id)
        df = pd.read_pickle('./plots/pickles/' + e + '_' + r + '.pkl')
        prophet(df, e_id, r_id) #This writes a column extra

        e, r = str(e_id), str(r_id)
        df = pd.read_pickle('./plots/pickles/' + e + '_' + r + '.pkl')
        index0 = int(df['index0'][0])
        index1 = int(df['index1'][0])
        time = np.asarray(df['time'])
        deltat = time[index1]-time[index0]
        symbol = '\u0394 T = ' + str(deltat) + ' [s]'
        t0 = 't0 = ' + str(time[index0]) + ' [s]'
        t1 = 't1 = ' + str(time[index1]) + ' [s]'
        # df = prophet(df, e_id, r_id)[2]
        lines_to_hide = ["og_signal", "boxcar+hanning", "trigger_line", "max_line"]
        fig = px.line(df,
            x="time", y=df.columns[1:9], title=f'Normalised Voltages\n {symbol}\n {t0}\n {t1}')
        fig.add_vline(x=time[index0], line_dash="dot", line_color="black")
        fig.add_vline(x=time[index1], line_dash="dot", line_color="black")
        fig.for_each_trace(lambda trace: trace.update(visible="legendonly") if trace.name in lines_to_hide else ())
        fig.update_layout(xaxis_range=[0, 0.02])

    else:
        e, r = str(e_id), str(r_id)
        df = pd.read_pickle('./plots/pickles/' + e + '_' + r + '.pkl')
        index0 = int(df['index0'][0])
        index1 = int(df['index1'][0])
        time = np.asarray(df['time'])
        deltat = time[index1]-time[index0]
        symbol = '\u0394 T = ' + str(deltat) + ' [s]'
        t0 = 't0 = ' + str(time[index0]) + ' [s]'
        t1 = 't1 = ' + str(time[index1]) + ' [s]'
        # df = prophet(df, e_id, r_id)[2]
        lines_to_hide = ["og_signal", "prediction", "boxcar+hanning", "trigger_line", "max_line"]
        fig = px.line(df,
            x="time", y=df.columns[1:9], title=f'Normalised Voltages\n {symbol}\n {t0}\n {t1}')
        fig.add_vline(x=time[index0], line_dash="dot", line_color="black")
        fig.add_vline(x=time[index1], line_dash="dot", line_color="black")
        fig.for_each_trace(lambda trace: trace.update(visible="legendonly") if trace.name in lines_to_hide else ())
        fig.update_layout(xaxis_range=[0, 0.02])
    return fig

@app.callback(
    Output("adjust-output", "children"),
    Input("adjust", "n_clicks"),
    Input("emission_id", "value"),
    Input("reception_id", "value"),
    Input("new_t0", "value"),
    Input("new_t1", "value")
)
def adjust(btn, e_id, r_id, new_t0, new_t1):
    e, r = str(e_id), str(r_id)
    df_loc = pd.read_pickle('./plots/pickles/' + e + '_' + r + '.pkl')

    index0 = int(df_loc['index0'][0])
    index1 = int(df_loc['index1'][0])
    time = np.asarray(df_loc['time'])

    if new_t0 is None:
        t0 = float(time[index0])
    else:
        t0 = float(new_t0)



    if new_t1 is None:
        t1 = float(time[index1])
    else:
        t1 = float(new_t1)


    dt = t1-t0

    if "adjust" == ctx.triggered_id:

        df_loc["time"] = time
        df_glob = pd.read_csv("results/time_differences.csv")
        e_loc = locations.index(e_id)
        r_loc = r_id
        df_glob.iloc[e_loc][r_loc] = dt
        df_loc.to_pickle('./plots/pickles/' + e + '_' + r + '.pkl')
        message = "Saved. \u0394T = " + str(dt) + "[s]"
    else:
        message = " "

    return message







if __name__ == '__main__':
    app.run_server(debug=False)