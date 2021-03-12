#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon 14 Jan 2021

@author: Ziba
"""

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Load both red and white wine datasets
df_red= pd.read_csv('winequality-red.csv',  sep=';')
df_white = pd.read_csv('winequality-white.csv',  sep=';')
df_red['color']= 0
df_white['color']=1
df_complete = df_red.append(df_white) 

app.layout = html.Div([

        html.Div([
        dcc.Markdown('''Assignment 1, Ziba'''),
        ], 
        style={'marginLeft': 40, 'marginRight': 40, 'marginTop': 10, 'marginBottom': 10, 
               'backgroundColor':'#F7FBFE',
               'border': 'thin lightgrey dashed', 'padding': '6px 0px 0px 8px'}),

    
            html.Div([
        dcc.Dropdown(
            id='xaxis-column',
            options=[{'label': i, 'value': i} for i in df_complete.columns],
            value='citric acid'
        ),
        ],style={'marginLeft': 100, 'marginRight': 50, 'marginTop': 10, 'marginBottom': 10,
                 'width': '40%','display': 'inline-block'}),
        html.Div([
        dcc.Dropdown(
            id='yaxis-column',
            options=[{'label': i, 'value': i} for i in df_complete.columns],
            value='volatile acidity'),
        ],style={'marginLeft': 50, 'marginRight': 100, 'marginTop': 10, 'marginBottom': 10,
                 'width': '40%','display': 'inline-block'}),
        
        html.Div([ 
        dcc.Graph(id='scatergraph_red_wine'),
        ],style={'marginLeft': 50, 'marginRight': 100, 'marginTop': 10, 'marginBottom': 10,
                 'width': '40%','display': 'inline-block'}),
        html.Div([ 
        dcc.Graph(id='scatergraph_white_wine'),
        ],style={'marginLeft': 100, 'marginRight': 50, 'marginTop': 10, 'marginBottom': 10,
                 'width': '40%','display': 'inline-block'}),
    
        html.Div([
            html.Div(
                [
                    html.H6("""Data sampling ratio""",
                            style={'margin-right': '2em'})
                ],
            ),
        
        dcc.Input(
            id='sample',
            type='number',
            value=80
        ),
        ],style={'marginLeft': 100, 'marginRight': 50, 'marginTop': 10, 'marginBottom': 10,
                 'width': '40%'}), 
        html.Div([ 
            html.Div(
                [
                    html.H6("""Select Maximum Quality""",
                            style={'margin-left': '2em'})
                ],
            ),
        
        dcc.Slider(
            id='quality--slider',
            min=df_complete['quality'].min(),
            max=df_complete['quality'].max(),
            value=df_complete['quality'].max(),
            marks={str(quality): str(quality) for quality in range(df_complete['quality'].min(),df_complete['quality'].max())},
            step=None
        ),
        ],style={'marginLeft': 50, 'marginRight': 50,'width': '90%'}),
])

@app.callback(
    Output('scatergraph_red_wine', 'figure'),
    Input('sample', 'value'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('quality--slider', 'value'))
def update_graph(sample, xaxis_column_name, yaxis_column_name, quality_value):
    df_quality = df_complete[df_complete['quality'] <= quality_value]
    rate = sample/100
    df_sampled = df_quality.sample(frac= rate, replace=True, random_state=1)
    dff_graph_red=df_sampled.loc[df_sampled['color'] == 0]
    fig_red = px.scatter(dff_graph_red, x=dff_graph_red[xaxis_column_name],
                     y=dff_graph_red[yaxis_column_name],color='quality',
                     hover_name='quality',title='Red Wine',trendline="ols")

    fig_red.update_layout(margin={'l': 20, 'b': 20, 't': 40, 'r': 20}, hovermode='closest',transition_duration=500)

    fig_red.update_xaxes(title=xaxis_column_name)

    fig_red.update(layout=dict(title=dict(x=0.5)))  

    fig_red.update_yaxes(title=yaxis_column_name)

    return fig_red

@app.callback(
    Output('scatergraph_white_wine', 'figure'),
    Input('sample', 'value'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('quality--slider', 'value'))
def update_graph(sample,xaxis_column_w_name, yaxis_column_w_name, quality_value):
    df_quality = df_complete[df_complete['quality'] <= quality_value]
    rate = sample/100
    df_sampled = df_quality.sample(frac= rate, replace=True, random_state=1)
    dff_graph_white =df_sampled.loc[df_sampled ['color'] == 1]
    fig_white =  px.scatter(dff_graph_white, x=dff_graph_white[xaxis_column_w_name],
                     y=dff_graph_white[yaxis_column_w_name],color='quality',
                     hover_name='quality',title='White Wine', trendline="ols")
    fig_white.update_layout(margin={ 'l': 20,'b': 20, 't': 40, 'r':20}, hovermode='closest',transition_duration=500)
    
    fig_white.update(layout=dict(title=dict(x=0.5)))

    fig_white.update_xaxes(title=xaxis_column_w_name)
        
    fig_white.update_yaxes(title=yaxis_column_w_name)

    return fig_white




if __name__ == '__main__':
    app.run_server(debug=True)
