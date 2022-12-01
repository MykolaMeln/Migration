import dash_bootstrap_components as dbc
from dash import dcc
import dash_html_components as html
from model import build_graph, build_diag_m

from app import app

layout = dbc.Container([
    html.H2('Grafic'),
    html.Hr(),
    dcc.Graph(figure=build_graph()),
    html.Hr(),
    dcc.Graph(figure=build_diag_m())
],
                       className="mt-4")
