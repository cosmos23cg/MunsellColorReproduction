import colour.difference
import numpy as np
import matplotlib.pyplot as plt


class MunsellScatter:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 9))
        self.marker_type = 's'
        self.s_size = 1600

    @staticmethod
    def _read_V_C_RGB(munsellObj):
        value_arr = np.array(munsellObj.HVC()[:, [1]]).astype('int')
        chroma_arr = np.array(munsellObj.HVC()[:, [2]]).astype('int')
        RGB_arr = np.array(munsellObj.RGB()).astype('float64') / 255
        return value_arr, chroma_arr, RGB_arr

    def _basixScatter(self, x, y, color):
        self.ax.scatter(
            x,
            y,
            s=self.s_size,
            c=color,
            marker=self.marker_type
        )

    def _scatter_axis(self, title=None) -> None:
        self.ax.set_xlim(0, 21)
        self.ax.set_ylim(0, 10)
        # ticks
        x_ticks = list(range(2, 21, 2))
        y_ticks = list(range(1, 10, 1))
        self.ax.set_xticks(x_ticks)
        self.ax.set_yticks(y_ticks)
        self.ax.tick_params(axis='both', pad=-18, labelsize=14, color="None")
        # label
        x_labels = [f'/{x}' for x in x_ticks]
        self.ax.set_xticklabels(x_labels)
        # title
        self.ax.set_title(title, fontsize=20)
        # spines
        self.ax.spines.bottom.set_visible(False)
        self.ax.spines.left.set_visible(False)
        self.ax.spines.right.set_visible(False)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    def scatter(self, munsellObj, title=None):
        value_arr, chroma_arr, RGB_arr = self._read_V_C_RGB(munsellObj)
        self._basixScatter(chroma_arr, value_arr, RGB_arr)
        self._scatter_axis(title)
        plt.show()
        return self.fig

    def scatterDe(self, com_munsellObj, ref_munsellObj, title=None):
        value_arr, chroma_arr, RGB_arr = self._read_V_C_RGB(com_munsellObj)
        de_arr = colour.difference.delta_E_CIE2000(com_munsellObj.Lab(), ref_munsellObj.Lab())
        face_color = np.where(de_arr > 2.0, '#C5C9C7', 'None')
        self._basixScatter(chroma_arr, value_arr, RGB_arr)
        self.ax.scatter(
            chroma_arr,
            value_arr,
            s=1050,
            facecolors=face_color,
            edgecolor='w'
        )
        for i in range(len(de_arr)):
            text_color = 'w' if value_arr[i] <= 4 else 'k'
            text_color = 'r' if de_arr[i] > 2.0 else text_color
            self.ax.text(
                chroma_arr[i],
                value_arr[i],
                round(de_arr[i], 1),
                c=text_color,
                ha='center',
                va='center_baseline',
                fontsize=13
            )
            self._scatter_axis(title)
        return self.fig


class CIE1931Diagram:
    def __init__(self):
        pass
