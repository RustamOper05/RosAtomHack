import sys
import os
import pandas as pd
import numpy as np
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as poi
from dash.dependencies import Input, Output, State
# args = sys.argv
# dir_path = args[1]


data = pd.read_csv(r"C:\Users\sahab\Desktop\csv\user_cluster.csv")
data_comp = pd.read_csv(r"C:\Users\sahab\Desktop\rijulya_ya_tebya_lublyu.csv")


# print(data)
# bins = [
#     0, 0.8, 1.2, 100
# ]
#
# names = [
#     'small', 'sim', 'bigger'
# ]
#
# bins_temp = [0, 200, 400, 500, 5000]
# tp_labels = ['low', 'opt', 'hig', 'ext']
# data['temp'] = pd.cut(data['TPLANET'], bins_temp, labels=tp_labels)
#
# rp_bins = [0, 0.5, 2, 4, 100]
# rp_labels = ['low', 'opt', 'hig', 'ext']
# data['grav'] = pd.cut(data['RPLANET'], rp_bins, labels=rp_labels)
#
# data['StarSize'] = pd.cut(data['RSTAR'], bins, labels=names)

# data['status'] = np.where((data['temp'] == 'opt') & (data['grav'] == 'opt'), 'intrest', None)
# data.loc[:, 'status'] = np.where((data['temp'] == 'opt') & (data['grav'].isin(['low', 'hig'])), 'chal', data['status'])
# data.loc[:, 'status'] = np.where((data['grav'] == 'opt') & (data['temp'].isin(['low', 'hig'])), 'chal', data['status'])
# data['status'] = data['status'].fillna('ext')

# fig = px.scatter(data, x='RPLANET', y='RSTAR', z='TPLANET')
tab1_cont = [
    html.Div('Попарные взаимодействия'),
    dcc.Graph(id='dist-temp-chart'),
]

labels = ['Пол', 'Категория', 'Место работы', 'Компетенция', 'Баллы, ед.']
names = ['Пол', 'Категория', 'Место работы', 'Компетенция', 'Баллы, ед.']

options = []
for i, j in zip(names, labels):
    options.append({'label': i, 'value': j})

sel_1 = dcc.Dropdown(
    id='chart-sel1',
    options=options,
    value='Категория',
    multi=False
)

sel_2 = dcc.Dropdown(
    id='chart-sel2',
    options=options,
    value='Компетенция',
    multi=False
)

poi.renderers.default = 'browser'

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(
    [
        html.H1('Дашборды'),
        html.Div('select planet main semi-axis'),
        html.Div(sel_1),
        html.Div(sel_2),
        html.Button('Apply', id='apply-button', n_clicks=0),
        html.Div(dcc.Graph(id='chart1'))
    ], style={'amrgin-left': '80px', 'margin-right': '80px'}
)


@app.callback(
    Output(component_id='chart1', component_property='figure'),
    [
        Input(component_id='apply-button', component_property='n_clicks')
    ],
    [
        State(component_id='chart-sel1', component_property='value'),
        State(component_id='chart-sel2', component_property='value')
    ]
)
def upd_list_temp_chart(n, value1, value2):
    # print(value1, value2)
    fig1 = px.scatter(
        data,
        x=value1,
        y=value2,
        color='clusters',
        # labels={
        #     'family': 'ФИО',
        #     '': '',
        #     '': '',
        # }
    )
    return fig1


app.run_server(debug=True, port=8051)
