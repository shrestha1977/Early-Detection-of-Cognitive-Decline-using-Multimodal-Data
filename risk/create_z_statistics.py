import os
import pickle
import pandas as pd

from normalize import (
    normalize_math,
    normalize_stroop,
    normalize_mrt
)

from calculate_ccs import calculate_ccs
from expected_score import expected_score
from age_adjust import age_adjusted_score


DATASET_PATH = "dataset/all_data.xlsx"

df = pd.read_excel(DATASET_PATH)


age_map = {
    "18-25": 22,
    "26-35": 30,
    "36-45": 40,
    "46-55": 50,
    "56+": 60
}

df["Age"] = df["Age"].replace(age_map)


age_adjusted_scores = []

for _, row in df.iterrows():

    math_z = normalize_math(
        row["num_ability_score"]
    )

    stroop_z = normalize_stroop(
        row["Stroop_error"],
        row["stroop_mean_RT"],
        row["Stroop_interference"]
    )

    mrt_z = normalize_mrt(
        row["MR_acc"],
        row["MR_reaction"],
        row["MR_spatial_score"],
        row["MR_high_angle_accuracy"]
    )

    ccs = calculate_ccs(
        math_z,
        stroop_z,
        mrt_z
    )

    exp = expected_score(
        row["Age"]
    )

    adj = age_adjusted_score(
        ccs,
        exp
    )

    age_adjusted_scores.append(adj)


z_statistics = {

    "mean": sum(age_adjusted_scores) / len(age_adjusted_scores),

    "std": pd.Series(age_adjusted_scores).std()

}


output = os.path.join(
    os.path.dirname(__file__),
    "z_statistics.pkl"
)

with open(output, "wb") as f:
    pickle.dump(z_statistics, f)

print("-------------------------------------")
print("Z statistics created successfully")
print(output)
print("-------------------------------------")

print()

print("Mean :", z_statistics["mean"])
print("Std  :", z_statistics["std"])
