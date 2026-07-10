"""
Age Adjustment Module

Formula:

Age Adjusted Score = CCS - Expected Score

where

CCS = Composite Cognitive Score

Expected Score = Predicted by Linear Regression
"""


def age_adjusted_score(ccs, expected_score):
    """
    Calculates the age-adjusted cognitive score.

    Parameters
    ----------
    ccs : float
        Composite Cognitive Score

    expected_score : float
        Expected score predicted by the regression model

    Returns
    -------
    float
        Age Adjusted Score
    """

    return ccs - expected_score