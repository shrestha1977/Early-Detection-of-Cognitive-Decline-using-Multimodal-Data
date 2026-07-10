import math

def classify(z):

    probability = 1 / (1 + math.exp(z))

    if probability < 0.33:
        risk = "Green"

    elif probability < 0.66:
        risk = "Yellow"

    else:
        risk = "Red"

    return risk, probability