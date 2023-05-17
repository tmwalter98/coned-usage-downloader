from datetime import datetime
from datetime import timedelta
from datetime import timezone
import dash
from dash import html, dcc
import pandas as pd
import pandas as pd
import plotly.graph_objects as go


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import OpowerReadings, Base

from dotenv import dotenv_values

config = dotenv_values(".env")

# Database connection configuration
engine = create_engine(config["PGSQL_CONNECTION_STRING"])
Session = sessionmaker(bind=engine)
session = Session()

# Dash app setup
app = dash.Dash(__name__)
t1 = datetime.now(timezone.utc) + timedelta(hours=-24)
t0 = t1 + timedelta(hours=-12) + timedelta(hours=-24)
# Function to fetch data from the database


def fetch_data_t(t0, t1):
    Base.metadata.create_all(engine)

    df = pd.read_sql_query(
        sql=select(OpowerReadings).filter(OpowerReadings.end_time.between(t0, t1)),
        con=engine,
    )
    rates = {
        "summer": {"peak": 25.50, "other": 1.80},
        "winter": {"peak": 9.44, "other": 1.80},
    }

    def calculate_cost(row):
        month = row["start_time"].month
        hour = row["start_time"].hour
        if month >= 6 and month <= 9:
            rate = rates["summer"]["other"] if hour < 8 else rates["summer"]["peak"]
        else:
            rate = rates["winter"]["other"] if hour < 8 else rates["winter"]["peak"]
        return ((row["duration"].total_seconds() / 3600) * rate) * row[
            "consumption_value"
        ]

    df["duration"] = df["end_time"] - df["start_time"]
    df["cost"] = df.apply(calculate_cost, axis=1)
    return df


# Define app layout
app.layout = html.Div(
    children=[
        html.H1("Data from PostgreSQL"),
        dcc.DatePickerRange(
            id="date-range",
            display_format="YYYY-MM-DD",
            start_date=t0,
            end_date=t1,
            clearable=True,
        ),
        dcc.Graph(id="line-chart"),
    ]
)

# Callback function to update the line chart


@app.callback(
    dash.dependencies.Output("line-chart", "figure"),
    [
        dash.dependencies.Input("date-range", "start_date"),
        dash.dependencies.Input("date-range", "end_date"),
    ],
)
def update_line_chart(start_date, end_date):
    df = fetch_data_t(start_date, end_date)
    start_date, end_date = min(start_date, end_date), max(start_date, end_date)
    filtered_df = df[(df["end_time"] >= start_date) & (df["end_time"] <= end_date)]

    if filtered_df.empty:
        return {}

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered_df["start_time"],
            y=filtered_df["consumption_value"],
            name="Consumption Value",
        )
    )
    fig.add_trace(
        go.Scatter(x=filtered_df["start_time"], y=filtered_df["cost"], name="Cost")
    )

    fig.update_layout(
        title="Consumption Value and Cost over Time",
        xaxis_title="Start Time",
        yaxis_title="Value",
        xaxis=dict(rangebreaks=[dict(bounds=["00:00", "08:00"], pattern="hour")]),
    )
    midnight_rows = df[df["start_time"].dt.time == pd.Timestamp("00:00:00").time()]
    midnight_tuples = []
    for __, row in midnight_rows.iterrows():
        val = row["start_time"]
        midnight_tuples.append(
            (val + pd.Timedelta(hours=8), val + pd.Timedelta(hours=24))
        )

    for row1, row2 in midnight_tuples:
        fig.add_vrect(
            x0=row1,
            x1=row2,
            annotation_text="Peak Hours",
            annotation_position="top left",
            fillcolor="red",
            opacity=0.25,
            line_width=0,
        )
    return fig


if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(debug=False)
