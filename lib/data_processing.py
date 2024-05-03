import csv
import math


def read_csv(input_path, skip_lines=None):
    with open(input_path, 'r') as csvfile:
        reader = csv.reader(csvfile)

        if skip_lines is None:
            return [line for line in reader]

        for _ in range(skip_lines):
            next(reader)

        return [line for line in reader]


def group_by(ipt_lst: list, group_key: int) -> dict:
    """
    ipt_lst:
        input_list
    group_key:

    """
    result = {}

    for sub_lst in ipt_lst:
        if sub_lst[group_key] not in result:
            result[sub_lst[group_key]] = []

        result[sub_lst[group_key]].append(sub_lst)

    return result


def check_float(lst: list):
    for i in range(-3, 0, 1):
        lst[i] = float(lst[i])
    return lst


def is_nested(lst: list):
    for item in lst:
        if isinstance(item, list):
            return True
    return False


def cie_1976_cab(a, b):
    """
    Calculate Cab value from a and b values.

    Parameters:
        a (float): a value.
        b (float): b value.

    Returns:
        float: Cab value.
    """
    return math.sqrt(float(a) ** 2 + float(b) ** 2)


def triangle_area(p1, p2, p3):
    return abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p3[1])) / 2.0)


def area_ratio(ref, points: list):
    result_lst = []
    for i in range(len(points)):
        ratio = (points[i] / ref) * 100
        result_lst.append([points[i], ratio])

    return result_lst

