import pandas as pd
import pickle
import os

from sklearn.linear_model import LinearRegression

from normalize import (
    normalize_math,
    normalize_stroop,
    normalize_mrt
)

from calculate_ccs import calculate_ccs


# =====================================
# LOAD DATASET
# =====================================

DATASET_PATH = "dataset/all_data.xlsx"

df = pd.read_excel(DATASET_PATH)


# =====================================
# AGE MAPPING
# =====================================

age_map = {
    "18-25": 22,
    "26-35": 30,
    "36-45": 40,
    "46-55": 50,
    "56+": 60
}

df["Age"] = df["Age"].replace(age_map)


# =====================================
# COMPUTE Z SCORES
# =====================================

math_z = []
stroop_z = []
mrt_z = []

for _, row in df.iterrows():

    mz = normalize_math(
        row["num_ability_score"]
    )

    sz = normalize_stroop(
        row["Stroop_error"],
        row["stroop_mean_RT"],
        row["Stroop_interference"]
    )

    rz = normalize_mrt(
        row["MR_acc"],
        row["MR_reaction"],
        row["MR_spatial_score"],
        row["MR_high_angle_accuracy"]
    )

    math_z.append(mz)
    stroop_z.append(sz)
    mrt_z.append(rz)


df["math_z"] = math_z
df["stroop_z"] = stroop_z
df["mrt_z"] = mrt_z


# =====================================
# COMPUTE CCS
# =====================================

df["CCS"] = df.apply(
    lambda x: calculate_ccs(
        x["math_z"],
        x["stroop_z"],
        x["mrt_z"]
    ),
    axis=1
)


# =====================================
# TRAIN LINEAR REGRESSION
# =====================================

X = df[["Age"]]

y = df["CCS"]

model = LinearRegression()

model.fit(X, y)


# =====================================
# SAVE MODEL
# =====================================

output = os.path.join(
    os.path.dirname(__file__),
    "regression_model.pkl"
)

with open(output, "wb") as f:
    pickle.dump(model, f)


print("--------------------------------")

print("Regression model trained.")

print("Saved to:")

print(output)

print("--------------------------------")