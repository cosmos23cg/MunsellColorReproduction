from pathlib import Path
import matplotlib.pyplot as plt
from lib import plotting, utilities


def group_data(data_lst, group_key):
    result_dict = {'header': data_lst[0]}

    for item in data_lst[1:]:
        k = item[group_key]
        if k not in result_dict:
            result_dict[k] = []

        result_dict[k].append(item)

    return result_dict


def max_Cab(data_lst: list):
    """
    Calculate the maximum CIE 1976 Cab for each group of data.

    Parameters
    ----------
    data_lst (list)
        List of data to be processed.
    Returns
    -------
        tuple: Two lists, one with HVC values and another with point coordinates.
    """
    grouped_data = group_data(data_lst, group_key=0)

    def process_values(values):
        # Calculate Cab for each value and append to the data
        for value in values:
            cab = utilities.cie_1976_cab(value[-2], value[-1])
            value.append(cab)
        # Find and return the entry with the maximum Cab
        return max(values, key=lambda x: x[-1])

    # Process each group except for the header
    result_lst = [process_values(values) for key, values in grouped_data.items() if key != 'header']

    # Extract HVC values and points
    hvc = [x[0:3] for x in result_lst]
    points = [[float(x) for x in entry[7:9]] for entry in result_lst]

    return hvc, points


def process_plot_gamut(file_path, gamut, c, ln, m, lb, marker, edge_c, hue_annotate=False):
    """
    Parameters
    ----------
    file_path
        Input data file path
    gamut
        Plotting instance
    c
        Color of the line and marker
    ln
        Line style
    m
        Line marker
    lb
        Label name
    marker
        Marker in the scatter
    edge_c
        Edge color of marker
    hue_annotate
        True/False, If True add the hue annotate
    """
    data = utilities.read_csv(file_path)
    hue_name, max_points = max_Cab(data)
    max_points.append(max_points[0])
    gamut.add_points(max_points, c=c, ln=ln, m=m, lb=lb)
    # ref_data has appended cab in the last. and the first row is header, so start in 1
    a, b = zip(*[(float(x[-3]), float(x[-2])) for x in data[1:]])

    gamut.plot_scatter(a, b, marker=marker, c=c, edge_c=edge_c)

    if hue_annotate is True:
        hue_name = [x[0] for x in hue_name]
        gamut.add_hue_annotate(max_points, hue_name)

    return max_points


def main(input_path, input_path2, write_path):
    gamut = plotting.Gamut(1, 1, figsize=(8, 8))

    ref_points = process_plot_gamut(input_path,
                                    gamut,
                                    c='royalblue',
                                    ln='-',
                                    m='^',
                                    lb='Ref',
                                    marker='^',
                                    edge_c='blue',
                                    hue_annotate=True)
    com_points = process_plot_gamut(input_path2,
                                    gamut,
                                    c='gold',
                                    ln='--',
                                    m='H',
                                    lb='Inkjet',
                                    marker='H',
                                    edge_c='goldenrod')

    gamut.gamut_area(ref_points, com_points)  # Show gamut area
    fig = gamut.plot_gamut()

    plotting.save_plt_figure(fig, write_path, dpi=1200)
    # plt.show()


if __name__ == '__main__':
    ref = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Dataset_BabelColour_HVC_RGB_Lab_D50\Dataset_BabelColour_HVC_RGB_Lab_D50_50_combine.csv"
    toner_4c = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C\4C_50_combined.csv"
    toner_4c_b = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-B_unfinished\4C-B_unfinished_50_combined.csv"
    toner_4c_g = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-G_unfinished\4C-G_unfinished_50_combined.csv"
    toner_4c_r = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\SunSui\SunSui_deReport_CSV\4C-R\4C-R_50_combined.csv"
    inkjet = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Deepblue\NTUST_50_20240315_rgb.csv"

    write_path = Path('output') / 'Printer Patch and Gamut Area (CIELAB)_Inkjet.png'
    main(ref, inkjet, write_path)
