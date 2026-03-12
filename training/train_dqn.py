import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import torch
import random
import numpy as np

from models.dqn_model import DQN


state_size = 10
action_size = 5


def train():

    model = DQN(state_size,action_size)

    optimizer = torch.optim.Adam(model.parameters(),lr=0.001)

    loss_fn = torch.nn.MSELoss()

    episodes = 500

    for ep in range(episodes):

        state = torch.randn(state_size)

        target = torch.randn(action_size)

        pred = model(state)

        loss = loss_fn(pred,target)

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        if ep % 50 == 0:

            print("Episode",ep,"Loss",loss.item())

    torch.save(model.state_dict(),"models/dqn_route_model.pth")

    print("DQN training finished")


if __name__ == "__main__":

    train()
