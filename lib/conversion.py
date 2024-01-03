import numpy as np
import colour

from lib import datasets


def Lab_to_RGB(Lab, input_ill, output_ill, rgb_colorspace):
    rgb = None  # Initialize rgb outside the try blocks

    try:
        XYZ = colour.Lab_to_XYZ(
            Lab=Lab,
            illuminant=datasets.illuminant_dict["CIE 1931"][input_ill]
        )
        try:
            np.testing.assert_array_less(XYZ, 1.0)
            rgb = colour.XYZ_to_RGB(
                XYZ=XYZ,
                colourspace=rgb_colorspace,
                illuminant=datasets.illuminant_dict["CIE 1931"][output_ill],
                chromatic_adaptation_transform="Bradford"
            )
            rgb = np.clip(rgb, 0, 1)

        except AssertionError:
            print("There is XYZ value > 1.0 at least.")
    except Exception as e:
        print(f"{e} error.")

    return rgb
