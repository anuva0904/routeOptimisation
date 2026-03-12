import pandas as pd


def preprocess_data(df):

    df['arrival_time'] = pd.to_datetime(df['arrival_time'])
    df['departure_time'] = pd.to_datetime(df['departure_time'])

    df = df.sort_values(['trip_id','arrival_time'])

    edges = []

    for trip, group in df.groupby("trip_id"):

        group = group.sort_values("arrival_time")

        for i in range(len(group)-1):

            current = group.iloc[i]
            next_stop = group.iloc[i+1]

            travel_time = (
                next_stop['arrival_time'] - current['departure_time']
            ).total_seconds()

            edges.append({
                "from_stop": current["stop_id"],
                "to_stop": next_stop["stop_id"],
                "travel_time": max(travel_time,1)
            })

    edges_df = pd.DataFrame(edges)

    return df, edges_df
