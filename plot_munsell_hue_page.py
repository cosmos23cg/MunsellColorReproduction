import colour.difference
from pathlib import Path

from lib import utilities, plot


def norm(data: list):
    result = []
    for sub_data in data:
        if isinstance(sub_data, list):
            sub_lst = [x / 255.0 for x in sub_data]
            result.append(sub_lst)

    return result


def plot_munsell_scatter(ref_path, com_path, write_dir):
    ref_data = utilities.read_csv(ref_path)
    ref_munsell_data = utilities.MunsellColor(ref_data)

    com_data = utilities.read_csv(com_path)
    com_munsell_data = utilities.MunsellColor(com_data)

    for idx, key in enumerate(ref_munsell_data.vc().keys()):
        v = [x[0] for x in ref_munsell_data.vc()[key]]
        c = [x[1] / 2 for x in ref_munsell_data.vc()[key]]
        ref_rgb = norm(ref_munsell_data.rgb()[key])

        de2000 = colour.difference.delta_E_CIE2000(ref_munsell_data.lab()[key], com_munsell_data.lab()[key])

        musell_hue_page = plot.MunsellHuePage(1, 1, figsize=(10, 8))
        fig = musell_hue_page.plot_munsell_hue_page(x=c, y=v, color=ref_rgb, title=key, de=de2000)

        write_path = write_dir.parent.joinpath(write_dir.name + f"_{key}.png")
        plot.save_plt_figure(fig, write_path, dpi=1200)


if __name__ == '__main__':
    fol = Path(r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction")
    ref_path = fol / r"Dataset_BabelColour_HVC_RGB_Lab_D50\Dataset_BabelColour_HVC_RGB_Lab_D50_50_combine.csv"
    # com_path = fol / r"SunSui\SunSui_deReport_CSV\4C\4C_50_combine.csv"
    com_path = fol / r"Deepblue\NTUST_50_20240315.csv"

    write_dir = Path('output') / 'inkjet_4c'
    plot_munsell_scatter(ref_path, com_path, write_dir)
