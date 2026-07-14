import joblib
import os

BASE_DIR = os.path.dirname(__file__)

stats = joblib.load(
    os.path.join(BASE_DIR, "z_statistics.pkl")
)

MEAN = stats["mean"]
STD = stats["std"]

def calculate_z(age_adjusted_score):

    if STD == 0:
        return 0

    z = (age_adjusted_score - MEAN) / STD

    return z
