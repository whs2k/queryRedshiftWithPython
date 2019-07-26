import pandas as pd

from sqlalchemy.engine import url as sa_url
from sqlalchemy import create_engine
import psycopg2
import datetime
import os

fn = 'AMZN.csv'
df = pd.read_csv(fn)

import traceback
import plotly.graph_objs as go
import plotly.offline as pyo

from flask import Flask


def init():

schedule_it = True #Define variables

amzn_plotDiv= pyo.plot(figure_or_data=fig,
                             config={"displayModeBar": False},
                             show_link=False,
                             include_plotlyjs=False,
                             output_type='div') \
                     .replace('height: 100%; width: 100%', 'height: 50%; width: 100%')

df_html = df.to_html() \
   .replace('<table border="1" class="dataframe">','<table class="table table-hover table-condensed table-striped">')
for col in df_reg.columns.tolist():
    df_html = df_html.replace('<th>'+col+'</th>','<th data-sortable="true" data-filter-control="input">'+col+'</th>')