from decisionTree import TrafficDecisionTreeModel

model = TrafficDecisionTreeModel(
    max_depth=8
)

model.fit("assets/training/traffic_per_stop.csv")
model.save()

print("Model trained and saved.")