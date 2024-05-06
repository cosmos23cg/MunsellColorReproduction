import colour
import numpy as np

import math
import csv

from lib import conversion, error


class MunsellColor:
    """
    This class load the csv data and save as object which have "HSV", "Lab", "nXYZ", "xyY" and "xy" attribute.

    Attribute: COLORDICT, HVC, Lab
    """
    def __init__(self, data: list):
        # self.rgb_header = ['h', 'v', 'c', 'r', 'g', 'b', 'l*', 'a*', 'b*']
        # self.cmyk_header = ['h', 'v', 'c', 'c', 'm', 'y', 'k', 'l*', 'a*', 'b*']
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

    # def _check_condition(self, conditions):
    #     """
    #     Find out the index that the *args appears in list.
    #     """
    #     result = ""
    #     for idx, value in enumerate(self.grouped_data['header']):
    #         for condition in conditions:
    #             if condition in value:
    #                 result += condition
    #     return result if len(result) > 0 else None

    # def _get_statement(self):
    #     """
    #     Required the list if the csv header has matched the 'L*a*b*', 'xyY', or 'RGB'.
    #     """
    #     result_ls = []
    #     conditions = [
    #         ('L*', 'a*', 'b*'),
    #         ('x', 'y', 'Y'),
    #         ('R', 'G', 'B')
    #     ]
    #
    #     for condition in conditions:
    #         result = self._check_condition(condition)
    #         if result is not None:
    #             result_ls.append(result)
    #
    #     return result_ls

    # def _check_idx(self, *args):
    #     idx_ls = []
    #     for idx, value in enumerate(self.grouped_data['header']):
    #         if any(arg in value for arg in args):
    #             idx_ls.append(idx)
    #     return idx_ls

    # def _extract_val_by_idx(self, index_list: list, np_dtype, clear_dict=None) -> dict | None:
    #     """
    #     Parameters: DICT is the return dictionary from whose function.
    #     index_list is the required index.
    #     Returns: required Dictionary
    #     """
    #     output_dict = {}
    #     munsell_data_clone = self.grouped_data.copy()
    #     min_idx, max_idx = min(index_list), max(index_list)
    #     for key in munsell_data_clone.keys():
    #         if key != 'header':
    #             extract_value = [x[min_idx:max_idx + 1] for x in munsell_data_clone[key]]
    #             if any(value == "" for value in extract_value[0]):
    #                 return None
    #             else:
    #                 output_dict[key] = np.array(extract_value).astype(np_dtype)
    #     return output_dict

    # def Lab(self, clear_dict=None) -> dict:
    #     # TODO: Converted Lab from xyY, XYZ, RGB
    #     """
    #     If Lab index is empty. then find header list if there are xy, xyY, XYZ, RGB
    #     Returns: Lab value dictionary
    #     """
    #     extract_Lab_dict = self._extract_val_by_idx(self._check_idx('L*', 'a*', 'b*'), np.float32)
    #     if extract_Lab_dict is not None:
    #         print(f"** Lab required from file. \n {extract_Lab_dict.keys()}")
    #         return extract_Lab_dict

    # def RGB(self, clear_dict=None):
    #     # TODO: used XYZ convert to RGB
    #     """
    #     Read from CSV
    #     Return: RGB in normalization [0, 1]
    #     """
    #     rgb_dict = {} if clear_dict is None else clear_dict
    #
    #     extract_rgb_dict = self._extract_val_by_idx(self._check_idx('R', 'G', 'B'), np.uint8)
    #     if extract_rgb_dict is not None:
    #         for key, value in extract_rgb_dict.items():
    #             value = value / 255.0  # normalization
    #             extract_rgb_dict[key] = value
    #         print(f"** RGB required from file. \n {extract_rgb_dict.keys()}")
    #         return extract_rgb_dict
    #
    #     elif 'L*a*b*' in self.statement:
    #         extract_Lab_dict = self._extract_val_by_idx(self._check_idx('L*', 'a*', 'b*'), np.float32)
    #         for key, value in extract_Lab_dict.items():
    #             rgb = conversion.Lab_to_RGB(value, "D50", "D50", "sRGB")
    #             rgb_dict[key] = rgb
    #         print(f"** RGB convert from L*a*b* \n {rgb_dict.keys()}")
    #         return rgb_dict


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

