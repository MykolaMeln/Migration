import dash_bootstrap_components as dbc
from dash import dcc
import dash_html_components as html
from model import build_diagram
from app import app

layout = dbc.Container(
    [html.H2('Diagram'),
     html.Hr(),
     dcc.Graph(figure=build_diagram())],
    className="mt-4")
