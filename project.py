# Import package
import dash #website dashboard
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd # import data set.
import plotly.graph_objs as go # plot charts

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/unemployment.csv') # March2000 - March2020 unemployment ratio with different race and sex categories.
df2 = pd.read_csv('../Datasets/unemployment_state.csv')# March 2020, different state unemployment ratio.



app = dash.Dash() # create a website dashboard object

#Bar Chart
# Sorting values and select first 20 highest unemployment ratio
new_df = df.sort_values(by=['Total'], ascending=[False]).head(20)

data_bar = [go.Bar(x=new_df['Month'], y=new_df['Total'])]

# Muiltiple Line chart plot the total unemployment ratio, teenager and different races together.
data_mutiLine = [go.Scatter(x=df['Month'], y=df['Total'], mode='lines', name='Total Ratio'),
        go.Scatter(x=df['Month'], y=df['White'], mode='lines', name='White people Ratio'),
        go.Scatter(x=df['Month'], y=df['16 to 19 years old'], mode='lines', name='Teenager Ratio'),
        go.Scatter(x=df['Month'], y=df['Black or African American'], mode='lines', name='Black and African American Ratio'),
        go.Scatter(x=df['Month'], y=df['Asian'], mode='lines', name='Asian Ratio'),
        go.Scatter(x=df['Month'], y=df['Hispanic or Latino'], mode='lines', name='Hispanic and Latino Ratio')]

# StackBar put different races together.
trace1 = go.Bar(x=df['Month'], y=df['White'], name='White',
                marker={'color': '#58508d'})
trace2 = go.Bar(x=df['Month'], y=df['Black or African American'], name='African American',
                marker={'color': '#008080'})
trace3 = go.Bar(x=df['Month'], y=df['Asian'], name='Asian',
                marker={'color': '#2A0A12'})
trace4 = go.Bar(x=df['Month'], y=df['Hispanic or Latino'], name='Hispanic',
                marker={'color': '#B45F04'})

data_stackbarchart = [trace1, trace2, trace3,trace4]

#HeatMap: the unemployment ratio for women and 20 years and over
data_heat = [go.Heatmap(x=df['Month'],
                   y=df['Women, 20 years and over'],
                   z=df['Total'].values.tolist(),
                   colorscale='Jet')]

##bubble chart for total unemployment ratio
trace5 = go.Scatter(
    x=df['Month'],
    y=df['Total'],
    mode='markers',
    name='Ratio',
    text= df['Total'],
    marker=dict(
        size= 10,
        line=dict(
        width=2
        ),
    )
)

data_bubble = [trace5]

# Choropleth Map which shows different states unemployment ratio at march 2020.
data_map = [go.Choropleth(
    locations=df2['code'],
    z=df2['rate'].astype(float),
    locationmode='USA-states',
    colorscale='Reds',
    autocolorscale=False,
    marker_line_color='white', # line markers between states
    colorbar_title="Unemployment rate"
)]


# Layout for the website dashboard.
app.layout = html.Div(children=[
    html.H1(children='Unemployment Rate Visualization', # The title
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('March 2020 - March 2000, Total unemployment Ratio ', style={'textAlign': 'center'}), #sub-title
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Line chart', style={'color': '#df1e56'}),
    html.Div('This Line chart represent the number of Unemployment ratio from March 2000 - March 2020'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a category', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-continent',
        options=[ # interactive line charts
            {'label': 'Total', 'value': 'Total'},
            {'label': '16 to 19 years old,White', 'value': '16 to 19 years old,White'},
            {'label': 'Asian', 'value': 'Asian'},
            {'label': 'Black or African American', 'value': 'Black or African American'},
            {'label': 'Hispanic or Latino', 'value': 'Hispanic or Latino'},
            {'label': 'Men, 20 years and over', 'value': 'Men, 20 years and over'},
            {'label': 'Women, 20 years and over', 'value': 'Women, 20 years and over'}
        ],
        value='Total'
    ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This line chart represent number of Unemployment ratio from March 2000 - March 2020.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_mutiLine,
                  'layout': go.Layout(
                      title='Unemployment ratio From March 2000 - March 2020 ',
                      xaxis={'title': 'Month'}, yaxis={'title': 'Ratio of unemployment'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represent the Unemployment ratio from March 2000 - March 2020'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_bubble,
                  'layout': go.Layout(title='Unemployment ratio from March 2000 - March 2020',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Unemployment Ratio'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represent the Unemployment ratio from March 2000 - March 2020'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Unemployment ratio from March 2000 - March 2020',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Unemployment Ratio'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'This heat bar chart represent the Women Unemployment in USA from 2000-2020'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_heat,
                  'layout': go.Layout(title='Total Unemployment (Women) from 2000-2020',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Unemployment Ratio'})
              }
              ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the Top 20 Unemployment Ratio in USA between 2000-2020'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bar,
                  'layout': go.Layout(title='Top 20 Unemployment Ratio From 2000-2020',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Unemployment Ratio'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('United States Choropleth Map', style={'color': '#df1e56'}),
    html.Div(
        'This United States Choroplethc Map shows the unemployment rate in March 2020'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_map,
                  'layout': go.Layout(
                                      title_text='Unemployment rate in March 2020.',
                                        geo = dict(
                                                scope='usa',
                                                projection=go.layout.geo.Projection(type = 'albers usa'),
                                                showlakes=True, # lakes
                                                lakecolor='rgb(255, 255, 255)')
                                      )
              }
              )
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-continent', 'value')])


def update_figure(selected_continent):
    data = [go.Scatter(y=df[selected_continent], x=df['Month'], mode='lines', name='Total Ratio')]
    return {'data': data, 'layout': go.Layout(title='Unemployment Ratio by '+selected_continent,
                                                                   xaxis={'title': 'Month'},
                                                                   yaxis={'title': 'Number of unemployment ratio'})}


if __name__ == '__main__':
    app.run_server()
