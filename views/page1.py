import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from model import build_graph, build_diag_m

from app import app

layout = dbc.Container([
    dbc.Container([
        html.Br(),
        html.H2('Grafic of migration from 2019 to 2021'),
        html.Br(),
        dcc.Graph(figure=build_graph(),
                  style={
                      'height': '650px',
                      'width': '100%'
                  })
    ],
                  className="graphs2"),
    html.Hr(),
    dbc.Container([
        html.H2('Grafic of migration from 2019 to 2021'),
        html.Hr(),
        dcc.Graph(figure=build_diag_m(),
                  style={
                      'height': '650px',
                      'width': '100%'
                  })
    ],
                  className="graphs2"),
], )
