import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from model import build_diagram, Diagram, build_diagram
import plotly.express as px
import plotly.graph_objects as go
from app import app

df = Diagram.int_st
years = df.Year.unique()

layout = dbc.Container([
    html.Label("Select Year", htmlFor="years"),
    dcc.Slider(
        min=int(years[0]),
        max=int(years[-1]),
        step=1,
        value=int(years[0]),
        id="years",
        marks={
            i: '{}'.format(i)
            for i in range(int(years[0]), int(years[-1]))
        },
    ),
    html.Hr(),
    dcc.Graph(id="graph", style={
        'height': '650px',
        'width': '100%'
    }),
    html.Br(),
],
                       className='graphs2')


@app.callback(Output("graph", "figure"), Input("years", "value"))
def update_figure(yr):

    return build_diagram(yr)