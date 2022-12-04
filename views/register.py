from dash import dcc
from dash import html
from dash import dash_table as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from views import login

from app import app
from model import add_user

layout = dbc.Container([
    html.Br(),
    dbc.Container([
        dcc.Location(id='urlRegister', refresh=True),
        html.H3('Register'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Label('Username: '),
                dcc.Input(
                    id='Username',
                    className='form-control',
                    n_submit=0,
                    style={'width': '90%'},
                ),
                html.Br(),
                dbc.Label('Password: '),
                dcc.Input(
                    id='Pwd1',
                    type='password',
                    className='form-control',
                    n_submit=0,
                    style={'width': '90%'},
                ),
                html.Br(),
                dbc.Label('Retype New Password: '),
                dcc.Input(
                    id='Pwd2',
                    type='password',
                    className='form-control',
                    n_submit=0,
                    style={'width': '90%'},
                ),
                html.Br(),
            ],
                    md=4),
            dbc.Col([
                dbc.Label('Email: '),
                dcc.Input(
                    id='Email',
                    className='form-control',
                    n_submit=0,
                    style={'width': '90%'},
                ),
                html.Br(),
                dbc.Label('Admin? '),
                dcc.Dropdown(
                    id='admin',
                    style={
                        'width': '200px',
                        'background-color': 'rgb(24,26,27)',
                        'border': '1px solid rgb(60,65,68)',
                        'border-radius': '1px',
                        'color': '#7B8A8B',
                    },
                    options=[
                        {
                            'label': 'Yes',
                            'value': 1
                        },
                        {
                            'label': 'No',
                            'value': 0
                        },
                    ],
                    value=0,
                    clearable=False,
                ),
                html.Br(),
                html.Br(),
                html.Button(children='Register',
                            id='RegisterButton',
                            n_clicks=0,
                            type='submit',
                            className='btn btn-primary btn-lg'),
                html.Br(),
                html.Div(id='RegisterSuccess')
            ],
                    md=4),
            dbc.Col([], md=4)
        ]),
    ],
                  className='jumbotron')
])


@app.callback(Output('Username', 'className'), [
    Input('RegisterButton', 'n_clicks'),
    Input('Username', 'n_submit'),
    Input('Pwd1', 'n_submit'),
    Input('Pwd2', 'n_submit'),
    Input('Email', 'n_submit')
], [State('Username', 'value')])
def validateUsername(n_clicks, usernameSubmit, newPassword1Submit,
                     newPassword2Submit, newEmailSubmit, newUsername):

    if (n_clicks > 0) or (usernameSubmit > 0) or (newPassword1Submit > 0) or \
        (newPassword2Submit > 0) or (newEmailSubmit > 0):

        if newUsername == None or newUsername == '':
            return 'form-control is-invalid'
        else:
            return 'form-control is-valid'
    else:
        return 'form-control'


#Валідація паролю
@app.callback(Output('Pwd1', 'className'), [
    Input('RegisterButton', 'n_clicks'),
    Input('Username', 'n_submit'),
    Input('Pwd1', 'n_submit'),
    Input('Pwd2', 'n_submit'),
    Input('Email', 'n_submit')
], [State('Pwd1', 'value'), State('Pwd2', 'value')])
def validatePassword1(n_clicks, usernameSubmit, newPassword1Submit,
                      newPassword2Submit, newEmailSubmit, newPassword1,
                      newPassword2):

    if (n_clicks > 0) or (usernameSubmit > 0) or (newPassword1Submit > 0) or \
        (newPassword2Submit > 0) or (newEmailSubmit > 0):

        if newPassword1 == newPassword2 and len(newPassword1) > 7:
            return 'form-control is-valid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'


#Попередження про введення паролю
@app.callback(Output('Pwd2', 'className'), [
    Input('RegisterButton', 'n_clicks'),
    Input('Username', 'n_submit'),
    Input('Pwd1', 'n_submit'),
    Input('Pwd2', 'n_submit'),
    Input('Email', 'n_submit')
], [State('Pwd1', 'value'), State('Pwd2', 'value')])
def validatePassword2(n_clicks, usernameSubmit, newPassword1Submit,
                      newPassword2Submit, newEmailSubmit, newPassword1,
                      newPassword2):

    if (n_clicks > 0) or (usernameSubmit > 0) or (newPassword1Submit > 0) or \
        (newPassword2Submit > 0) or (newEmailSubmit > 0):

        if newPassword1 == newPassword2 and len(newPassword2) > 7:
            return 'form-control is-valid'
        else:
            return 'form-control is-invalid'
    else:
        return 'form-control'


#Валідація email
@app.callback(Output('Email', 'className'), [
    Input('RegisterButton', 'n_clicks'),
    Input('Username', 'n_submit'),
    Input('Pwd1', 'n_submit'),
    Input('Pwd2', 'n_submit'),
    Input('Email', 'n_submit')
], [State('Email', 'value')])
def validateEmail(n_clicks, usernameSubmit, newPassword1Submit,
                  newPassword2Submit, newEmailSubmit, newEmail):

    if (n_clicks > 0) or (usernameSubmit > 0) or (newPassword1Submit > 0) or \
        (newPassword2Submit > 0) or (newEmailSubmit > 0):

        if newEmail == None or newEmail == '':
            return 'form-control is-invalid'
        else:
            return 'form-control is-valid'
    else:
        return 'form-control'


#Запис в базу
@app.callback(Output('RegisterSuccess', 'children'), [
    Input('RegisterButton', 'n_clicks'),
    Input('Username', 'n_submit'),
    Input('Pwd1', 'n_submit'),
    Input('Pwd2', 'n_submit'),
    Input('Email', 'n_submit')
], [
    State('pageContent', 'children'),
    State('Username', 'value'),
    State('Pwd1', 'value'),
    State('Pwd2', 'value'),
    State('Email', 'value'),
    State('admin', 'value')
])
def createUser(n_clicks, usernameSubmit, newPassword1Submit,
               newPassword2Submit, newEmailSubmit, pageContent, newUser,
               newPassword1, newPassword2, newEmail, admin):
    if (n_clicks > 0) or (usernameSubmit > 0) or (newPassword1Submit > 0) or \
        (newPassword2Submit > 0) or (newEmailSubmit > 0):

        if newUser and newPassword1 and newPassword2 and newEmail != '':
            if newPassword1 == newPassword2:
                if len(newPassword1) > 7:
                    try:
                        add_user(newUser, newPassword1, newEmail, admin)
                        return login.layout
                    except Exception as e:
                        return html.Div(
                            children=['Register failed: {e}'.format(e=e)],
                            className='text-danger')
                else:
                    return html.Div(
                        children=['Password Must Be Minimum 8 Characters'],
                        className='text-danger')
            else:
                return html.Div(children=['Passwords do not match'],
                                className='text-danger')
        else:
            return html.Div(children=['Invalid details submitted'],
                            className='text-danger')
