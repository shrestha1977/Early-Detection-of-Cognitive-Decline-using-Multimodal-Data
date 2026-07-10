import pickle
import os
import pandas as pd


# =====================================
# LOAD TRAINED REGRESSION MODEL
# =====================================

model_path = os.path.join(
    os.path.dirname(__file__),
    "regression_model.pkl"
)

with open(model_path, "rb") as f:
    regression_model = pickle.load(f)


# =====================================
# AGE MAPPING
# =====================================

AGE_MAPPING = {
    "18-25": 22,
    "26-35": 30,
    "36-45": 40,
    "46-55": 50,
    "56+": 60
}


# =====================================
# PREDICT EXPECTED SCORE
# =====================================

def expected_score(age):

    """
    Predicts the expected cognitive score
    using the trained regression model.

    Parameters
    ----------
    age : str or int

    Returns
    -------
    float
    """

    if isinstance(age, str):
        age = AGE_MAPPING.get(age, 22)

    X = pd.DataFrame({
        "Age": [age]
    })

    prediction = regression_model.predict(X)

    return float(prediction[0])