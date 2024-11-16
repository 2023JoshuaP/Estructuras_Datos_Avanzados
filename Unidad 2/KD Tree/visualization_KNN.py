import pandas as pd
import matplotlib.pyplot as plt

brute_force_data = pd.read_csv("execution_times_bruce_force_k_diferent.csv")
kd_tree_data = pd.read_csv("execution_times_vs_k.csv")

datasets = brute_force_data['File Name'].unique()

for dataset in datasets:
    bf_subset = brute_force_data[brute_force_data['File Name'] == dataset]
    kd_subset = kd_tree_data[kd_tree_data['File Name'] == dataset]
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(bf_subset['K'], bf_subset['Execution Time (seconds)'], label="Brute Force", marker='o')
    plt.plot(kd_subset['k'], kd_subset['Execution Time (seconds)'], label="KD-Tree", marker='s')
    plt.title(f"Execution Time vs K for Dataset: {dataset}")
    plt.xlabel("K")
    plt.ylabel("Execution Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.show()