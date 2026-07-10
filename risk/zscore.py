import joblib
import os

# -------------------------------------------------------
# Load Z-score statistics
# -------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)

stats = joblib.load(
    os.path.join(BASE_DIR, "z_statistics.pkl")
)

MEAN = stats["mean"]
STD = stats["std"]


# -------------------------------------------------------
# Calculate Overall Z Score
# -------------------------------------------------------

def calculate_z(age_adjusted_score):

    """
    Calculates the final cognitive Z-score.

    Formula:

        Z = (Age Adjusted Score - Mean Age Adjusted Score)
                /
          Standard Deviation of Age Adjusted Scores
    """

    if STD == 0:
        return 0

    z = (age_adjusted_score - MEAN) / STD

    return z