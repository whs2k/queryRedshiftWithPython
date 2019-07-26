import pandas as pd
from sqlalchemy.engine import url as sa_url
from sqlalchemy import create_engine
import psycopg2
import datetime
import os

import traceback
import plotly.graph_objs as go
import plotly.offline as pyo
from flask import Flask

schedule_it = True  # Usually its better to save these in a Config.py file
fake = True
d = datetime.datetime.now().strftime("%Y-%m-%d")

def init_data():
    '''

    :return: outputs a file in templates folder called index.html
    '''
    db_connect_url = sa_url.URL(
                drivername='postgresql+psycopg2', #redshift+psycopg2
                username='_probably_something_like_dbname_ro',
                password='_some_random_string',
                host='_something_._something_randomg_.us-east-1.redshift.amazonaws.com',
                port='9128',
                database='_something_meaningful_',
    )
    engine = create_engine(db_connect_url)

    query = '''
         SELECT Date, High, Low 
         FROM table_name
         WHERE ticket_symbol LIKE ('%AMZN%')
              AND Date > TO_DATE('{}', 'YYYY-MM-DD') - 360 
              -- yes it would be easier to use sysdate
         ORDER BY col_date DESC
         '''.format(d).replace('%', '%%')  # watch out for special chars!
    print('Starting Query: ', datetime.datetime.now())
    df = pd.read_sql(sql=query, con=engine)
    print('Finished Query: ', datetime.datetime.now())
    #df.tail()

    if fake:
        df =pd.read_csv('AMZON.csv')

    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)  # df.Date.apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['High'],
        name="High",
        line_color='deepskyblue',
        opacity=0.8))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Low'],
        name="Low",
        line_color='dimgray',
        opacity=0.8))
    fig.update_layout(# xaxis_range=['2016-07-01','2016-12-31'],
        title_text="AMZN")


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

    bootstrap_header = r'''
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.11.0/bootstrap-table.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.9.1/extensions/filter-control/bootstrap-table-filter-control.js"></script>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"/>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.11.0/bootstrap-table.min.css" rel="stylesheet"/>
    <style>body{ margin:0 100; background:whitesmoke; }</style>
    '''

    html_string = '''
     <html>
         <head>
              ''' + bootstrap_header + '''
         </head>
         <body>
             <h1>This is a dashboard!</h1>
             <br>
             <p>This is a description</p>
    <h2>Section 1: Plotly Data!</h2>
             <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#demo1">Click Me For Data</button>
             <div id='demo1' class="collapse">
              ''' + amzn_plotDiv + '''
              <p>ADDITIONAL TEXT HERE</p>
          </div>
             <br>
    <h2>Section 2: Pandas Data!</h2>
             <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#demo1">Click Me For Data</button>
             <div id='demo1' class="collapse">
              ''' + df_htmls + '''
              <p>ADDITIONAL TEXT HERE</p>
          </div>
             <br>
             <br>
             <h2>Data Query:</h2>
             <pre><code style="white-space: pre-wrap"> ''' + query + ''' </code></pre>
             </div>
     </body>
     </html>
     '''.encode('utf-8', errors='replace').decode('utf-8', errors='replace')

    with open(os.path.join(os.getcwd(), 'templates', index.html), 'w') as f:
        f.write(html_string)


def init_site(df, fake=True):
    '''
    inputs a df of data
    :return: html page as index.html
    '''


    @app.route('/', endpoint='funct1' + d)  # Need to rename the endpoint each time otherwise updates will fail
    def first_func():
        return html_string

    @app.route('/egg', endpoint='funct2' + d)
    def first_func():
        return '<h1>Easter Egg!</h1>'

if __name__ == '__main__':
    init_site()
    init_data()
    if schedule_it:
        from apscheduler.schedulers.blocking import BlockingScheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=init_data, trigger="cron", hour=7)  # GMT Time on the Server RN
        scheduler.add_job(func=init_site, trigger="cron", hour=12)
        scheduler.start()

    port = int(os.environ.get('PORT', 5001))
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=port, debug=debug_mode, reloader_interval=60)

    if schedule_it:
        atexit.register(lambda: scheduler.shutdown())  # Shut down the scheduler when exiting the app
