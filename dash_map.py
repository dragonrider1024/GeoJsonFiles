import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import geopandas as gpd
import os
from django_plotly_dash import DjangoDash
import json

mapbox_access_token = 'pk.eyJ1Ijoid2VueHUxMDI0IiwiYSI6ImNqdXR2ODQwNDBjNjE0NHFpa3FhMGs2enEifQ.QQlvoH5ChTs7AMCTgP1nHw'

#app = DjangoDash('SimpleExample')
app = dash.Dash()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.layout = html.Div([
    dcc.RadioItems(
        id='dropdown-color',
        options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
        value='red'
    ),
    html.Div(id='output-color',children=""),
    dcc.RadioItems(
        id='dropdown-size',
        options=[{'label': i, 'value': j} for i, j in [('L','large'), ('M','medium'), ('S','small')]],
        value='medium'
    ),
    html.Div(id='output-size',children=""),
    dcc.Graph(
        figure = go.Figure(
            data = [
                dict(type='scattermapbox',
                lat= (40.7272,),
                lon= (-73.99,),
                mode='markers',
                marker=dict(size=0.5, color= '#a490bd'),
                showlegend=False,
                hoverinfo='text'
            )],
            layout = go.Layout(
                title = 'Average Sold Home Price for Towns in Greater Boston Area',
                margin = go.layout.Margin(l=40,r=0,t=40,b=30),
                autosize=True,
                hovermode='closest',
                mapbox = dict(
                    accesstoken = mapbox_access_token,
                    bearing = 0,
                    style="light",
                    pitch=0,
                    zoom=11.0,
                    center=dict(lat=42.361145,lon=-71.057083),
                    layers = [
                    dict(
                        type="fill",
                        sourcetype="geojson",
                        #source="https://raw.githubusercontent.com/dragonrider1024/GeoJsonFiles/master/ACTON.json",
                        source="https://raw.githubusercontent.com/dragonrider1024/GeoJsonFiles/master/ACTON.json",
                        opacity=0.8,
                        color='rgba(163,22,19,0.8)',
                        below="water",
                        )
                    ]
                    )
                )
            ),
        style={'height':600},
        id='town_sold_home_price'
        )
])

@app.callback(
    dash.dependencies.Output('output-color', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value')])
def callback_color(dropdown_value):
    return "The selected color is %s." % dropdown_value

@app.callback(
    dash.dependencies.Output('output-size', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value'),
     dash.dependencies.Input('dropdown-size', 'value')])
def callback_size(dropdown_color, dropdown_size):
    return "The chosen T-shirt is a %s %s one." %(dropdown_size,
                                                  dropdown_color)
if __name__ == "__main__":
    app.run_server(debug=True)
