import numpy as np


def grade_convert(grade):
    grade = grade.upper()
    if grade == "A*":
        return 56
    if grade == "A":
        return 48
    if grade == "B":
        return 40
    if grade == "C":
        return 32
    if grade == "D":
        return 24
    if grade == "E":
        return 16
    else:
        return 0


def points_convert(points):
    if points >= 52:
        return "A*"
    if points >= 44:
        return "A"
    if points >= 36:
        return "B"
    if points >= 28:
        return "C"
    if points >= 20:
        return "D"
    if points >= 12:
        return "E"
    else:
        return "U"


def get_fractions(gcse):
    fractions = {}
    if gcse:
        fractions["predicted"] = 0.3
        fractions["mock"] = 0.35
        fractions["GCSE"] = 0.10
        fractions["termly"] = 1 - fractions["predicted"] - fractions["mock"] - fractions["GCSE"]
    else:
        fractions["predicted"] = 0.3
        fractions["mock"] = 0.4
        fractions["termly"] = 1 - fractions["predicted"] - fractions["mock"]

    fractions["extrapolation"] = 0.1
    fractions["attainment"] = 0.2
    fractions["total_points"] = 1 - fractions["extrapolation"] - fractions["attainment"]

    return fractions


def attainment(grades):
    number_of_grades = len(grades)
    grade_order = ["U", "E", "D", "C", "B", "A", "A*"]

    count = {"A*": 0,
             "A": 0,
             "B": 0,
             "C": 0,
             "D": 0,
             "E": 0,
             "U": 0}

    att = {"A*": 0,
           "A": 0,
           "B": 0,
           "C": 0,
           "D": 0,
           "E": 0,
           "U": 0}

    for grade in grades:
        count[grade] += 1

    for key in att.keys():
        above = 0
        for grade in grades:
            if grade_order.index(grade) >= grade_order.index(key):
                above += 1
        att[key] = round(above/number_of_grades,3)
    return att


def extrapolate(grades):
    y = np.array([grade_convert(i) for i in grades])
    x = np.array([i for i in range(1, len(grades)+1)])

    denominator = x.dot(x) - x.mean() * x.sum()

    m = (x.dot(y) - y.mean() * x.sum()) / denominator
    b = (y.mean() * x.dot(x) - x.mean() * x.dot(y)) / denominator

    end = round((len(grades)+1)*m + b, 3)
    return end


def multiplier(x):
    k = 0.015  # Larger k - harsher on inconsistency
    return 2 / (np.exp(k*x) + 1)


def normal_sigmoid(grades):
    points = [grade_convert(grade) for grade in grades]

    mean = sum(points) / len(points)

    variance = sum(map(lambda x: ((x-mean)**2)/len(points), points))
    std = round(variance**0.5, 3)

    mean_samples = np.random.normal(loc=mean, scale=variance/len(points), size=10000)
    mean_mean_samples = np.mean(mean_samples)

    final = multiplier(std) * mean_mean_samples

    return final
