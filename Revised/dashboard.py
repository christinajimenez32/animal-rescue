
# Setup Dash
from dash import Dash, callback_context

# Configure the necessary Python module imports 
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64

# Configure OS module
import os

# Configure the plotting and data manipulation modules
import numpy as np
import pandas as pd

# Import CRUD module
from Shelter import AnimalShelter

###########################
# Data Manipulation / Model
###########################

# Local MongoDB Cconfiguration
USER = ""           
PASS = ""           
HOST = "localhost"  # Local MongoDB
PORT = 27017        # MongoDB port
DB = "AAC"
COL = "animals"

# Connect to database via CRUD Module
db = AnimalShelter(USER, PASS, HOST, PORT, DB, COL)

# Read all documents from database
df = pd.DataFrame.from_records(db.read({}))

# Remove MongoDB '_id' 
if '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)

print(f"Loaded {len(df)} animals from database")

# Get values for dropdown filters 
animal_types = sorted(df['animal_type'].unique().tolist()) if 'animal_type' in df.columns else []
genders = sorted(df['sex_upon_outcome'].unique().tolist()) if 'sex_upon_outcome' in df.columns else []

#########################
# Dashboard Layout / View
#########################
app = Dash(__name__)

# Load Grazioso Salvare logo
try:
    image_filename = "Logo.png"
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    logo_exists = True
except:
    logo_exists = False
    print("Logo.png not found")

