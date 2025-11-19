import pandas as pd
import matplotlib.pyplot as plt

dtype_mapping = {
    "n": "int32",
    "k": "int32",
    "t": "int32",
    "duration": "float64"
}
dataset = pd.read_csv("measurements.csv", dtype=dtype_mapping)

unique_t = dataset["t"].unique()
data_per_t = {t: dataset[dataset["t"] == t] for t in unique_t}

m = dataset['n'][0] * dataset['k'][0]

fig, ax = plt.subplots()
ax.set_title(f"m = {m}")

for t, data in data_per_t.items():
    ax.plot(data["k"], data["duration"], label=f"t = {t}")

all_ks = sorted(dataset["k"].unique())
ax.set_xticks(all_ks)

x_labels = [f"{k}\n{m//k}" for k in all_ks]
k=all_ks[0]
x_labels[0] = f"{k=}\nn={m//k}"
ax.set_xticklabels(x_labels)
ax.set_ylabel("Duration (seconds)")

ax.legend()
plt.savefig("search_k_t.png") 

best_duration_idx = dataset["duration"].argmin()
print(f"Shortest duration for\n{dataset.iloc[best_duration_idx]}")