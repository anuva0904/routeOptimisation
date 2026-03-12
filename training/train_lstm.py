import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import torch
import pandas as pd
import numpy as np

from models.lstm_model import LSTMModel


DATA_PATH = "data/final_merged_with_stops.csv"


def prepare_data():

    df = pd.read_csv(DATA_PATH)

    df['arrival_time'] = pd.to_datetime(df['arrival_time'])
    df['departure_time'] = pd.to_datetime(df['departure_time'])

    df = df.sort_values(['trip_id','arrival_time'])

    travel_times = []

    for trip, group in df.groupby("trip_id"):

        group = group.sort_values("arrival_time")

        for i in range(len(group)-1):

            t = (
                pd.to_datetime(group.iloc[i+1]['arrival_time']) -
                pd.to_datetime(group.iloc[i]['departure_time'])
            ).total_seconds()

            travel_times.append(max(t,1))

    travel_times = np.array(travel_times)

    X = travel_times[:-1]
    y = travel_times[1:]

    X = torch.tensor(X).float().view(-1,1,1)
    y = torch.tensor(y).float().view(-1,1)

    return X,y


def train():

    X,y = prepare_data()

    model = LSTMModel()

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    loss_fn = torch.nn.MSELoss()

    epochs = 50

    for epoch in range(epochs):

        pred = model(X)

        loss = loss_fn(pred,y)

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        print("Epoch",epoch,"Loss",loss.item())

    torch.save(model.state_dict(),"models/lstm_travel_time.pth")

    print("Model saved")


if __name__ == "__main__":

    train()