# Dashboard Layout
app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    
    # Header
    html.Div(style={
        'backgroundColor': "#81B0DE",
        'color': 'white',
        'padding': '20px',
        'textAlign': 'center',
        'marginBottom': '20px'
    }, children=[
        html.H1('Grazioso Salvare Animal Rescue Dashboard', 
                style={'margin': '0'}),
        html.P('Manage and Explore Rescued Animal Data',
                style={'margin': '0', 'fontSize': '18px'})
               
    ]),
    
    # Logo section
    html.Div(style={'textAlign': 'center', 'marginBottom': '20px'}, children=[
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                style={'height': '150px', 'margin': '10px'}) if logo_exists else html.Div(),
    ]),
    
    html.Hr(),
    
    # Filter section
    html.Div(style={
        'backgroundColor': "#CCE5EB",
        'padding': '20px',
        'borderRadius': '5px',
        'marginBottom': '20px'
    }, children=[
        html.H3('Search & Filter Options', style={'color': '#2C3E50', 'marginBottom': '20px'}),
        
        # Rescue type filter
        html.Div(style={'marginBottom': '15px'}, children=[
            html.Label('Quick Rescue Filter:', style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='rescue-filter',
                options=[
                    {'label': 'No Rescue Filter', 'value': 'None'},
                    {'label': 'Water Rescue', 'value': 'Water'},
                    {'label': 'Mountain/Wilderness Rescue', 'value': 'Mountain'},
                    {'label': 'Disaster/Tracking', 'value': 'Disaster'}
                ],
                value='None',
                clearable=False,
                style={'width': '100%'}
            )
        ]),
        
        # Animal type and gender
        html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '15px'}, children=[
            html.Div(style={'flex': '1'}, children=[
                html.Label('Animal Type:', style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='animal-type-filter',
                    options=[{'label': 'All Animals', 'value': 'All'}] + 
                            [{'label': atype, 'value': atype} for atype in animal_types],
                    value='All',
                    clearable=False,
                    style={'width': '100%'}
                )
            ]),
            html.Div(style={'flex': '1'}, children=[
                html.Label('Gender:', style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='gender-filter',
                    options=[{'label': 'All Genders', 'value': 'All'}] + 
                            [{'label': gender, 'value': gender} for gender in genders],
                    value='All',
                    clearable=False,
                    style={'width': '100%'}
                )
            ])
        ]),
        
        # Age range
        html.Div(style={'marginBottom': '15px'}, children=[
            html.Label('Age Range (in weeks):', style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
            html.Div(style={'display': 'flex', 'gap': '10px', 'alignItems': 'center'}, children=[
                dcc.Input(
                    id='age-min-filter',
                    type='number',
                    placeholder='Min age',
                    style={'flex': '1', 'padding': '8px', 'borderRadius': '3px', 'border': '1px solid #BDC3C7'}
                ),
                html.Span('to', style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='age-max-filter',
                    type='number',
                    placeholder='Max age',
                    style={'flex': '1', 'padding': '8px', 'borderRadius': '3px', 'border': '1px solid #BDC3C7'}
                )
            ])
        ]),
        
        # Buttons
        html.Div(style={'textAlign': 'center', 'marginTop': '20px'}, children=[
            html.Button(
                'Apply Filters',
                id='apply-filters-btn',
                n_clicks=0,
                style={
                    'backgroundColor': '#3498DB',
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 30px',
                    'borderRadius': '5px',
                    'fontSize': '16px',
                    'cursor': 'pointer',
                    'marginRight': '10px'
                }
            ),
            html.Button(
                'Reset All Filters',
                id='reset-filters-btn',
                n_clicks=0,
                style={
                    'backgroundColor': '#95A5A6',
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 30px',
                    'borderRadius': '5px',
                    'fontSize': '16px',
                    'cursor': 'pointer'
                }
            )
        ])
    ]),
    
    html.Hr(),
    
    # Results count
    html.Div(
        id='results-count',
        style={
            'textAlign': 'center',
            'fontSize': '18px',
            'fontWeight': 'bold',
            'color': '#2C3E50',
            'marginBottom': '15px'
        }
    ),
    
    # Data table
    dash_table.DataTable(
        id='datatable-id',
        columns=[{
            "name": i.replace('_', ' ').title(),
            "id": i,
            "deletable": False,
            "selectable": True
        } for i in df.columns],
        data=df.to_dict('records'),
        row_selectable='single',
        selected_rows=[0],
        page_size=15,
        page_action='native',
        sort_action='native',
        sort_mode='multi',
        filter_action='native',
        style_table={
            'overflowX': 'auto',
            'maxHeight': '500px',
            'overflowY': 'auto'
        },
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'fontFamily': 'Arial'
        },
        style_header={
            'backgroundColor': "#5A98D6",
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#F8F9F9'
            },
            {
                'if': {'state': 'selected'},
                'backgroundColor': '#3498DB',
                'color': 'white'
            }
        ]
    ),
    
    html.Br(),
    html.Hr(),
    
    # Visualizations side by side
    html.Div(className='row', style={'display': 'flex', 'gap': '20px'}, children=[
        html.Div(id='graph-id', style={'flex': '1', 'minWidth': '400px'}),
        html.Div(id='map-id', style={'flex': '1', 'minWidth': '400px'})
    ])
])

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback(
    [Output('datatable-id', 'data'),
     Output('results-count', 'children'),
     Output('rescue-filter', 'value'),
     Output('animal-type-filter', 'value'),
     Output('gender-filter', 'value'),
     Output('age-min-filter', 'value'),
     Output('age-max-filter', 'value')],
    [Input('apply-filters-btn', 'n_clicks'),
     Input('reset-filters-btn', 'n_clicks'),
     Input('rescue-filter', 'value')],
    [State('animal-type-filter', 'value'),
     State('gender-filter', 'value'),
     State('age-min-filter', 'value'),
     State('age-max-filter', 'value')]
)
def update_dashboard(apply_clicks, reset_clicks, rescue_type, animal_type, gender, age_min, age_max):
    """Update data table based on all selected filters"""
    
    # Determine which input triggered the callback
    ctx = callback_context
    if not ctx.triggered:
        trigger_id = 'rescue-filter'
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # If reset button clicked reset everything
    if trigger_id == 'reset-filters-btn':
        filtered_data = db.read({})
        df_filtered = pd.DataFrame.from_records(filtered_data)
        if '_id' in df_filtered.columns:
            df_filtered.drop(columns=['_id'], inplace=True)
        
        count = len(df_filtered)
        results_message = f"Showing {count} animal(s) - All filters reset"
        
        # Reset all filter values
        return df_filtered.to_dict('records'), results_message, 'None', 'All', 'All', None, None
    
    query = {}
    
    # Build query with all filters
    
    #  Rescue type filter
    if rescue_type and rescue_type != 'None':
        if rescue_type == 'Water':
            query = {
                "animal_type": "Dog",
                "breed": {
                    "$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]
                },
                "sex_upon_outcome": "Intact Female",
                "age_upon_outcome_in_weeks": {
                    "$gte": 26,
                    "$lte": 156
                }
            }
        elif rescue_type == 'Mountain':
            query = {
                "animal_type": "Dog",
                "breed": {
                    "$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", 
                           "Siberian Husky", "Rottweiler"]
                },
                "sex_upon_outcome": "Intact Male",
                "age_upon_outcome_in_weeks": {
                    "$gte": 26,
                    "$lte": 156
                }
            }
        elif rescue_type == 'Disaster':
            query = {
                "animal_type": "Dog",
                "breed": {
                    "$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", 
                           "Bloodhound", "Rottweiler"]
                },
                "sex_upon_outcome": "Intact Male",
                "age_upon_outcome_in_weeks": {
                    "$gte": 20,
                    "$lte": 300
                }
            }
    
    # Animal Filter
    # If both rescue filter and animal selected then animals type takes precedence
    if animal_type and animal_type != 'All':
        if rescue_type and rescue_type != 'None':
            # Add animal type to existing query 
            query['animal_type'] = animal_type
        else:
            # animal type
            query['animal_type'] = animal_type
    
    # Gender filter
    if gender and gender != 'All':
        query['sex_upon_outcome'] = gender
    
    # Age filter
    if age_min is not None or age_max is not None:
        age_query = {}
        if age_min is not None:
            age_query['$gte'] = age_min
        if age_max is not None:
            age_query['$lte'] = age_max
        if age_query:
            # If there is already an age filter from rescue type it will be overwritten 
            if 'age_upon_outcome_in_weeks' in query:
                # Combine constraints
                existing_age = query['age_upon_outcome_in_weeks']
                if '$gte' in age_query and '$gte' in existing_age:
                    age_query['$gte'] = max(age_query['$gte'], existing_age['$gte'])
                elif '$gte' in existing_age:
                    age_query['$gte'] = existing_age['$gte']
                    
                if '$lte' in age_query and '$lte' in existing_age:
                    age_query['$lte'] = min(age_query['$lte'], existing_age['$lte'])
                elif '$lte' in existing_age:
                    age_query['$lte'] = existing_age['$lte']
            
            query['age_upon_outcome_in_weeks'] = age_query
    
    # Fetch filtered data from database
    print(f"Query being executed: {query}")  # Debug
    filtered_data = db.read(query)
    df_filtered = pd.DataFrame.from_records(filtered_data)
    
    # Remove '_id' column if present
    if '_id' in df_filtered.columns:
        df_filtered.drop(columns=['_id'], inplace=True)
    
    # Count results
    count = len(df_filtered)
    
    if count == 0:
        results_message = "No results matched"
    else:
        results_message = f"Showing {count} animal(s) matching your criteria"
    
    # Return current filter values 
    return df_filtered.to_dict('records'), results_message, rescue_type, animal_type, gender, age_min, age_max


