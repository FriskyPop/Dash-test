# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go
import os


app = dash.Dash(__name__)
server = app.server

interpolation=np.loadtxt(r'Interpolation STD avec 10 deg X-Y.txt', delimiter = ', ')

filtre = []
for i in range(np.size(interpolation, axis = 0)):
    condition = interpolation[i,3]>-1 and interpolation[i,4]>-1 and interpolation[i,5]>-1 and interpolation[i,6]>-1 and interpolation[i,7]>-1
    if condition == True:
        filtre.append(True)
    else:
        filtre.append(False)
        
interpolation = interpolation[filtre,:]



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='P&W Demo'),

    html.Div(children='''
        Map of the standard deviation of fitted residuals (of a plane) for different angles
    '''),

    dcc.Graph(
        id='interpolation',
        style={'vertical-align':'right'}
        
            ),
            
    dcc.Slider(
        id='RotX',

        min=-10,
        max=10,
        value=0,
        step=1,
        marks={str(item) : str(item) for item in range(-10,11,1)},
        updatemode='drag'
    ),
    
    html.Div(id = 'display-rotationsX', style={'margin-top': 20}),
    
    dcc.Slider(
        id='RotY',

        min=-10,
        max=10,
        value=0,
        step=1,
        marks={str(item) : str(item) for item in range(-10,11,1)},
        updatemode='drag'
    ),
    
    html.Div(id = 'display-rotationsY', style={'margin-top': 20}),
    
    dcc.Slider(
        id='RangeX',

        min=-110,
        max=110,
        value=110,
        step=5,
        marks={str(item) : str(item) for item in range(-110,115,5)},
        updatemode='drag'
    ),
    
    html.Div(id = 'display-rangeX', style={'margin-top': 20}),
])
    
@app.callback([Output('interpolation', 'figure'),Output('display-rotationsX', 'children'), Output('display-rotationsY','children'), Output('display-rangeX','children')],\
               [Input('RotX', 'value'), Input('RotY', 'value'), Input('RangeX','value')])
#               


def update_figure(selected_rotX, selected_rotY, selected_rangeX):
    selection = interpolation[:,0]<selected_rangeX
    interpolationTemp=interpolation[selection,:]
    rotx=np.abs(selected_rotX)
    roty=np.abs(selected_rotY)
    if selected_rotX >=0 and selected_rotY >= 0:
        x = (rotx*interpolationTemp[:,4]+(10-rotx)*interpolationTemp[:,3])/10
        y = (roty*interpolationTemp[:,6]+(10-roty)*interpolationTemp[:,3])/10
        
    if selected_rotX >=0 and selected_rotY <= 0:
        x = (rotx*interpolationTemp[:,4]+(10-rotx)*interpolationTemp[:,3])/10
        y = (roty*interpolationTemp[:,7]+(10-roty)*interpolationTemp[:,3])/10
        
    if selected_rotX <=0 and selected_rotY <= 0:
        x = (rotx*interpolationTemp[:,5]+(10-rotx)*interpolationTemp[:,3])/10
        y = (roty*interpolationTemp[:,7]+(10-roty)*interpolationTemp[:,3])/10
    
    if selected_rotX <=0 and selected_rotY >= 0:
        x = (rotx*interpolationTemp[:,5]+(10-rotx)*interpolationTemp[:,3])/10
        y = (roty*interpolationTemp[:,6]+(10-roty)*interpolationTemp[:,3])/10
        
    couleur = (x+y)/2
    trace = [go.Scatter3d(
        
                                visible=True,
                                x=interpolationTemp[:,0],
                                y=interpolationTemp[:,1],
                                z=interpolationTemp[:,2],
                                mode='markers',
                                marker=dict(                
                                        size=15,
                                        opacity=0.3,
                                        color=couleur,
                                        cmin=0,
                                        cmax=0.08,
                                        colorscale='Rainbow',
                                        showscale=True,
                                        symbol='circle',
                                        colorbar=dict(
                                                title='Standard deviation of fitted residuals',
                                                )
                                        ),
                                text=["std = " + str(item) for item in couleur],
                        
                            )]
    a = {'data': trace,
            'layout': go.Layout(
                                uirevision='dash',
                                title=dict(
                                    text='STD inside volume'
                                ),
                                barmode='overlay',
                                width=1100,
                                height=700,
                                scene=dict(
                                            xaxis=dict(
                                                    title='X',
                                                    titlefont=dict(
                                                            size=18
                                                                ),
                                                    tickfont=dict(
                                                            size=12
                                                                ),
                                                     range=[-110,110]
                                                     ),
                                            yaxis=dict(
                                                    title='Y',
                                                    titlefont=dict(
                                                            size=18
                                                                ),
                                                    tickfont=dict(
                                                            size=12
                                                                ),
                                                     range=[-110,110]
                                                     ),
                                            zaxis=dict(
                                                    title='Z',
                                                    titlefont=dict(
                                                            size=18
                                                                ),
                                                    tickfont=dict(
                                                            size=12
                                                                ),
                                                     range=[-110,110]
                                                     ),
                                            aspectmode='manual',
                                            aspectratio=dict(
                                                    x=1,
                                                    y=1,
                                                    z=1,
                                                    )
                        
                                            )
            )}
    return a, 'Rotation X = {}'.format(selected_rotX), 'Rotation Y = {}'.format(selected_rotY), 'Range X = {}'.format(selected_rangeX)

if __name__ == '__main__':
    app.run_server(debug=True)


if __name__ == '__main__':
    app.run_server(debug=True)
