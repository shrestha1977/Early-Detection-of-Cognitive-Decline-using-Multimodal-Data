import pandas as pd
import pickle
import os

DATASET_PATH = "dataset/all_data.xlsx"

df = pd.read_excel(DATASET_PATH)

required_columns = [
    "num_ability_score",
    "Stroop_error",
    "stroop_mean_RT",
    "Stroop_interference",
    "MR_acc",
    "MR_reaction",
    "MR_spatial_score",
    "MR_high_angle_accuracy"
]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in dataset.")


statistics = {
    "math_mean": df["num_ability_score"].mean(),
    "math_std": df["num_ability_score"].std(),

    "Stroop_error_mean": df["Stroop_error"].mean(),
    "Stroop_error_std": df["Stroop_error"].std(),

    "stroop_mean_RT_mean": df["stroop_mean_RT"].mean(),
    "stroop_mean_RT_std": df["stroop_mean_RT"].std(),

    "Stroop_interference_mean": df["Stroop_interference"].mean(),
    "Stroop_interference_std": df["Stroop_interference"].std(),

    "MR_acc_mean": df["MR_acc"].mean(),
    "MR_acc_std": df["MR_acc"].std(),

    "MR_reaction_mean": df["MR_reaction"].mean(),
    "MR_reaction_std": df["MR_reaction"].std(),

    "MR_spatial_score_mean": df["MR_spatial_score"].mean(),
    "MR_spatial_score_std": df["MR_spatial_score"].std(),

    "MR_high_angle_accuracy_mean": df["MR_high_angle_accuracy"].mean(),
    "MR_high_angle_accuracy_std": df["MR_high_angle_accuracy"].std()
}


output_file = os.path.join(
    os.path.dirname(__file__),
    "statistics.pkl"
)

with open(output_file, "wb") as f:
    pickle.dump(statistics, f)

print("=====================================")
print("Statistics successfully created.")
print("Saved to:", output_file)
print("=====================================")

print("\nDataset Statistics\n")

for key, value in statistics.items():
    print(f"{key:20s}: {value:.4f}")
