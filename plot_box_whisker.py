from pathlib import Path

from lib import plot, utilities


def process_data(data_lst, group_key):
    grouped_data: dict = utilities.group_by(data_lst, group_key)  # 1 hue, 2 value, 3 chroma

    all_data = []
    all_labels = []

    for key, values in grouped_data.items():
        printer_0 = [float(value[7]) for value in values]
        printer_1 = [float(value[11]) for value in values]

        all_data.extend([printer_0, printer_1])
        all_labels.extend([f'{key}\nToner\n4C', f'{key}\nInkjet'])

    return all_data, all_labels


def plot_box_whisker(data_path, group_key, write_name):
    data_lst = utilities.read_csv(data_path, skip_lines=2)

    all_data, all_label = process_data(data_lst, group_key)

    box = plot.Box(1, 1, figsize=(16, 9))
    fig = box.plot_box_whisker(all_data, all_label, 'Box and whisker', write_name)

    write_path = Path('output') / f'box_whisker-{write_name}.png'
    plot.save_plt_figure(fig, write_path, dpi=1200)


if __name__ == '__main__':
    # Plot contour or box whisker
    p = r"C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Analysis\ref_com_de_only.csv"
    plot_box_whisker(p, 3, 'chroma')
