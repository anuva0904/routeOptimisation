import pandas as pd


def load_data(path):

    df = pd.read_csv(path)

    return df


def compute_travel_times(df):

    df['arrival_time'] = pd.to_datetime(df['arrival_time'])
    df['departure_time'] = pd.to_datetime(df['departure_time'])

    df = df.sort_values(['trip_id', 'arrival_time'])

    edges = []

    for trip, group in df.groupby("trip_id"):

        group = group.sort_values("arrival_time")

        for i in range(len(group)-1):

            current = group.iloc[i]
            nxt = group.iloc[i+1]

            travel_time = (
                nxt['arrival_time'] - current['departure_time']
            ).total_seconds()

            travel_time = max(travel_time, 1)

            # forward edge
            edges.append({
                "from_stop": current["stop_id"],
                "to_stop": nxt["stop_id"],
                "travel_time": travel_time
            })

            # reverse edge
            edges.append({
                "from_stop": nxt["stop_id"],
                "to_stop": current["stop_id"],
                "travel_time": travel_time
            })

    edges_df = pd.DataFrame(edges)

    # average travel time across trips
    edges_df = edges_df.groupby(
        ["from_stop", "to_stop"]
    )["travel_time"].mean().reset_index()

    return edges_df