@app.callback(
    Output('graph-id', 'children'),
    [Input('datatable-id', 'derived_virtual_data')]
)
def update_graphs(viewData):
    """Rescue Animals Breed Distribution Pie Chart"""
    
    if viewData is None or len(viewData) == 0:
        return [html.Div(style={
            'textAlign': 'center',
            'padding': '40px',
            'backgroundColor': '#F8F9F9',
            'borderRadius': '5px',
            'border': '2px dashed #BDC3C7'
        }, children=[
            html.H4('No Data to Display', style={'color': '#7F8C8D'}),
            html.P('Try adjusting your filters', style={'color': '#95A5A6'})
        ])]
    
    df_graph = pd.DataFrame(viewData)
    
    # Count breeds
    if 'breed' not in df_graph.columns:
        return [html.P('No breed data available')]
    
    # Get top 10 breeds
    breed_counts = df_graph['breed'].value_counts().head(10)
    
    # Create DataFrame for plotly
    chart_df = pd.DataFrame({
        'Breed': breed_counts.index,
        'Count': breed_counts.values
    })
    
    # Create pie chart 
    figure = px.pie(
        chart_df,
        values='Count',  
        names='Breed',   
        title='Top 10 Breeds of Rescued Animals',
        hole=0.3
    )
    
    figure.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )
    
    figure.update_layout(
        showlegend=True,
        legend=dict(
            title="Breeds",
            orientation="v",
            x=1.05,
            y=1
        ),
        height=500
    )
    
    return [dcc.Graph(figure=figure)]


