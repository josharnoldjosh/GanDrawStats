import os
import json
import plotly.graph_objects as go
from collections import Counter, defaultdict

class Data:

    def __init__(self, split_path, split_name=""):
        self.split_name = split_name
        with open(split_path, 'r') as file:
            self.data = json.load(file)
            self.build_map()

    def get_strategies(self, dialog):
        results = []
        for turn in dialog['dialog']:
            results += [turn['teller_label'], turn['drawer_label']]
        counts = Counter(results)
        return list(counts.items())

    def get_dialog_map(self, dialog):
        dialog_map = {}
        for (key, count) in self.get_strategies(dialog):
            dialog_map.update({f"{key}_{count}":dialog['score']})
        return dialog_map

    def build_map(self):
        data_map = defaultdict(list)
        for dialog in self.data:
            for (key, value) in self.get_dialog_map(dialog).items():
                data_map[key].append(value)            
        self.data_map = data_map

    def get_x_y(self, strategy=""):
        x = []
        y = []
        z = []
        for i in range(1, 7):
            try:
                strat = self.data_map[f"{strategy}_{i}"]
                y.append(sum(strat)/len(strat))
                x.append(i)
                z.append(len(strat))
            except:
                pass
        return x, y, z

    def plot(self, strategy="Describe_Image"):
        x, y, z = self.get_x_y(f"{strategy}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=f'{strategy}',  marker = dict(size=20, color=z, colorscale='Viridis', showscale=True)))
        fig.update_layout(
            title=f"# of Times {strategy} Used Against Mean Conversation Score for {self.split_name}.",
            xaxis_title=f"{strategy} Usage",
            yaxis_title="Mean Score",
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="#7f7f7f"
            )
        )
        fig.show()

    def plot_all(self):
        for strat in ["Describe_Image", "Request_Correction", "Elicit_Information", "Correct_Drawing"]:
            self.plot(strat)

path = os.path.join(os.getcwd(), 'Split Data', 'internal.json')
data = Data(path, "First UCD Students")
data.plot_all()