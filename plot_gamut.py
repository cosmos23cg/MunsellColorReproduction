from pathlib import Path

from lib import plot, utilities


def max_Cab(data_lst: list, col):
    grouped_data: dict = utilities.group_by(data_lst, group_key=1)  # 1 is hue in Excel file

    result_lst = []
    for key, value in grouped_data.items():
        for i in range(len(value)):
            # slice the list
            value[i] = [value[i][j] for j in [0, 1, 2, 3, col[0], col[1]]]

            # calculate the Cab then append in lst
            cab = utilities.cie_1976_cab(value[i][-2], value[i][-1])
            grouped_data[key][i].append(cab)

        max_lst = max(grouped_data[key], key=lambda x: x[-1])
        max_lst = utilities.check_float(max_lst)
        result_lst.append(max_lst)

    hvc = [x[1:4] for x in result_lst]
    points = [x[4:6] for x in result_lst]

    return hvc, points


def plot_gamut(input_path):
    data_lst = utilities.read_csv(input_path, skip_lines=2)

    ref_hue, ref_points = max_Cab(data_lst, (5, 6))
    _, toner_4c_points = max_Cab(data_lst, (8, 9))
    _, injeck_points = max_Cab(data_lst, (20, 21))

    # Make the data can plot a circle
    ref_points.append(ref_points[0])
    toner_4c_points.append(toner_4c_points[0])
    injeck_points.append(injeck_points[0])

    gamut = plot.Gamut(1, 1, figsize=(8, 6))
    gamut.add_points(ref_points, c='k', ln='-', m='o', lb="Ref")
    gamut.add_points(toner_4c_points, c='y', ln='--', m='^', lb="4C")
    gamut.add_points(injeck_points, c='m', ln='--', m='^', lb="Inkjet")

    gamut.gamut_area(ref_points, toner_4c_points, injeck_points)
    gamut.add_annotate(ref_points, ref_hue)
    fig = gamut.plot_gamut()
    write_path = Path('output') / 'gamut and ratio.png'
    plot.save_plt_figure(fig, write_path, dpi=1200)


if __name__ == '__main__':
    p = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Analysis\Summary_lab.csv"
    plot_gamut(p)
