import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("measurements.csv")

unique_t = dataset["t"].unique()
durations_categorized = {t: dataset["duration"][dataset["t"] == t] for t in unique_t}
duration_means = {t: durations_categorized[t].mean() for t in unique_t}

fig, ax = plt.subplots()
ax.set_title(f"n = {dataset['n'][0]}, k = {dataset['k'][0]}")

ax.plot(duration_means.keys(), duration_means.values(), alpha=0.5)
ax.boxplot(durations_categorized.values(), meanline=True, showmeans=True)
ax.set_xticklabels(durations_categorized.keys())

ax.set_xlabel("Number of Threads (t)")
ax.set_ylabel("Duration (seconds)")

plt.savefig("performance.png") 
