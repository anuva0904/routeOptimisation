import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

from preprocessing.data_preprocessing import preprocess_data
from graph.graph_builder import build_graph
from optimization.route_optimizer import optimize_route


# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="AI Bus Route Optimization",
    layout="wide"
)

st.title("🚌 AI Bus Route Optimization System")


# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
df = pd.read_csv("data/final_merged_with_stops.csv")

df, edges_df = preprocess_data(df)

G = build_graph(df, edges_df)


# ------------------------------------------------
# SIDEBAR ROUTE SELECTION
# ------------------------------------------------
st.sidebar.header("Route Selection")

stops = df["stop_id"].unique()

start = st.sidebar.selectbox("Start Stop", stops)
end = st.sidebar.selectbox("Destination Stop", stops)

find = st.sidebar.button("Find Optimal Route")


# ------------------------------------------------
# ROUTE CALCULATION
# ------------------------------------------------
if find:

    route, total_time = optimize_route(G, start, end)

    if len(route) == 0:

        st.error("No route found")

    else:

        route_df = df[df["stop_id"].isin(route)].drop_duplicates("stop_id")

        route_df = route_df.set_index("stop_id").loc[route].reset_index()


        # ------------------------------------------------
        # MAP DATA
        # ------------------------------------------------
        map_df = pd.DataFrame({
            "lat": route_df["stop_lat"],
            "lon": route_df["stop_lon"],
            "name": route_df["stop_name"]
        })


        # ------------------------------------------------
        # ROUTE LINE
        # ------------------------------------------------
        route_layer = pdk.Layer(
            "PathLayer",
            data=[{
                "path": map_df[["lon","lat"]].values.tolist()
            }],
            get_path="path",
            get_color=[255,0,0],
            width_scale=20,
            width_min_pixels=3
        )


        # ------------------------------------------------
        # BUS STOPS
        # ------------------------------------------------
        stop_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position="[lon, lat]",
            get_radius=80,
            get_color=[0,200,255],
            pickable=True
        )


        # ------------------------------------------------
        # MAP VIEW
        # ------------------------------------------------
        view_state = pdk.ViewState(
            latitude=map_df["lat"].mean(),
            longitude=map_df["lon"].mean(),
            zoom=12,
            pitch=0
        )


        deck = pdk.Deck(
            map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
            initial_view_state=view_state,
            layers=[route_layer, stop_layer],
            tooltip={"text": "{name}"}
        )


        # ------------------------------------------------
        # LAYOUT
        # ------------------------------------------------
        col1, col2 = st.columns([3,1])


        with col1:

            st.subheader("Route Map")

            st.pydeck_chart(deck)


        with col2:

            st.subheader("Route Summary")

            st.metric("Total Stops", len(route))
            st.metric("Estimated Time", f"{round(total_time,2)} min")
            st.metric("Route Length", f"{len(route)-1} segments")

            st.write("Stops:")

            for r in route:
                st.write("➡", df[df["stop_id"]==r]["stop_name"].iloc[0])


        # ------------------------------------------------
        # TRAVEL TIME CHART
        # ------------------------------------------------
        st.subheader("Travel Time Analysis")

        times = []

        for i in range(len(route)-1):

            t = G[route[i]][route[i+1]]["weight"]

            times.append(t)

        chart_df = pd.DataFrame({
            "Segment": list(range(len(times))),
            "Travel Time": times
        })


        fig = px.line(
            chart_df,
            x="Segment",
            y="Travel Time",
            markers=True,
            title="Segment Travel Time"
        )

        st.plotly_chart(fig, use_container_width=True)