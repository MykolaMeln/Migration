from dash import dcc

from dash import html
import dash_bootstrap_components as dbc

from dash import dash_table as dt
from dash.dependencies import Input, Output, State

from app import app
from model import show_users, add_user, get_data, add_data

layout = dbc.Container([
    html.Br(),
    dbc.Container([
        dcc.Location(id='urlUserAdmin', refresh=True),
        html.H3('Add New User'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Label('Username: '),
                dcc.Input(
                    id='newUsername',
                    className='form-control',
                    n_submit=0,
                    style={'width': '90%'},
                ),
                html.Br(),
                dbc.Label('Password: '),
                dcc.Input(
                    id='newPwd1',
                    type='password',
                    className='form-control',
                    n_submit=0,
                    style={'width': '90%'},
                ),
                html.Br(),
                dbc.Label('Retype New Password: '),
                dcc.Input(
                    id='newPwd2',
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
                    id='newEmail',
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
                html.Button(children='Create User',
                            id='createUserButton',
                            n_clicks=0,
                            type='submit',
                            className='btn btn-primary btn-lg'),
                html.Br(),
                html.Div(id='createUserSuccess')
            ],
                    md=4),
            dbc.Col([], md=4)
        ]),
    ],
                  className='jumbotron'),
    dbc.Container([
        html.H3('View Users'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dt.DataTable(
                    id='users',
                    columns=[{
                        'name': 'ID',
                        'id': 'id'
                    }, {
                        'name': 'Username',
                        'id': 'username'
                    }, {
                        'name': 'Email',
                        'id': 'email'
                    }, {
                        'name': 'Admin',
                        'id': 'admin'
                    }],
                    data=show_users(),
                    style_cell={
                        'background_color': 'rgb(24,26,27)',
                        'text_align': 'center',
                        'border': '1px solid rgb(60,65,68)',
                        'border-radius': '5px',
                    },
                ),
            ],
                    md=12),
        ]),
    ],
                  className='jumbotron'),
    dbc.Container([
        html.H3('View and add data'),
        html.Hr(),
        dt.DataTable(
            id='table-editing-simple',
            columns=[{
                'id': i,
                'name': i
            } for i in [
                'Year', 'Country of Origin Code', 'Country of Asylum Code',
                'Country of Asylum Name', 'Refugees', 'Asylum seekers'
            ]],
            data=get_data(),
            style_cell={
                'background_color': 'rgb(24,26,27)',
                'text_align': 'center',
                'border': '1px solid rgb(60,65,68)',
                'border-radius': '5px',
            },
            editable=False),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Input(id='newyear',
                          className='form-control',
                          n_submit=0,
                          style={'width': '80px'},
                          placeholder='Year')
            ]),
            dbc.Col([
                dcc.Input(id='newcouncode',
                          className='form-control',
                          n_submit=0,
                          style={'width': '150px'},
                          placeholder='Code of Asylum Country')
            ]),
            dbc.Col([
                dcc.Input(id='newcounname',
                          className='form-control',
                          n_submit=0,
                          style={'width': '245px'},
                          placeholder='Name of Asylum Country')
            ]),
            dbc.Col([
                dcc.Input(id='newrefug',
                          className='form-control',
                          n_submit=0,
                          style={'width': '140px'},
                          placeholder='C-nt Refugees')
            ]),
            dbc.Col([
                dcc.Input(id='newasylum',
                          className='form-control',
                          n_submit=0,
                          style={'width': '140px'},
                          placeholder='C-nt Asylum')
            ]),
            dbc.Col([
                html.Button(children='Add data',
                            id='add_data_Button',
                            n_clicks=0,
                            type='submit',
                            className='btn btn-primary btn-lg'),
                html.Div(id='add_data_Success')
            ]),
        ])
    ],
                  className='jumbotron'),
])


