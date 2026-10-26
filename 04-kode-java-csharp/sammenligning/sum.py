import time

start = time.perf_counter()
total = 0
for i in range(100_000_000):
    total += i % 7
print(total, f"{time.perf_counter() - start:.2f} s")
