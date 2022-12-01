# index page
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app, server
from flask_login import logout_user, current_user
from views import login, error, page1, page2, profile, register, user_admin

navBar = dbc.Navbar(
    id='navBar',
    children=[],
    sticky='top',
    color='primary',
    className='navbar navbar-expand-lg navbar-dark bg-primary',
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([navBar, html.Div(id='pageContent')])
],
                      id='table-wrapper')


#Якщо не авторизований повертає на сторінку входу
@app.callback(Output('pageContent', 'children'), [Input('url', 'pathname')])
def displayPage(pathname):
    if pathname == '/':
        if current_user.is_authenticated:
            return page1.layout
        else:
            return login.layout

    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return login.layout
        else:
            return login.layout

    if pathname == '/page1':
        if current_user.is_authenticated:
            return page1.layout
        else:
            return login.layout

    if pathname == '/page2':
        if current_user.is_authenticated:
            return page2.layout
        else:
            return login.layout

    if pathname == '/profile':
        if current_user.is_authenticated:
            return profile.layout
        else:
            return login.layout

    if pathname == '/register':
        if current_user.is_authenticated:
            return profile.layout
        else:
            return register.layout
    if pathname == '/admin':
        if current_user.is_authenticated:
            if current_user.admin == 1:
                return user_admin.layout
            else:
                return error.layout
        else:
            return login.layout

    else:
        return error.layout


#Показувати навігацію, лиш коли авторизований
@app.callback(Output('navBar', 'children'), [Input('pageContent', 'children')])
def navBar(input1):
    if current_user.is_authenticated:
        if current_user.admin == 1:
            navBarContents = [
                dbc.NavItem(
                    dbc.NavbarBrand(
                        html.Img(src='/assets/migration_3.svg',
                                 height="75px"))),
                dbc.NavItem(html.H5(dbc.NavLink('Graph', href='/page1'))),
                dbc.NavItem(html.H5(dbc.NavLink('Diagram', href='/page2'))),
                dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label=current_user.username,
                    children=[
                        dbc.DropdownMenuItem(html.H5('Profile'),
                                             href='/profile'),
                        dbc.DropdownMenuItem(html.H5('Admin'), href='/admin'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem(html.H6('Logout'),
                                             href='/logout'),
                    ],
                ),
            ]
            return navBarContents

        else:
            navBarContents = [
                dbc.NavItem(
                    dbc.NavbarBrand(
                        html.Img(src='/assets/migration_3.svg',
                                 height="75px"))),
                dbc.NavItem(html.H5(dbc.NavLink('Graph', href='/page1'))),
                dbc.NavItem(html.H5(dbc.NavLink('Diagram', href='/page2'))),
                dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label=current_user.username,
                    children=[
                        dbc.DropdownMenuItem('Profile', href='/profile'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem('Logout', href='/logout'),
                    ],
                ),
            ]
            return navBarContents

    else:
        navBarContents = [
            dbc.NavItem(
                dbc.NavbarBrand(
                    html.Img(src='/assets/migration_3.svg', height="75px"))),
            dbc.NavItem(html.H5(dbc.NavLink('Login', href='/'))),
            dbc.NavItem(html.H5(dbc.NavLink('Register', href='/register'))),
        ]
    return navBarContents


if __name__ == '__main__':
    app.run_server(debug=True)