#?????????????????? ?????????? ?? csv
@app.callback(Output('add_data_Success', 'children'), [
    Input('add_data_Button', 'n_clicks'),
    Input('newyear', 'n_submit'),
    Input('newcouncode', 'n_submit'),
    Input('newcounname', 'n_submit'),
    Input('newrefug', 'n_submit'),
    Input('newasylum', 'n_submit')
], [
    State('newyear', 'value'),
    State('newcouncode', 'value'),
    State('newcounname', 'value'),
    State('newrefug', 'value'),
    State('newasylum', 'value'),
])
def add_new_data(n_clicks, newyearSubmit, newcouncodeSubmit, newcounnameSubmit,
                 newrefugSubmit, newasylumSubmit, newyear, newcouncode,
                 newcounname, newrefug, newasylum):
    if (n_clicks > 0) or (newyearSubmit > 0) or (newcouncodeSubmit > 0) or \
        (newcounnameSubmit > 0) or (newrefugSubmit > 0) or (newasylumSubmit > 0):

        if newyear and newcouncode and newcounname and newrefug and newasylum != '':
            try:
                add_data(newyear, newcouncode, newcounname, newrefug,
                         newasylum)
                return html.Div(children=['New data added'],
                                className='text-success')

            except Exception as e:
                return html.Div(
                    children=['New data not added: {e}'.format(e=e)],
                    className='text-danger')
        else:
            return html.Div(children=['Invalid details submitted'],
                            className='text-danger')


#?????????????????? email
@app.callback(Output('newUsername', 'className'), [
    Input('createUserButton', 'n_clicks'),
    Input('newUsername', 'n_submit'),
    Input('newPwd1', 'n_submit'),
    Input('newPwd2', 'n_submit'),
    Input('newEmail', 'n_submit')
], [State('newUsername', 'value')])
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


#?????????????????? ????????????
@app.callback(Output('newPwd1', 'className'), [
    Input('createUserButton', 'n_clicks'),
    Input('newUsername', 'n_submit'),
    Input('newPwd1', 'n_submit'),
    Input('newPwd2', 'n_submit'),
    Input('newEmail', 'n_submit')
], [State('newPwd1', 'value'),
    State('newPwd2', 'value')])
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


#???????????????????????? ?????? ?????????? ????????????
@app.callback(Output('newPwd2', 'className'), [
    Input('createUserButton', 'n_clicks'),
    Input('newUsername', 'n_submit'),
    Input('newPwd1', 'n_submit'),
    Input('newPwd2', 'n_submit'),
    Input('newEmail', 'n_submit')
], [State('newPwd1', 'value'),
    State('newPwd2', 'value')])
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


#?????????????????? email
@app.callback(Output('newEmail', 'className'), [
    Input('createUserButton', 'n_clicks'),
    Input('newUsername', 'n_submit'),
    Input('newPwd1', 'n_submit'),
    Input('newPwd2', 'n_submit'),
    Input('newEmail', 'n_submit')
], [State('newEmail', 'value')])
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


#?????????????????? ?? ????????
@app.callback(Output('createUserSuccess', 'children'), [
    Input('createUserButton', 'n_clicks'),
    Input('newUsername', 'n_submit'),
    Input('newPwd1', 'n_submit'),
    Input('newPwd2', 'n_submit'),
    Input('newEmail', 'n_submit')
], [
    State('pageContent', 'children'),
    State('newUsername', 'value'),
    State('newPwd1', 'value'),
    State('newPwd2', 'value'),
    State('newEmail', 'value'),
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
                        return html.Div(children=['New User created'],
                                        className='text-success')
                    except Exception as e:
                        return html.Div(
                            children=['New User not created: {e}'.format(e=e)],
                            className='text-danger')
                else:
                    return html.Div(
                        children=['New Password Must Be Minimum 8 Characters'],
                        className='text-danger')
            else:
                return html.Div(children=['Passwords do not match'],
                                className='text-danger')
        else:
            return html.Div(children=['Invalid details submitted'],
                            className='text-danger')
