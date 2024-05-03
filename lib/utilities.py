from pathlib import Path
from typing import Optional

import colour
import csv
import numpy as np

from lib import conversion


# def


class LoadFolder:
    """
    instance this class auto read and save file data as dictionary.
    Load folder and read the sub file as dictionary. The key is the file name and values is the file contents.
    """
    def __init__(self, file_path, file_format):
        self.p = Path(file_path)
        self.fmt = file_format
        self.color_dict = {}
        self._read_file()

    def _sub_files(self):
        """
        Fetch the file path with the specific data format
        """
        if not self.p.exists():
            raise FileNotFoundError(f'Folder {self.p} not found.')

        if self.p.is_dir():
            return list(self.p.glob("**/*" + self.fmt))
        elif self.p.is_file():
            return [self.p]
        else:
            raise FileExistsError(f"Foldr {self.p} not found.")

    def _read_file(self):
        """
        Read the file path and save as dictionary.
        """
        error_file = []
        for file in self._sub_files():
            if file.is_file():
                try:
                    with open(file, "r") as csvfile:
                        if self.fmt == '.csv':
                            reader = csv.reader(csvfile)
                            self.color_dict["header"] = next(reader)  # obtained the first row from csv
                            # TODO: this will exclude the N.csv
                            if len(file.stem) > 2:  # if the file name character more than 2
                                separator = '_' if '_' in file.stem else "-"
                                hue_title = file.stem.split(separator)[0]
                                self.color_dict[hue_title] = list(reader)
                except csv.Error as e:
                    error_file.append(file)
                    print(f"Error reading CSV file {file}: {e}")  # Handle csv error

class MunsellColor:
    """
    This class load the csv data and save as object which have "HSV", "Lab", "nXYZ", "xyY" and "xy" attribute.

    Attribute: COLORDICT, HVC, Lab
    """

    def __init__(self, file_path, file_format):
        self.p = Path(file_path)
        self.fmt = file_format
        self.munsell_dict: Optional[dict] = LoadFolder(self.p, self.fmt).color_dict
        self.statement = self._get_statement()

    def _check_condition(self, conditions):
        """
        Find out the index that the *args appears in list.
        """
        result = ""
        for idx, value in enumerate(self.munsell_dict['header']):
            for condition in conditions:
                if condition in value:
                    result += condition
        return result if len(result) > 0 else None

    def _get_statement(self):
        """
        Required the list if the csv header has matched the 'L*a*b*', 'xyY', or 'RGB'.
        """
        result_ls = []
        conditions = [
            ('L*', 'a*', 'b*'),
            ('x', 'y', 'Y'),
            ('R', 'G', 'B')
        ]

        for condition in conditions:
            result = self._check_condition(condition)
            if result is not None:
                result_ls.append(result)

        return result_ls

    def _check_idx(self, *args):
        idx_ls = []
        for idx, value in enumerate(self.munsell_dict['header']):
            if any(arg in value for arg in args):
                idx_ls.append(idx)
        return idx_ls

    def _extract_val_by_idx(self, index_list: list, np_dtype, clear_dict=None) -> dict | None:
        """
        Parameters: DICT is the return dictionary from whose function.
        index_list is the required index.
        Returns: required Dictionary
        """
        output_dict = {}
        munsell_data_clone = self.munsell_dict.copy()
        min_idx, max_idx = min(index_list), max(index_list)
        for key in munsell_data_clone.keys():
            if key != 'header':
                extract_value = [x[min_idx:max_idx + 1] for x in munsell_data_clone[key]]
                if any(value == "" for value in extract_value[0]):
                    return None
                else:
                    output_dict[key] = np.array(extract_value).astype(np_dtype)
        return output_dict

    def VC(self, clear_dict=None) -> dict:
        """
        find the hVC index, then print the HVC value in dictionary by indexing.
        Returns: HVC value dictionary
        """
        extract_VC_DICT = self._extract_val_by_idx(self._check_idx('V', "C"), np.uint8)
        if extract_VC_DICT is not None:
            print(f"** VC required from file. \n {extract_VC_DICT.keys()}")
            return extract_VC_DICT

    def Lab(self, clear_dict=None) -> dict:
        # TODO: Converted Lab from xyY, XYZ, RGB
        """
        If Lab index is empty. then find header list if there are xy, xyY, XYZ, RGB
        Returns: Lab value dictionary
        """
        extract_Lab_dict = self._extract_val_by_idx(self._check_idx('L*', 'a*', 'b*'), np.float32)
        if extract_Lab_dict is not None:
            print(f"** Lab required from file. \n {extract_Lab_dict.keys()}")
            return extract_Lab_dict

    def RGB(self, clear_dict=None):
        # TODO: used XYZ convert to RGB
        """
        Read from CSV
        Return: RGB in normalization [0, 1]
        """
        rgb_dict = {} if clear_dict is None else clear_dict

        extract_rgb_dict = self._extract_val_by_idx(self._check_idx('R', 'G', 'B'), np.uint8)
        if extract_rgb_dict is not None:
            for key, value in extract_rgb_dict.items():
                value = value / 255.0  # normalization
                extract_rgb_dict[key] = value
            print(f"** RGB required from file. \n {extract_rgb_dict.keys()}")
            return extract_rgb_dict

        elif 'L*a*b*' in self.statement:
            extract_Lab_dict = self._extract_val_by_idx(self._check_idx('L*', 'a*', 'b*'), np.float32)
            for key, value in extract_Lab_dict.items():
                rgb = conversion.Lab_to_RGB(value, "D50", "D50", "sRGB")
                rgb_dict[key] = rgb
            print(f"** RGB convert from L*a*b* \n {rgb_dict.keys()}")
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
