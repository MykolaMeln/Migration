from sqlalchemy import Table
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from config import engine

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import iplot
import csv

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


userTable = Table('user', User.metadata)


def create_user_table():
    User.metadata.create_all(engine)


def add_user(username, password, email, admin):
    hashed_password = generate_password_hash(password,
                                             method='pbkdf2:sha1',
                                             salt_length=8)

    insert_stmt = userTable.insert().values(username=username,
                                            email=email,
                                            password=hashed_password,
                                            admin=admin)

    conn = engine.connect()
    conn.execute(insert_stmt)
    conn.close()


def update_password(username, password):
    hashed_password = generate_password_hash(password,
                                             method='pbkdf2:sha1',
                                             salt_length=8)

    update = userTable.update().\
        values(password=hashed_password).\
        where(userTable.c.username==username)

    conn = engine.connect()
    conn.execute(update)
    conn.close()


def show_users():
    select_stmt = select([
        userTable.c.id, userTable.c.username, userTable.c.email,
        userTable.c.admin
    ])

    conn = engine.connect()
    results = conn.execute(select_stmt)

    users = []

    for result in results:
        users.append({
            'id': result[0],
            'username': result[1],
            'email': result[2],
            'admin': str(result[3])
        })

    conn.close()

    return users


class Migr():
    migr_19 = pd.read_csv('data/migration_by_region_19.csv')
    migr_20 = pd.read_csv('data/migration_by_region_20.csv')
    migr_21 = pd.read_csv('data/migration_by_region_21.csv')

    migr_19 = migr_19.drop(0)
    migr_20 = migr_20.drop(0)
    migr_21 = migr_21.drop(0)


def build_graph():
    fig = go.Figure()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(y=Migr.migr_19['All total emigrants'],
                   x=Migr.migr_19['Region'],
                   text=Migr.migr_19['All total emigrants'],
                   mode='lines',
                   name="2019"),
        secondary_y=False,
    )

    fig.add_trace(go.Scatter(y=Migr.migr_20['All total emigrants'],
                             x=Migr.migr_20['Region'],
                             text=Migr.migr_20['All total emigrants'],
                             mode='lines',
                             name="2020"),
                  secondary_y=True)
    fig.add_trace(go.Scatter(y=Migr.migr_21['All total emigrants'],
                             x=Migr.migr_21['Region'],
                             text=Migr.migr_21['All total emigrants'],
                             mode='lines',
                             name="2021"),
                  secondary_y=True)
    fig.update_layout(height=700,
                      width=1000,
                      title_text="Count of emigrants in 2019-2021 years",
                      template="plotly_dark")

    return fig


def build_diag_m():
    fig = go.Figure()
    fig.add_trace(
        go.Bar(y=Migr.migr_19['All total emigrants'],
               x=Migr.migr_19['Region'],
               text=Migr.migr_19['All total emigrants'],
               name="2019",
               marker_color="#BDB246"))
    fig.add_trace(
        go.Bar(
            y=Migr.migr_20['All total emigrants'],
            x=Migr.migr_20['Region'],
            text=Migr.migr_20['All total emigrants'],
            name="2020",
            marker_color="#007C77",
            textposition="inside",
        ))
    fig.add_trace(
        go.Bar(y=Migr.migr_21['All total emigrants'],
               x=Migr.migr_21['Region'],
               text=Migr.migr_21['All total emigrants'],
               name="2021",
               marker_color="#CA2E55"))
    fig.update_layout(height=800,
                      width=1800,
                      title_text="Count of emigrants in 2019-2021 years",
                      template="plotly_dark")
    fig.update_traces(textfont=dict(family="Arial", size=20, color="white"))

    return fig


class Diagram():
    int_st = pd.read_csv('data/end_year_population_totals_originating_ukr.csv')

    int_st.drop(labels=0,
                axis=0,
                index=None,
                columns=None,
                level=None,
                inplace=False,
                errors='raise')

    int_st = int_st[int_st['Refugees'] != "0"]
    int_st = int_st[int_st.Year > "2013"]


def build_diagram():
    fig = go.Figure()
    fig = px.bar(Diagram.int_st,
                 x="Country of Asylum Code",
                 y='Refugees',
                 color='Year',
                 text='Year',
                 title="Refugees in countries")
    fig.update_layout(height=700, width=1500, template="plotly_dark")

    return fig