@app.callback(
    Output('map-id', 'children'),
    [Input('datatable-id', 'derived_virtual_data'),
     Input('datatable-id', 'derived_virtual_selected_rows')]
)
def update_map(viewData, index):
    """Update map based on selected animal"""
    
    if viewData is None or not viewData:
        return [html.Div(style={
            'textAlign': 'center',
            'padding': '40px',
            'backgroundColor': '#F8F9F9',
            'borderRadius': '5px',
            'border': '2px dashed #BDC3C7'
        }, children=[
            html.H4('No Data to Display', style={'color': '#7F8C8D'}),
            html.P('Select an animal from the table above', style={'color': '#95A5A6'})
        ])]
    
    if index is None or not index:
        return [html.Div(style={
            'textAlign': 'center',
            'padding': '40px',
            'backgroundColor': '#F8F9F9',
            'borderRadius': '5px',
            'border': '2px dashed #BDC3C7'
        }, children=[
            html.H4('Select an Animal', style={'color': '#7F8C8D'}),
            html.P('Click on a row in the table to view its location', style={'color': '#95A5A6'})
        ])]
    
    dff = pd.DataFrame.from_dict(viewData)
    
    # Get selected row
    row = index[0] if index else 0
    
    # Safety check
    if row >= len(dff):
        row = 0
    
    # Get location data
    try:
        lat = float(dff.iloc[row]['location_lat']) if 'location_lat' in dff.columns else 30.75
        lon = float(dff.iloc[row]['location_long']) if 'location_long' in dff.columns else -97.48
        breed = str(dff.iloc[row]['breed']) if 'breed' in dff.columns else 'Unknown'
        name = str(dff.iloc[row]['name']) if 'name' in dff.columns else 'Unknown'
        animal_type = str(dff.iloc[row]['animal_type']) if 'animal_type' in dff.columns else 'Unknown'
        age = str(dff.iloc[row]['age_upon_outcome_in_weeks']) if 'age_upon_outcome_in_weeks' in dff.columns else 'Unknown'
    except Exception as e:
        print(f"Error getting location data: {e}")
        lat, lon = 30.75, -97.48
        breed, name, animal_type, age = 'Unknown', 'Unknown', 'Unknown', 'Unknown'
    
    # Create map with zoom to exact location
    return [
        dl.Map(
            style={'width': '100%', 'height': '500px'},
            center=[lat, lon],  # Center on animal location
            zoom=15,  # Zoom closer 
            children=[
                dl.TileLayer(id="base-layer-id"),
                dl.Marker(
                    position=[lat, lon],
                    children=[
                        dl.Tooltip(f"{name} - {breed}"),
                        dl.Popup([
                            html.H4(f"{name}", style={'margin': '0 0 10px 0'}),
                            html.P(f"Type: {animal_type}", style={'margin': '5px 0'}),
                            html.P(f"Breed: {breed}", style={'margin': '5px 0'}),
                            html.P(f"Age: {age} weeks", style={'margin': '5px 0'}),
                            html.P(f"Location: ({lat}, {lon})", style={'margin': '5px 0', 'fontSize': '12px', 'color': '#7F8C8D'})
                        ])
                    ]
                )
            ]
        )
    ]


# Run the app
if __name__ == '__main__':
    print("\nStarting Grazioso Salvare Dashboard...")
    print("Access at: http://localhost:8050")
    print("Press CTRL+C to stop\n")
    app.run(debug=True, port=8050)