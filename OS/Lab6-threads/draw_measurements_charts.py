import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

dataset = pd.read_csv("measurements.csv")

unique_t = dataset["t"].unique()
durations_categorized = {t: dataset["duration"][dataset["t"] == t] for t in unique_t}
duration_means = {t: durations_categorized[t].mean() for t in unique_t}

# fit LSE line
model = LinearRegression()
X = np.array(dataset["t"])
y = dataset["duration"]
result = model.fit(X.reshape(-1, 1), y)
print(f"{result.coef_=}")

b0 = result.intercept_
b1 = result.coef_[0]

fig, ax = plt.subplots()
ax.set_title(f"n = {dataset['n'][0]}, k = {dataset['k'][0]}")

ax.plot(duration_means.keys(), duration_means.values(), alpha=0.5)
ax.boxplot(durations_categorized.values(), meanline=True, showmeans=True)
ax.set_xticklabels(durations_categorized.keys())

xlim = ax.get_xlim()
A, B = (xlim[0], b0 + b1*xlim[0]), (xlim[1], b0 + b1*xlim[1])
ax.axline((xlim[0], b0 + b1*xlim[0]), (xlim[1], b0 + b1*xlim[1]), c="r", linestyle="--", label=f"{b0} + {b1}*t")

ax.set_xlabel("Number of Threads (t)")
ax.set_ylabel("Duration (seconds)")

ax.legend()

plt.savefig("performance.png") 


