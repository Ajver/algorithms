import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

dataset = pd.read_csv("measurements.csv")

unique_t = dataset["t"].unique()
durations_categorized = {t: dataset["duration"][dataset["t"] == t] for t in unique_t}
duration_means = {t: durations_categorized[t].mean() for t in unique_t}

corr = np.corrcoef(dataset["t"], dataset["duration"])[0, 1]
print(f"{corr=}")

# fit LSE line
X = np.ones((dataset["t"].shape[0], 2))
X[:, 1] = dataset["t"]
y = dataset["duration"]
model = sm.OLS(y, X)
result = model.fit()
print(f"{result.summary()}")

b0 = result.params.iloc[0]
b1 = result.params.iloc[1]
p_value = result.pvalues[1]

fig, ax = plt.subplots()
ax.set_title(f"n = {dataset['n'][0]}, k = {dataset['k'][0]}")

ax.plot(duration_means.keys(), duration_means.values(), alpha=0.5)
ax.boxplot(durations_categorized.values(), meanline=True, showmeans=True)
ax.set_xticklabels(durations_categorized.keys())

xlim = ax.get_xlim()
A, B = (xlim[0], b0 + b1*xlim[0]), (xlim[1], b0 + b1*xlim[1])
ax.axline((xlim[0], b0 + b1*xlim[0]), (xlim[1], b0 + b1*xlim[1]), c="r", linestyle="--", label=f"{b0} + {b1}*t\np = {p_value}")

ax.set_xlabel("Number of Threads (t)")
ax.set_ylabel("Duration (seconds)")

ax.legend()

plt.savefig("performance.png") 


