import os.path
import subprocess


if os.path.exists("measurements.csv"):
    os.remove("measurements.csv")

m = 120

for k in range(1, m//2 + 1):
    if m % k != 0:
        # not divisible!
        continue

    n = m // k

    for t in range(1, 5):
        print(f"{n=}, {k=}, {t=}")
        subprocess.run(["./psum", str(n), str(k), str(t)])