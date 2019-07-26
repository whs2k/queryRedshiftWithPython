import traceback
import plotly.graph_objs as go
import plotly.offline as pyo


schedule_it = True #Define variables
df_html = df.to_html() \
   .replace('<table border="1" class="dataframe">','<table class="table table-hover table-condensed table-striped">')
for col in df_reg.columns.tolist(): 
    df_html = df_html.replace('<th>'+col+'</th>','<th data-sortable="true" data-filter-control="input">'+col+'</th>')
