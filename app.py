import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
from vega_datasets import data
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.FLATLY])
server = app.server

app.title = 'Dash app with pure Altair HTML'

############ Function for World map and histogram #########

def make_map(year = 1940):
    map_and_bar_df = pd.read_csv('data/clean_map_and_bar_data.csv', index_col=0)

    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 500
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 10,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 18,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 32,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default

    # json base country map data 
    country_map = alt.topo_feature(data.world_110m.url, 'countries')
      
    
    quote_yr = str(year)
    
    #add rank column
    plot_df = map_and_bar_df
    plot_df = plot_df.loc[plot_df['child']=='all']
    plot_df = plot_df.dropna(subset=[quote_yr])
    plot_df['Rank'] = plot_df[quote_yr].rank(ascending = 0)
    plot_df.drop_duplicates(subset='countryname', keep='first', inplace=True)
    
    selection = alt.selection_multi(fields = ['countryname'], resolve='global')
    map_chart = alt.Chart(country_map).mark_geoshape(
        stroke='white',
        fill='lightgray'
    ).encode(
        color=alt.condition(selection,
                           alt.Color(quote_yr, type='quantitative',
                                    scale=alt.Scale(domain=[0, 1])),
                           alt.value('lightgray'),
                           legend=alt.Legend(title="EMI")),
        tooltip = [
            alt.Tooltip('countryname:N', title="country"),
            alt.Tooltip(f'{year}:Q', title="EMI"),
            alt.Tooltip('Rank:N', title="Global Rank")
        ]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(plot_df,'country_num', [quote_yr, 'countryname', 'Rank'])
    ).properties(
        width=00
    ).project(
        'equirectangular'
    ).properties(title=f'Global Education Mobility Index: {year}',
                height=325,
                width=650
    ).add_selection(
                    selection
    )#.interactive()

    
    bar_chart_data = plot_df
    
    bar_chart = alt.Chart(bar_chart_data.loc[bar_chart_data['child'] == 'all']).mark_bar().encode(
        alt.X(f'{quote_yr}:Q', title="Education Mobility Index"),
        alt.Y('countryname', axis=None, title='',
        sort=alt.EncodingSortField(field='Rank',
                                   order="ascending")),
        #color=alt.Color('incgroup2'),
        color=alt.condition(selection,
                            'incgroup2',
                            alt.value('lightgray'),
                            legend=alt.Legend(title="")
        ),
        tooltip = [
            alt.Tooltip('countryname:N', title="country"),
            alt.Tooltip(f'{quote_yr}:Q', title="EMI"),
            alt.Tooltip('Rank:N', title="Global Rank")
        ]
    ).properties(title=f'{year} Global Ranking', height = 315, width = 175).add_selection(selection)
      
    
    map_and_bar = (map_chart | bar_chart).configure_legend(
        orient="right",
        labelFontSize=14)
    
    return map_and_bar

######### Function for Line graph(s) ###########

def make_line_chart(country_list = ['Africa', 'Canada', 'Developing economies']):
    compare_chart_df = pd.read_csv('data/clean_comparison_chart_data.csv', index_col=0)
    if country_list == []:
        country_list = ['Canada']

    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                "headerFacet":{
                    "header": {"titleFontSize": 30, "FontSize": 30}
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'], empty='none')
    
    
    data_to_plot = compare_chart_df[compare_chart_df.countryname.isin(country_list)]
    
    line_chart = alt.Chart(data_to_plot).mark_line(clip=True).encode(
        alt.X('year:N', axis=alt.Axis(labelAngle=0), title="Generation"),
        alt.Y('EMI:Q', title="EMI", scale=alt.Scale(domain=(0,1))),
        alt.Color('countryname:N', title="")
    )
    
    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor

    selectors = alt.Chart(data_to_plot).mark_point().encode(
        x='year:N',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line_chart.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line_chart.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'EMI:Q', alt.value(' '))
    ).transform_calculate(label=f'format(datum.EMI,".3f")')
    
    rules = alt.Chart(data_to_plot).mark_rule(color='gray').encode(
        x='year:N',
    ).transform_filter(
        nearest
    )
    
    interactive_line_chart = alt.layer(
        line_chart, selectors, points, rules, text
    ).properties(
        width=275, height=250
    ).facet(
        column= alt.Column('child:N', title=None,
        header=alt.Header(labelFontSize=18))
    ).interactive().configure_legend(
        orient="right",
        labelFontSize=16)
    
    return interactive_line_chart

