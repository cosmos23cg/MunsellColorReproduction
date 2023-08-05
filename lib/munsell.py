import csv
import os.path

import colour
import numpy as np

from lib import untitle


class MunsellColor:
    def __init__(self, file_path: str, illuminant: str = None) -> None:
        self.filepath = file_path
        self.illuminant = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer'][illuminant]
        self.data = self._readFile()

    def _readFile(self):
        with open(self.filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            data = list(reader)
        return np.array(data)

    def hueFileName(self):
        return os.path.basename(self.filepath)[:-4]

    def HVC(self) -> np.ndarray:
        """
        Read from CSV file
        """
        h_index, v_index, c_index = 0, 1, 2
        return np.array(self.data[:, [h_index, v_index, c_index]])

    def XYZn(self) -> np.ndarray:
        return np.array(colour.Lab_to_XYZ(self.Lab(), illuminant=self.illuminant))

    def xyY(self) -> np.ndarray:
        return np.array(colour.XYZ_to_xyY(self.XYZn(), illuminant=self.illuminant))

    def RGB(self) -> np.ndarray:
        """
        Read from CSV file, but if the RGB column is empty, RGB will convert by Lab()
        """
        r_index, g_index, b_index = 3, 4, 5
        if (self.data[:, r_index] == '').any():
            # return untitle.CustomXYZ2AdobeRGB.XYZ2AdobeRGB(self.XYZn())
            return untitle.Lab_to_RGB(self.XYZn(), self.illuminant)
        else:
            return np.array(self.data[:, [r_index, g_index, b_index]]).astype(float)

    def Lab(self) -> np.ndarray:
        """
        Read from CSV file
        """
        L_index, a_index, b_index = 6, 7, 8
        return np.array(self.data[:, [L_index, a_index, b_index]]).astype(float)
