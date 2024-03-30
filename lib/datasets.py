
illuminant_dict = {
    "CIE 1931": {
        "A": (0.44757, 0.40745),
        "B": (0.34842, 0.35161),
        "C": (0.31006, 0.31616),
        "D50": (0.34567, 0.3585),
        "D55": (0.33242, 0.34743),
        "D65": (0.31271, 0.32902),
        "D75": (0.29902, 0.31485),
        "D93": (0.28315, 0.29711),
        "E": (1/3, 1/3),
        "F1": (0.3131, 0.33727),
        "F2": (0.37208, 0.37529),
        "F3": (0.4091, 0.3943),
        "F4": (0.44018, 0.40329),
        "F5": (0.31379, 0.34531),
        "F6": (0.3779, 0.38835),
        "F7": (0.31292, 0.32933),
        "F8": (0.34588, 0.35875),
        "F9": (0.37417, 0.37281),
        "F10": (0.34609, 0.35986),
        "F11": (0.38052, 0.37713),
        "F12": (0.43695, 0.40441),
        "LED-B1": (0.456, 0.4078),
        "LED-B2": (0.4357, 0.4012),
        "LED-B3": (0.3756, 0.3723),
        "LED-B4": (0.3422, 0.3502),
        "LED-B5": (0.3118, 0.3236),
        "LED-BH1": (0.4474,	0.4066),
        "LED-RGB": (0.4557, 0.4211),
        "LED-V1": (0.456, 0.4548),
        "LED-v2": (0.3781, 0.3775)
    },
    "CIE 1964": {
        "A": (0.45117, 0.40594),
        "B": (0.3498, 0.3527),
        "C": (0.31039, 0.31905),
        "D50": (0.34773, 0.35952),
        "D55": (0.33411, 0.34877),
        "D65": (0.31382, 0.331),
        "D75": (0.29968, 0.3174),
        "D93": (0.28327, 0.30043),
        "E": (1/3, 1/3),
        "F1": (0.31811, 0.33559),
        "F2": (0.37925, 0.36733),
        "F3": (0.41761, 0.38324),
        "F4": (0.4492, 0.39074),
        "F5": (0.31975, 0.34246),
        "F6": (0.3866, 0.37847),
        "F7": (0.31569, 0.3296),
        "F8": (0.34902, 0.35939),
        "F9": (0.37829, 0.37045),
        "F10": (0.3509, 0.35444),
        "F11": (0.38541, 0.37123),
        "F12": (0.44256, 0.39717)
    }
}

# The centers of each hue ranges are labeled 5R, 5YR, 5Y, 5GY, 5G, 5BG, 5B, 5PB, 5P, 5RP
munsell_hue_rotation = [
    '10RP', '2.5R', '5R', '7.5R', '10R', '2.5YR', '5YR', '7.5YR', '10YR', '2.5Y', '5Y', '7.5Y', '10Y', '2.5GY',
    '5GY', '7.5GY', '10GY', '2.5G', '5G', '7.5G', '10G', '2.5BG', '5BG', '7.5BG', '10BG', '2.5B', '5B', '7.5B',
    '10B', '2.5PB', '5PB', '7.5PB', '10PB', '2.5P', '5P', '7.5P', '10P', '2.5RP', '5RP', '7.5RP'
]

munsell_hue_order_dict = {'R': 0, 'YR': 1, 'Y': 2, 'GY': 3, 'G': 4, 'BG': 5, 'B': 6, 'PB': 7, 'P': 8, 'RP': 9}