######### App layoput begins ################

app.layout = html.Div([

dbc.Container
    ([
        ####### Framework for upper half begins ###########

        dbc.Row([
                html.H1("Visualizing Global Education Opportunity", style = {"margin-left":"10px", "margin-top":"10px", 'text-align':'center'}, className="display-5"),
                html.P(
                    "In an ideal world, every child would have the opportunity to achieve success regardless of what social class they happened to be born into.  This visualization shows how education mobility (the potential for offspring to achieve an equal or higher education level than their parents) has changed globally over five generations using data from the World Bank (GDIM, 2018).  Use the map and bar chart to get a big-picture view for each generation then use the line plots below to explore comparisons of your choosing (Shift click either the bar chart or map to select multiple countries).  For example, see for yourself whether the US truly is 'the land of equal opportunity'!", 
                style = {"textAlign":"left", "margin-left":"10px", "margin-bottom":"30px"},
                className="lead"),
            ]),
            
    

        ######## Add Radio button as a Row ########
        dbc.Row([

            dbc.Col([
                    html.Div([
                        dcc.Markdown("**Select generation**\n(decade of birth)",style={"textAlign":"left",'font-size': '18px','margin-left':'25px'}),
                        dcc.RadioItems(
                            id='rb-chart-year',
                            options=[
                                        {'label': '1940', 'value': '1940'},
                                        {'label': '1950', 'value': '1950'},
                                        {'label': '1960', 'value': '1960'},
                                        {'label': '1970', 'value': '1970'},
                                        {'label': '1980', 'value': '1980'},
                                    ], value='1940',
                            labelStyle={'display': 'inline-block', 'font-size':'14px','width':'40%', 'margin-left':'25px'},
                            style={"display":"table-row"},
                            labelClassName="lead"
                                    )
                        ])
                        ]
                        ),


            ###### dbc.Col for World and Bar plot ###### 
                       
            dbc.Col([
                html.Iframe(
                sandbox='allow-scripts',
                id='plot_map',
                height='450',
                width='1200',
                style={'border-width': '0'},
                ####### The magic happens here ######### 
                srcDoc = make_map().to_html()
                ######### The magic happens here ######### 
                )]
            ),

                ]),


        ####### Framework for upper half ends ###########
        
        ####### Framework for bottom half begins ###########

        ######## Add header for lineplots ###########
        html.Div([
                html.H4('Region / Country / Economy Comparisons', style={"textAlign":"center", "margin-left":"0px"}),
            ]),

        ####### Add dropdown for line charts ########

        dbc.Col(
                html.Div([
                 html.Br(),
                 dcc.Markdown("Use the drop down below to select specific countries, continents, or economies to compare and see how education opportunity has changed overall, and whether it is different for boys (sons) and girls (daughters)",style={"textAlign":"left",'font-size': '18px'}),   
                 dcc.Dropdown(
                            id='dd-chart-area',
                            options=[
                                    {'label': 'Africa', 'value': 'Africa'},
                                    {'label': 'Asia', 'value': 'Asia'},
                                    {'label': 'Europe', 'value': 'Europe'},
                                    {'label': 'North America', 'value': 'North America'},
                                    {'label': 'Oceania', 'value': 'Oceania'},
                                    {'label': 'South America', 'value': 'South America'},
                                    {'label': 'Developing economies', 'value': 'Developing economies'},
                                    {'label': 'High-income economies', 'value': 'High-income economies'},
                                    {'label': 'Afghanistan', 'value': 'Afghanistan'},
                                    {'label': 'Albania', 'value': 'Albania'},
                                    {'label': 'Angola', 'value': 'Angola'},
                                    {'label': 'Argentina', 'value': 'Argentina'},
                                    {'label': 'Armenia', 'value': 'Armenia'},
                                    {'label': 'Australia', 'value': 'Australia'},
                                    {'label': 'Austria', 'value': 'Austria'},
                                    {'label': 'Azerbaijan', 'value': 'Azerbaijan'},
                                    {'label': 'Bangladesh', 'value': 'Bangladesh'},
                                    {'label': 'Belarus', 'value': 'Belarus'},
                                    {'label': 'Belgium', 'value': 'Belgium'},
                                    {'label': 'Benin', 'value': 'Benin'},
                                    {'label': 'Bhutan', 'value': 'Bhutan'},
                                    {'label': 'Bolivia', 'value': 'Bolivia'},
                                    {'label': 'Bosnia and Herzegovina', 'value': 'Bosnia and Herzegovina'},
                                    {'label': 'Botswana', 'value': 'Botswana'},
                                    {'label': 'Brazil', 'value': 'Brazil'},
                                    {'label': 'Bulgaria', 'value': 'Bulgaria'},
                                    {'label': 'Burkina Faso', 'value': 'Burkina Faso'},
                                    {'label': 'Cabo Verde', 'value': 'Cabo Verde'},
                                    {'label': 'Cambodia', 'value': 'Cambodia'},
                                    {'label': 'Cameroon', 'value': 'Cameroon'},
                                    {'label': 'Canada', 'value': 'Canada'},
                                    {'label': 'Central African Republic', 'value': 'Central African Republic'},
                                    {'label': 'Chad', 'value': 'Chad'},
                                    {'label': 'Chile', 'value': 'Chile'},
                                    {'label': 'China', 'value': 'China'},
                                    {'label': 'Colombia', 'value': 'Colombia'},
                                    {'label': 'Comoros', 'value': 'Comoros'},
                                    {'label': 'Congo, Dem. Rep.', 'value': 'Congo, Dem. Rep.'},
                                    {'label': 'Congo, Rep.', 'value': 'Congo, Rep.'},
                                    {'label': 'Costa Rica', 'value': 'Costa Rica'},
                                    {'label': "Cote d'Ivoire", 'value': "Cote d'Ivoire"},
                                    {'label': 'Croatia', 'value': 'Croatia'},
                                    {'label': 'Cyprus', 'value': 'Cyprus'},
                                    {'label': 'Czech Republic', 'value': 'Czech Republic'},
                                    {'label': 'Denmark', 'value': 'Denmark'},
                                    {'label': 'Djibouti', 'value': 'Djibouti'},
                                    {'label': 'Dominican Republic', 'value': 'Dominican Republic'},
                                    {'label': 'Ecuador', 'value': 'Ecuador'},
                                    {'label': 'Egypt, Arab Rep.', 'value': 'Egypt, Arab Rep.'},
                                    {'label': 'El Salvador', 'value': 'El Salvador'},
                                    {'label': 'Estonia', 'value': 'Estonia'},
                                    {'label': 'Ethiopia', 'value': 'Ethiopia'},
                                    {'label': 'Fiji', 'value': 'Fiji'},
                                    {'label': 'Finland', 'value': 'Finland'},
                                    {'label': 'France', 'value': 'France'},
                                    {'label': 'Gabon', 'value': 'Gabon'},
                                    {'label': 'Georgia', 'value': 'Georgia'},
                                    {'label': 'Germany', 'value': 'Germany'},
                                    {'label': 'Ghana', 'value': 'Ghana'},
                                    {'label': 'Greece', 'value': 'Greece'},
                                    {'label': 'Guatemala', 'value': 'Guatemala'},
                                    {'label': 'Guinea', 'value': 'Guinea'},
                                    {'label': 'Guinea-Bissau', 'value': 'Guinea-Bissau'},
                                    {'label': 'Honduras', 'value': 'Honduras'},
                                    {'label': 'Hungary', 'value': 'Hungary'},
                                    {'label': 'Iceland', 'value': 'Iceland'},
                                    {'label': 'India', 'value': 'India'},
                                    {'label': 'Indonesia', 'value': 'Indonesia'},
                                    {'label': 'Iran, Islamic Rep.', 'value': 'Iran, Islamic Rep.'},
                                    {'label': 'Iraq', 'value': 'Iraq'},
                                    {'label': 'Ireland', 'value': 'Ireland'},
                                    {'label': 'Israel', 'value': 'Israel'},
                                    {'label': 'Italy', 'value': 'Italy'},
                                    {'label': 'Japan', 'value': 'Japan'},
                                    {'label': 'Jordan', 'value': 'Jordan'},
                                    {'label': 'Kazakhstan', 'value': 'Kazakhstan'},
                                    {'label': 'Kenya', 'value': 'Kenya'},
                                    {'label': 'Kiribati', 'value': 'Kiribati'},
                                    {'label': 'Korea, Rep.', 'value': 'Korea, Rep.'},
                                    {'label': 'Kyrgyz Republic', 'value': 'Kyrgyz Republic'},
                                    {'label': 'Lao PDR', 'value': 'Lao PDR'},
                                    {'label': 'Latvia', 'value': 'Latvia'},
                                    {'label': 'Lebanon', 'value': 'Lebanon'},
                                    {'label': 'Lesotho', 'value': 'Lesotho'},
                                    {'label': 'Liberia', 'value': 'Liberia'},
                                    {'label': 'Lithuania', 'value': 'Lithuania'},
                                    {'label': 'Macedonia, FYR', 'value': 'Macedonia, FYR'},
                                    {'label': 'Madagascar', 'value': 'Madagascar'},
                                    {'label': 'Malawi', 'value': 'Malawi'},
                                    {'label': 'Malaysia', 'value': 'Malaysia'},
                                    {'label': 'Maldives', 'value': 'Maldives'},
                                    {'label': 'Mali', 'value': 'Mali'},
                                    {'label': 'Mauritania', 'value': 'Mauritania'},
                                    {'label': 'Mauritius', 'value': 'Mauritius'},
                                    {'label': 'Mexico', 'value': 'Mexico'},
                                    {'label': 'Moldova', 'value': 'Moldova'},
                                    {'label': 'Mongolia', 'value': 'Mongolia'},
                                    {'label': 'Montenegro', 'value': 'Montenegro'},
                                    {'label': 'Morocco', 'value': 'Morocco'},
                                    {'label': 'Mozambique', 'value': 'Mozambique'},
                                    {'label': 'Namibia', 'value': 'Namibia'},
                                    {'label': 'Nepal', 'value': 'Nepal'},
                                    {'label': 'Netherlands', 'value': 'Netherlands'},
                                    {'label': 'New Zealand', 'value': 'New Zealand'},
                                    {'label': 'Nicaragua', 'value': 'Nicaragua'},
                                    {'label': 'Niger', 'value': 'Niger'},
                                    {'label': 'Nigeria', 'value': 'Nigeria'},
                                    {'label': 'Norway', 'value': 'Norway'},
                                    {'label': 'Pakistan', 'value': 'Pakistan'},
                                    {'label': 'Panama', 'value': 'Panama'},
                                    {'label': 'Papua New Guinea', 'value': 'Papua New Guinea'},
                                    {'label': 'Paraguay', 'value': 'Paraguay'},
                                    {'label': 'Peru', 'value': 'Peru'},
                                    {'label': 'Philippines', 'value': 'Philippines'},
                                    {'label': 'Poland', 'value': 'Poland'},
                                    {'label': 'Portugal', 'value': 'Portugal'},
                                    {'label': 'Romania', 'value': 'Romania'},
                                    {'label': 'Russian Federation', 'value': 'Russian Federation'},
                                    {'label': 'Rwanda', 'value': 'Rwanda'},
                                    {'label': 'Sao Tome and Principe', 'value': 'Sao Tome and Principe'},
                                    {'label': 'Senegal', 'value': 'Senegal'},
                                    {'label': 'Serbia', 'value': 'Serbia'},
                                    {'label': 'Sierra Leone', 'value': 'Sierra Leone'},
                                    {'label': 'Slovak Republic', 'value': 'Slovak Republic'},
                                    {'label': 'Slovenia', 'value': 'Slovenia'},
                                    {'label': 'South Africa', 'value': 'South Africa'},
                                    {'label': 'South Sudan', 'value': 'South Sudan'},
                                    {'label': 'Spain', 'value': 'Spain'},
                                    {'label': 'Sri Lanka', 'value': 'Sri Lanka'},
                                    {'label': 'Sudan', 'value': 'Sudan'},
                                    {'label': 'Swaziland', 'value': 'Swaziland'},
                                    {'label': 'Sweden', 'value': 'Sweden'},
                                    {'label': 'Switzerland', 'value': 'Switzerland'},
                                    {'label': 'Taiwan, China', 'value': 'Taiwan, China'},
                                    {'label': 'Tajikistan', 'value': 'Tajikistan'},
                                    {'label': 'Tanzania', 'value': 'Tanzania'},
                                    {'label': 'Thailand', 'value': 'Thailand'},
                                    {'label': 'Timor-Leste', 'value': 'Timor-Leste'},
                                    {'label': 'Togo', 'value': 'Togo'},
                                    {'label': 'Tonga', 'value': 'Tonga'},
                                    {'label': 'Tunisia', 'value': 'Tunisia'},
                                    {'label': 'Turkey', 'value': 'Turkey'},
                                    {'label': 'Tuvalu', 'value': 'Tuvalu'},
                                    {'label': 'Uganda', 'value': 'Uganda'},
                                    {'label': 'Ukraine', 'value': 'Ukraine'},
                                    {'label': 'United Kingdom', 'value': 'United Kingdom'},
                                    {'label': 'United States', 'value': 'United States'},
                                    {'label': 'Uruguay', 'value': 'Uruguay'},
                                    {'label': 'Uzbekistan', 'value': 'Uzbekistan'},
                                    {'label': 'Vanuatu', 'value': 'Vanuatu'},
                                    {'label': 'Venezuela, RB', 'value': 'Venezuela, RB'},
                                    {'label': 'Vietnam', 'value': 'Vietnam'},
                                    {'label': 'West Bank and Gaza', 'value': 'West Bank and Gaza'},
                                    {'label': 'Yemen, Rep.', 'value': 'Yemen, Rep.'},
                                    {'label': 'Zambia', 'value': 'Zambia'},
                                ],
                            value = ['Africa', 'Canada', 'Developing economies'],
                            multi = True,
                            style = {"width":'60%', "margin-left":"0px"}
                            ),
                ], style={'font-size': '17px',"margin-top":"2px","margin-right":"0px",
                         "padding": "0px"})),
       

        ######## Add Line Plot(s) ############
        
        dbc.Row([

            ######## dbc.Col for line graphs ######
            dbc.Col([
                        html.Iframe(
                        sandbox='allow-scripts',
                        id='plot',
                        height='450',
                        width='1225',
                        style={'border-width': '0'},
                    ################ The magic happens here
                        srcDoc = make_line_chart().to_html()
                    ################ The magic happens here
                        ),
            ])
        ]),


        ######### Add footer ###########
        dbc.Row([
            dbc.Col([
                html.P('This Dash app was made collaboratively by the DSCI 532 L02 Group 212 from MDS 2019-20 batch'),
                html.P('Data Source: GDIM. 2018. Global Database on Intergenerational Mobility. Development Research Group, World Bank. Washington, D.C.: World Bank Group.')])
                ]),
    
    ], fluid = True,)
 
])

@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart-area', 'value')])
def update_plot(area):
    '''
    Takes in an area and calls make_line_chart to update our Altair figure
    '''
    updated_plot = make_line_chart(area).to_html()
    return updated_plot

@app.callback(
    dash.dependencies.Output('plot_map', 'srcDoc'),
    [dash.dependencies.Input('rb-chart-year', 'value')])

def update_plot_map(year):
    '''
    Takes in an area and calls make_map to update our Altair figure
    '''
    updated_plot_map = make_map(year).to_html()
    return updated_plot_map

if __name__ == '__main__':
    app.run_server(debug=True)
