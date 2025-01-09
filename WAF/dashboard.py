import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
from request import DBController

# Initialize the app
app = dash.Dash(__name__)
app.title = "AI-Driven Firewall Dashboard"

# CSS for styling
app.css.config.serve_locally = True
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Database controller
db = DBController()

# Layout of the dashboard
app.layout = html.Div([
    # Header with current date and time
    html.Div([
        html.H1("AI-Driven Firewall Dashboard", style={"text-align": "center", "margin-bottom": "10px"}),
        html.H3(id="current-datetime", style={"text-align": "center", "margin-bottom": "30px"}),
    ], style={"padding": "10px", "background-color": "#f7f7f7"}),

    # Tabs for navigation
    dcc.Tabs(id="tabs", value="overview", children=[
        dcc.Tab(label="Overview", value="overview", style={"padding": "10px"}),
        dcc.Tab(label="Detailed Analysis", value="analysis", style={"padding": "10px"}),
        dcc.Tab(label="Logs", value="logs", style={"padding": "10px"})
    ], style={"font-size": "18px"}),

    # Tab content
    html.Div(id="tab-content", style={"padding": "20px"})
])

# Callback to update current date and time
@app.callback(Output("current-datetime", "children"), Input("tabs", "value"))
def update_datetime(_):
    return f"Current Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# Callback to update tab content
@app.callback(Output("tab-content", "children"), [Input("tabs", "value")])
def update_tab(tab_name):
    if tab_name == "overview":
        return html.Div([
            html.H2("Threat Overview", style={"text-align": "center"}),
            dcc.Graph(
                id="threat-distribution-pie",
                figure={
                    "data": [
                        go.Pie(
                            labels=["SQL Injection", "XSS", "Path Traversal", "Command Injection"],
                            values=[10, 15, 7, 4],  # Replace with actual database data
                            hole=0.4,
                            textinfo="label+percent",
                            hoverinfo="label+value"
                        )
                    ],
                    "layout": {
                        "title": "Distribution of Threat Types",
                        "legend": {"orientation": "h", "x": 0.5, "y": -0.1, "xanchor": "center"}
                    }
                }
            ),
            dcc.Graph(
                id="threat-frequency-bar",
                figure={
                    "data": [
                        go.Bar(
                            x=["2025-01-01", "2025-01-02", "2025-01-03"],
                            y=[5, 3, 8],  # Replace with actual database data
                            name="SQL Injection",
                            marker={"color": "indianred"}
                        ),
                        go.Bar(
                            x=["2025-01-01", "2025-01-02", "2025-01-03"],
                            y=[3, 4, 5],  # Replace with actual database data
                            name="XSS",
                            marker={"color": "lightblue"}
                        )
                    ],
                    "layout": {
                        "title": "Threat Frequency Over Time",
                        "barmode": "stack",
                        "legend": {"orientation": "h", "x": 0.5, "y": -0.2, "xanchor": "center"}
                    }
                }
            ),
            html.H3("Threat Summary Report", style={"text-align": "center", "margin-top": "20px"}),
            html.Table([
                html.Tr([html.Th("Threat Type"), html.Th("Count")], style={"background-color": "#f2f2f2"}),
                html.Tr([html.Td("SQL Injection"), html.Td("10")]),
                html.Tr([html.Td("XSS"), html.Td("15")]),
                html.Tr([html.Td("Path Traversal"), html.Td("7")]),
                html.Tr([html.Td("Command Injection"), html.Td("4")])
            ], style={"width": "50%", "margin": "0 auto", "border": "1px solid black"})
        ])
    
    elif tab_name == "analysis":
        try:
            data = db.read_all()
            return html.Div([
                html.H2("Detailed Attack Analysis", style={"text-align": "center"}),
                dcc.Graph(
                    id="detailed-analysis-graph",
                    figure={
                        "data": [
                            go.Bar(
                                x=data["timestamp"],
                                y=data["threat_type"],
                                name="Threats by Timestamp",
                                marker={"color": "orange"}
                            )
                        ],
                        "layout": {
                            "title": "Threats Over Time",
                            "xaxis": {"title": "Timestamp"},
                            "yaxis": {"title": "Threat Count"}
                        }
                    }
                ),
                html.H3("Log Details", style={"text-align": "center", "margin-top": "20px"}),
                html.Table(
                    [html.Tr([html.Th(col) for col in ["Timestamp", "Origin", "Host", "Method", "Threat Type"]], style={"background-color": "#f2f2f2"})] +
                    [html.Tr([html.Td(row[col]) for col in ["timestamp", "origin", "host", "method", "threat_type"]]) for _, row in data.iterrows()],
                    style={"width": "100%", "margin-top": "20px", "border": "1px solid black"}
                )
            ])
        except Exception as e:
            return html.Div([html.H2("Error loading data"), html.P(str(e))])

    elif tab_name == "logs":
        try:
            data = db.read_all()
            return html.Div([
                html.H2("Log Entries", style={"text-align": "center"}),
                html.Table(
                    [html.Tr([html.Th(col) for col in ["Timestamp", "Origin", "Host", "Method", "Threat Type"]], style={"background-color": "#f2f2f2"})] +
                    [html.Tr([html.Td(row[col]) for col in ["timestamp", "origin", "host", "method", "threat_type"]]) for _, row in data.iterrows()],
                    style={"width": "100%", "margin-top": "20px", "border": "1px solid black"}
                )
            ])
        except Exception as e:
            return html.Div([html.H2("Error loading logs"), html.P(str(e))])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
