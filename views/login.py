from dash import dcc
from dash import html
from dash import dash_table as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from views import register
from app import app, User
from flask_login import login_user
from werkzeug.security import check_password_hash

layout = dbc.Container([
    html.Br(),
    dbc.Container([
        dcc.Location(id='urlLogin', refresh=True),
        html.Div([
            dbc.Container(
                html.Img(src='/assets/migration_3.svg', className='center'), ),
            html.Br(),
            dbc.Container(id='loginType',
                          children=[
                              dcc.Input(placeholder='Enter your username',
                                        type='text',
                                        id='usernameBox',
                                        className='form-control',
                                        n_submit=0,
                                        style={
                                            'margin-left': '25%',
                                            'width': '50%',
                                        }),
                              html.Br(),
                              dcc.Input(placeholder='Enter your password',
                                        type='password',
                                        id='passwordBox',
                                        className='form-control',
                                        n_submit=0,
                                        style={
                                            'margin-left': '25%',
                                            'width': '50%',
                                        }),
                              html.Br(),
                              html.Button(children='Login',
                                          n_clicks=0,
                                          type='submit',
                                          id='loginButton',
                                          style={
                                              'margin-left': '45%',
                                          },
                                          className='btn btn-primary btn-lg'),
                              html.Br(),
                          ],
                          className='form-group'),
        ]),
    ],
                  className='jumbotron')
])


#Перехід на сторінку, якшо всі лані вірні
@app.callback(Output('urlLogin', 'pathname'), [
    Input('loginButton', 'n_clicks'),
    Input('usernameBox', 'n_submit'),
    Input('passwordBox', 'n_submit')
], [State('usernameBox', 'value'),
    State('passwordBox', 'value')])
def sucess(n_clicks, usernameSubmit, passwordSubmit, username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return '/page1'
        else:
            pass
    else:
        pass


#Попередження про невірні дані
@app.callback(Output('usernameBox', 'className'), [
    Input('loginButton', 'n_clicks'),
    Input('usernameBox', 'n_submit'),
    Input('passwordBox', 'n_submit')
], [State('usernameBox', 'value'),
    State('passwordBox', 'value')])
def update_output(n_clicks, usernameSubmit, passwordSubmit, username,
                  password):
    if (n_clicks > 0) or (usernameSubmit > 0) or (passwordSubmit) > 0:
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return 'form-control'
            else:
                return 'form-control is-invalid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'


#Попередження про різні дані
@app.callback(Output('passwordBox', 'className'), [
    Input('loginButton', 'n_clicks'),
    Input('usernameBox', 'n_submit'),
    Input('passwordBox', 'n_submit')
], [State('usernameBox', 'value'),
    State('passwordBox', 'value')])
def update_output(n_clicks, usernameSubmit, passwordSubmit, username,
                  password):
    if (n_clicks > 0) or (usernameSubmit > 0) or (passwordSubmit) > 0:
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return 'form-control'
            else:
                return 'form-control is-invalid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'
