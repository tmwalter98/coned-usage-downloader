from typing import Tuple
import streamlit as st
import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import datetime
from datetime import timedelta
from datetime import timezone
from models import OpowerReadings, Base
from plotly.tools import FigureFactory as ff

st.set_page_config(page_title='ConEd Usage Data',layout="wide")
st.title('ConEd Usage Data')

PGSQL_CONNECTION_STRING = 'postgresql://postgres:ByK64.{Chrbh&hMjuAV7PLv>c-?D@shopping-services.cigwtl4yjm4i.us-east-1.rds.amazonaws.com/postgres'
DATE_COLUMN = 'date/time'

plotly.io.json.config.default_engine = 'orjson'


engine = create_engine(PGSQL_CONNECTION_STRING)
Session = sessionmaker(bind=engine)
session = Session()

def get_time_range():
    time_range = None
    with Session() as sess:
        select(OpowerReadings)
        oldest_record: OpowerReadings = session.query(OpowerReadings).order_by(OpowerReadings.end_time.asc()).first()
        newest_record: OpowerReadings = session.query(OpowerReadings).order_by(OpowerReadings.end_time.desc()).first()
        time_range = (oldest_record.end_time, newest_record.end_time)
        print(time_range)
        return time_range

@st.cache_data
def load_data(t0, t1) -> pd.DataFrame:
    engine = create_engine(PGSQL_CONNECTION_STRING)
    Base.metadata.create_all(engine)

    df = pd.read_sql_query(
        sql=select(OpowerReadings).filter(
            OpowerReadings.end_time.between(t0, t1)),
        con=engine
    )
    rates = {
    'summer': {'peak': 25.50, 'other': 1.80},
    'winter': {'peak': 9.44, 'other': 1.80}
    }

    def calculate_cost(row):
        month = row['start_time'].month    
        hour = row['start_time'].hour
        if month >= 6 and month <= 9:
            rate = rates['summer']['other'] if hour > 8 else rates['summer']['peak']
        else:
            rate = rates['winter']['other'] if hour > 8 else rates['winter']['peak']
        return ((row['duration'].total_seconds() / 3600) * rate)*row['consumption_value']

    df['duration'] = df['end_time'] - df['start_time']
    df['cost'] = df.apply(calculate_cost, axis=1)
    return df


t0, t1 = get_time_range()
data_load_state = st.text('Loading data...')
#data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

time_range = (t1 + timedelta(hours=-48), t1)
d: Tuple[datetime.date, datetime.date] = st.date_input("date range without default", value=time_range, min_value=t0, max_value=t1)
#st.write(load_data(d[0], d[1]))
fig = ff.create_line_chart(df, x='start_time', y=['consumption_value', 'cost'], title='Consumption and Cost Over Time')

# Update x-axis and y-axis labels
fig.update_xaxes(title='Start Time')
fig.update_yaxes(title='Consumption Value')

st.plotly_chart(fig, use_container_width=True)
