from .important import grade_convert, points_convert, get_fractions, extrapolate, normal_sigmoid
from django.http import HttpResponse, JsonResponse



# Create your views here.

def termly_test(grades):
    total = sum([grade_convert(i) for i in grades])  # Calculate total points
    avg_points = total / len(grades)  # Work out mean number of points
    # grade = points_convert(avg_points)  # Convert back to grade
    return avg_points


def model(grades, gcse):
    fractions = get_fractions(gcse)

    gcse_points = 0  # Set to 0 if no GCSE for subject
    if gcse:
        gcse_points = grade_convert(grades["GCSE"]) * fractions["GCSE"]
    termly_points = termly_test(grades["termly"]) * fractions["termly"]
    mock_points = grade_convert(grades["mock"]) * fractions["mock"]
    predicted_points = grade_convert(grades["predicted"]) * fractions["predicted"]

    total_points = termly_points + mock_points + gcse_points + predicted_points

    extrapolation_points = extrapolate(grades["termly"])
    attainment_points = normal_sigmoid(grades["termly"])

    rest = fractions["extrapolation"] * extrapolation_points + \
        fractions["total_points"] * total_points + \
        fractions["attainment"] * attainment_points

    coursework_points = grade_convert(grades["coursework"])

    end = grades["coursework_percent"] * coursework_points + \
        grades["others_percent"] * rest

    result = {"points": end, "grade": points_convert(end)}
    print(end, points_convert(end))
    return result


def grades(request, details=None):
    grades = {}
    g = details.split("/")
    grades["predicted"] = g[0]
    grades["mock"] = g[1]
    grades["coursework"] = g[2]
    grades["coursework_percent"] = int(g[3])/100
    grades["others_percent"] = 1 - grades["coursework_percent"]
    grades["termly"] = list(g[4])
    gcse = g[5]
    if gcse == "true":
        grades["GCSE"] = g[6]
        gcse = True
    else:
        gcse = False

    result = model(grades, gcse)
    return JsonResponse(result)


def index(request):
    return HttpResponse("This will be called when no URL is given.")
