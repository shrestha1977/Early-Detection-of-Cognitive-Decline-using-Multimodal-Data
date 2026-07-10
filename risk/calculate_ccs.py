"""
Composite Cognitive Score (CCS)

Architecture:

Task Scores
      ↓
Z-Score Normalization
      ↓
CCS = (Math_Z + Stroop_Z + MRT_Z) / 3
"""

def calculate_ccs(math_z, stroop_z, mrt_z):
    """
    Calculates the Composite Cognitive Score.

    Parameters
    ----------
    math_z : float
        Z-score of Numerical Ability Test

    stroop_z : float
        Z-score of Stroop Test

    mrt_z : float
        Z-score of Mental Rotation Test

    Returns
    -------
    float
        Composite Cognitive Score (CCS)
    """

    ccs = (math_z + stroop_z + mrt_z) / 3

    return ccs