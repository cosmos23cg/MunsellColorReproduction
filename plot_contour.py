from pathlib import Path
import numpy as np

from lib import plot, utilities


def plot_contour(ipt_path, contour_type, split_num=11):
    data_lst = utilities.read_csv(ipt_path, 2)

    value_col = 2  # 1 hue, 2 value, 3 chroma
    grouped_data: dict = utilities.group_by(data_lst, value_col)

    # Fetch all De and find the min max value for the colorbar range
    de_col = [7, 11]  # Toner_printer_4C, Inkjet_printer
    z_all = []

    for key, value in grouped_data.items():
        if utilities.is_nested(value) is True:
            for sub_value in value:
                z_all.extend(float(sub_value[i]) for i in de_col)
        else:
            z_all.extend([float(value[i]) for i in de_col])

    z_min, z_max = min(z_all), max(z_all)
    lv = np.linspace(z_min, z_max, split_num)

    # Split the input data into two figures
    for i, (key, data) in enumerate(grouped_data.items()):
        x, y, z1, z2 = [], [], [], []  # a*, b*, de2000_1, de2000_2

        for value in data:
            x.append(float(value[5]))
            y.append(float(value[6]))
            z1.append(float(value[7]))
            z2.append(float(value[11]))

        contour = plot.Contour(1, 2, figsize=(13, 6), sharex=True, sharey=True)
        contour.add_points(x, y, z1, lv, cmap='coolwarm', title='Toner')
        contour.add_points(x, y, z2, lv, cmap='coolwarm', title='Inkjet')

        title = f"Value {i+1}"

        match contour_type:
            case "tricontourf":
                fig = contour.plot_tricontourf(title, xlim=(-90, 90), ylim=(-80, 120))
                save_path = Path('output') / f"Toner_4C_Inkjet_contourf-Value_{i + 1}.png"
                # plot.save_plt_figure(fig, save_path, dpi=1200)

            case "tricontour":
                fig = contour.plot_tricontour(title, xlim=(-90, 90), ylim=(-80, 120))
                save_path = Path('output') / f"Toner_4C_Inkjet_contour-Value_{i + 1}.png"
                # plot.save_plt_figure(fig, save_path, dpi=1200)

            # case "contour":
            #     fig = contour.plot_contour(title, xlim=(-90, 90), ylim=(-80, 120))


if __name__ == '__main__':
    p = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Analysis\ref_com_de_only.csv"
    plot_contour(p, "contour")
