import colour
import numpy as np

import math
import csv

from lib import conversion, error


class MunsellColor:
    def __init__(self, data: list):
        self.grouped_data = self._group_hue(data)

    @staticmethod
    def _group_hue(input_list):
        # lw = [x.lower() for x in input_list[0]]

        grouped = {'header': input_list[0]}
        group_temp = group_by(input_list[1:], 0)
        grouped.update(group_temp)

        return grouped

    def _require_index(self, value):
        lw = [x.lower() for x in self.grouped_data['header']]
        idxs = [lw.index(x) for x in value]

        return idxs

    def _extract_value(self, idxs):
        output = {key: [] for key in self.grouped_data.keys() if key != 'header'}

        for idx, (key, values) in enumerate(self.grouped_data.items()):
            # skip header
            if key == 'header':
                continue

            for value in values:
                value = [value[x] for x in idxs]

                if any(len(x) == 0 for x in value):
                    return None

                value = [float(x) for x in value]
                output[key].append(value)

        return output

    def vc(self):
        idxs = self._require_index(['v', 'c'])
        vc_dict = self._extract_value(idxs)

        return vc_dict

    def lab(self):
        idxs = self._require_index(['l*', 'a*', 'b*'])
        lab_dict = self._extract_value(idxs)

        if lab_dict is None:
            raise error.InputDataEmptyError

        return lab_dict

    def rgb(self):
        idxs = self._require_index(['r', 'g', 'b'])
        rgb_dict = self._extract_value(idxs)

        if rgb_dict is not None:
            return rgb_dict


class Gamut:
    def __init__(self, color_space: str):
        self.color_space_prim = colour.RGB_COLOURSPACES[color_space].primaries
        self.x1, self.y1 = self.color_space_prim[0][0], self.color_space_prim[0][1]
        self.x2, self.y2 = self.color_space_prim[1][0], self.color_space_prim[1][1]
        self.x3, self.y3 = self.color_space_prim[2][0], self.color_space_prim[2][1]

    @staticmethod
    def _triangleArea(x1, y1, x2, y2, x3, y3):
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y3)) / 2.0)

    def isInside_AreaMethod(self, xyY_arr):
        """
        Only can use when the parameter is integer
        """
        # Triangle area
        gamut_area = self._triangleArea(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)

        x, y = xyY_arr[0], xyY_arr[1]
        # point Triangle
        PBC = self._triangleArea(x, y, self.x2, self.y2, self.x3, self.y3)
        PAC = self._triangleArea(self.x1, self.y1, x, y, self.x3, self.y3)
        PAB = self._triangleArea(self.x1, self.y1, self.x2, self.y2, x, y)

        if gamut_area == PBC + PAC + PAB:
            print(f"{round(x, 3), round(y, 3)} is inside the gamut")
            return True
        else:
            print(f"{round(x, 3), round(y, 3)} is outside the gamut")
            return False

    def isInside_CrossMethod(self, point):
        xp, yp = point[0], point[1]
        c1 = (self.x2 - self.x1) * (yp - self.y1) - (self.y2 - self.y1) * (xp - self.x1)
        c2 = (self.x3 - self.x2) * (yp - self.y2) - (self.y3 - self.y2) * (xp - self.x2)
        c3 = (self.x1 - self.x3) * (yp - self.y3) - (self.y1 - self.y3) * (xp - self.x3)
        if (c1 < 0 and c2 < 0 and c3 < 0) or (c1 > 0 and c2 > 0 and c3 > 0):
            return True
        else:
            return False


def read_csv(input_path, skip_lines=None):
    """
    Read csv and return list.
    """
    with open(input_path, 'r') as csvfile:
        reader = csv.reader(csvfile)

        if skip_lines is None:
            return [line for line in reader]

        # skip the row by manual entry
        for _ in range(skip_lines):
            next(reader)

        return [line for line in reader]


def group_by(ipt_lst: list, group_col: int) -> dict:
    """
    ipt_lst:
        input_list
    group_key:

    """
    result = {}

    for sub_lst in ipt_lst:
        group_key = sub_lst[group_col]

        if group_key not in result:
            result[group_key] = []

        result[group_key].append(sub_lst)

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

