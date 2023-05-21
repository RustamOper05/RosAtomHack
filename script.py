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
import warnings

warnings.filterwarnings("ignore")

args = sys.argv
dir_path = args[1]

data = pd.read_csv(dir_path)

data1 = pd.read_csv("cfg.csv")

tab2_fig = px.scatter(
    data1,
    x='Баллы, %',
    y='cnt_users',
    color='cluster',
    hover_data=[
        'Компетенция',
        'ФИО',
    ], size='ФИО'
)

tab2_cont = [
    html.Div('Кластер соревнований'),
    dcc.Graph(id='radar-chart-chart', figure=tab2_fig),
]

options = []
for i in data["family"].values:
    options.append({'label': i, 'value': i})

user_selector = dcc.Dropdown(
    id='user-sel',
    options=options,
    value=data["family"].values[0],
    multi=False
)

tab3_cont = [
    html.Div('Лепестковая диаграмма'),
    dcc.Graph(id='radar-chart', figure=tab2_fig),
    html.Div(user_selector),
    html.Button('Применить изменения', id='apply-button-radar', n_clicks=0),
]

labels_tab1 = ['Пол', 'Категория', 'Место работы', 'Компетенция', 'Баллы, ед.']
names_tab1 = ['Пол', 'Категория', 'Место работы', 'Компетенция', 'Баллы, ед.']

options = []
for i, j in zip(names_tab1, labels_tab1):
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

tab1_cont = [
    html.Div('Кластеры попарных взаимодействий признаков пользователей'),
    dcc.Graph(id='user-chart'),
    html.Div(sel_1),
    html.Div(sel_2),
    html.Button('Применить изменения', id='apply-button', n_clicks=0),
]

poi.renderers.default = 'browser'

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(
    [
        html.H1('Обзор данных'),
        dbc.Tabs(
            [
                dbc.Tab(tab1_cont, label='Пользователи'),
                dbc.Tab(tab2_cont, label='Соревнования'),
                dbc.Tab(tab3_cont, label='Характеристика пользователей')
            ]
        ),
    ], style={'amrgin-left': '80px', 'margin-right': '80px'}
)


@app.callback(
    Output(component_id='user-chart', component_property='figure'),
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
        hover_data=[
            'family',
            'Пол_dec',
            'Роль в мероприятии_dec',
            'Список компетенций_dec',
            'Место работы_dec'
        ]
    )
    return fig1


@app.callback(
    Output(component_id='radar-chart', component_property='figure'),
    [
        Input(component_id='apply-button-radar', component_property='n_clicks')
    ],
    [
        State(component_id='user-sel', component_property='value'),
    ]
)
def upd_list_user_conc_chart(n, value):
    user_data = data[data["family"] == value][["IT", "Физика", "Гуманитарные науки", "Строительство", "Электроника"]]
    user_data_transp = user_data.T.reset_index()
    user_data_transp.columns = ['name', 'rate']
    fig = px.line_polar(user_data_transp, r='rate', theta='name', line_close=True)
    return fig


app.run_server(debug=True, port=8051)
