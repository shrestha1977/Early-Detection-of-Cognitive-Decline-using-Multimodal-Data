import math

def classify(z):

    if z >= 0:
        risk = "Green"

    elif z >= -1:
        risk = "Yellow"

    else:
        risk = "Red"

    return risk
