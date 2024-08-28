import numpy as np
import colour

from lib import datasets


def split_lab(arr):
    arr = np.asarray(arr)
    return arr[:, 0], arr[:, 1], arr[:, 2]


def dE_CIE2000(Lab_1, Lab_2, textiles=False):
    # TODO: Fix formula
    # Step 1. Calculate the CIELAB L*, a*, b*, and C*as usual:
    L_1, a_1, b_1 = split_lab(Lab_1)
    L_2, a_2, b_2 = split_lab(Lab_2)

    Cab_1 = np.hypot(a_1, b_1)
    Cab_2 = np.hypot(a_2, b_2)

    # Step 2. Calculate a*,C* and h*:
    C_bar_ab_7 = ((Cab_1 + Cab_2) / 2) ** 7
    G = 0.5 * (1 - np.sqrt(C_bar_ab_7 / C_bar_ab_7 + 25 ** 7))

    a_p_1 = (1 + G) * a_1
    a_p_2 = (1 + G) * a_2

    C_p_1 = np.hypot(a_p_1, b_1)
    C_p_2 = np.hypot(a_p_2, b_2)

    h_p_1 = np.where(
        np.logical_and(b_1 == 0, a_p_1 == 0),
        0,
        np.degrees(np.arctan2(b_1, a_p_1)) % 360,
    )
    h_p_2 = np.where(
        np.logical_and(b_2 == 0, a_p_2 == 0),
        0,
        np.degrees(np.arctan2(b_2, a_p_2)) % 360,
    )

    # Step 3. Calculate DL*, DC* and DH*:
    delta_L_p = L_2 - L_1

    delta_C_p = C_p_2 - C_p_1

    h_p_2_s_1 = h_p_2 - h_p_1
    C_p_1_m_2 = C_p_1 * C_p_2
    delta_h_p = np.select(
        [
            C_p_1_m_2 == 0,
            np.fabs(h_p_2_s_1) <= 180,
            h_p_2_s_1 > 180,
            h_p_2_s_1 < -180,
        ],
        [
            0,
            h_p_2_s_1,
            h_p_2_s_1 - 360,
            h_p_2_s_1 + 360,
        ],
    )

    delta_H_p = 2 * np.sqrt(C_p_1_m_2) * np.sin(np.deg2rad(delta_h_p / 2))

    # Step 4. Calculate CIEDE2000 DE00:
    k_L = 2 if textiles else 1
    k_C = 1
    k_H = 1

    # S_L
    L_bar_p = (L_1 + L_2) / 2
    L_bar_p_cal = (L_bar_p - 50) ** 2
    S_L = 1 + ((0.015 * L_bar_p_cal) / np.sqrt(20 + L_bar_p_cal))

    # S_C
    C_bar_p = (C_p_1 + C_p_2) / 2
    S_C = 1 + 0.045 * C_bar_p

    # S_H
    a_h_p_1_s_2 = np.fabs(h_p_1 - h_p_2)
    h_p_1_a_2 = h_p_1 + h_p_2
    h_bar_p = np.select(
        [
            C_p_1_m_2 == 0,
            a_h_p_1_s_2 <= 180,
            np.logical_and(a_h_p_1_s_2 > 180, h_p_1_a_2 < 360),
            np.logical_and(a_h_p_1_s_2 > 180, h_p_1_a_2 >= 360),
        ],
        [
            h_p_1_a_2,
            h_p_1_a_2 / 2,
            (h_p_1_a_2 + 360) / 2,
            (h_p_1_a_2 - 360) / 2,
        ],
    )

    T = (
        1
        - 0.17 * np.cos(np.deg2rad(h_bar_p - 30))
        + 0.24 * np.cos(np.deg2rad(2 * h_bar_p))
        + 0.32 * np.cos(np.deg2rad(3 * h_bar_p + 6))
        - 0.20 * np.cos(np.deg2rad(4 * h_bar_p - 63))
    )
    S_H = 1 + 0.015 * C_bar_p * T

    # R_C
    C_bar_p_7 = C_bar_p**7
    R_C = 2 * np.sqrt(C_bar_p_7 / (C_bar_p_7 + 25**7))

    # R_T
    delta_theta = 30 * np.exp(-(((h_bar_p - 275) / 25) ** 2))
    R_T = -np.sin(np.deg2rad(2 * delta_theta)) * R_C

    dE = np.sqrt(
        (delta_L_p / k_L * S_L) ** 2
        + (delta_C_p / k_C * S_C) ** 2
        + (delta_H_p / (k_H * S_H)) ** 2
        + R_T * (delta_C_p / (k_C * S_C)) * (delta_H_p / (k_H * S_H))
    )

    return dE


def lab_to_lab(Lab, source_ill, target_ill):
    XYZ = colour.Lab_to_XYZ(Lab, colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"][source_ill])

    return colour.XYZ_to_Lab(XYZ, colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"][target_ill])


def Lab_to_RGB(Lab, input_ill, output_ill, rgb_colorspace):
    # TODO: Have to fix this function
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
