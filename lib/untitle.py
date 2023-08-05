import colour
import numpy as np

ILLUMINANTS = {
    'RGB TO XYZ': {
        'D65': np.array(
            ([0.57667, 0.18556, 0.18823],
             [0.29734, 0.62736, 0.07529],
             [0.02703, 0.07069, 0.99134])
        ),
        'D50': np.array(
            ([0.6097559, 0.2052401, 0.1492240],
             [0.3111242, 0.6256560, 0.0632197],
             [0.0194811, 0.0608902, 0.7448387])
        )
    },
    'XYZ TO RGB': {
        'D65': np.array(
            ([2.04159, -0.56501, -0.34473],
             [-0.96924, 1.87597, 0.04156],
             [0.01344, -0.11836, 1.01517])
        ),
        'D50': np.array(
            ([1.9624274, -0.6105343, -0.3413404],
             [-0.9787684, 1.9161415, 0.0334540],
             [0.0286869, -0.1406752, 1.3487655])
        )
    }
}


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


class CustomXYZ2AdobeRGB:
    """
    This method is converted by D65.
    """
    def __init__(self):
        pass

    @staticmethod
    def gamma_RGB(RGB):
        return [0 if x < 0 else pow(x, (1 / 2.19921875)) for x in RGB]

    @staticmethod
    def XYZ2AdobeRGB(XYZ):
        output = []
        for i in range(len(XYZ)):
            RGB = np.matmul(XYZ[i], ILLUMINANTS['XYZ TO RGB']['D50'])
            RGB = CustomXYZ2AdobeRGB.gamma_RGB(RGB)
            RGB = np.round([x * 255 for x in RGB])
            output.append(RGB)
        return np.array(output).astype(int)


def Lab_to_RGB(XYZ: np.ndarray, illuminant: list):
    RGB = colour.XYZ_to_RGB(XYZ,
                            illuminant_XYZ=illuminant,
                            illuminant_RGB=illuminant,
                            matrix_XYZ_to_RGB=colour.RGB_COLOURSPACES['Adobe RGB (1998)'].matrix_XYZ_to_RGB,
                            chromatic_adaptation_transform='Bradford')
    RGB = clip_rgb(RGB)
    RGB *= 255
    RGB = np.round(RGB).astype(int)
    return RGB


def clip_rgb(rgb_array: np.ndarray) -> np.ndarray:
    return np.clip(rgb_array, 0, 255)
