# AI Bus Route Optimization System

This project is an AI-powered system that optimizes bus routes. It utilizes machine learning models (LSTM) to predict sequence-based travel times between bus stops and reinforcement learning (DQN) + genetic algorithms for routing behavior.

## Project Structure

- `app.py`: The Streamlit web application.
- `preprocessing/`: Includes `data_preprocessing.py` mapping coordinates and extracting sequences.
- `graph/`: Includes `graph_builder.py` representing routes as Directed Graphs.
- `models/`: Contains the PyTorch `lstm_model.py` and `dqn_model.py`.
- `training/`: Contains standalone scripts to train models.
- `optimization/`: Contains algorithms like GA or Dijkstra wrappers to produce shortest path predictions.

## How to Run

1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify / Build Data**:
   Ensure `final_merged_with_stops.csv` is correctly placed inside the `data/` directory.

3. **Train Models** (Optional, for ML research):
   ```bash
   python training/train_lstm.py
   python training/train_dqn.py
   ```

4. **Run Web UI**:
   ```bash
   streamlit run app.py
   ```
