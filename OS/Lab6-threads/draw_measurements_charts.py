import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("measurements.csv")

plt.scatter(dataset["t"], dataset["duration"])
plt.title(f"n = {dataset['n'][0]}, k = {dataset['k'][0]}")

plt.xlabel("Number of Threads (t)")
plt.ylabel("Duration (seconds)")

plt.savefig("performance.png") 
