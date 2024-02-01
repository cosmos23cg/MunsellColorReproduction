import math

import numpy as np
import matplotlib.pyplot as plt

class MunsellScatter:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 9))
        self.marker_type = 's'

    def _basic_scatter(self, x, y, color):
        self.ax.scatter(x, y, s=1500, c=color, marker=self.marker_type)

    def _scatter_axis(self, title):
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
        y_labels = [f'{y}/' for y in y_ticks]
        self.ax.set_xticklabels(x_labels)
        self.ax.set_yticklabels(y_labels)
        # title
        self.ax.set_title(title, fontsize=20)
        # spines
        self.ax.spines.bottom.set_visible(False)
        self.ax.spines.left.set_visible(False)
        self.ax.spines.right.set_visible(False)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    def scatter(self, val_chroma: list, rgb: list, title: str):
        """
        Plot the scatter, x-axis: chroma, y-axis: value

        Parameters
        ----------
        val_chroma:
            value and chroma list or array by each hue
        rgb:
            rgb list by each hue
        title:
            hue name
        """
        val_arr = np.array(val_chroma[:, 0])
        chroma_arr = np.array(val_chroma[:, 1])
        rgb_arr = np.array(rgb)

        self._basic_scatter(chroma_arr, val_arr, rgb_arr)
        self._scatter_axis(title)
        return self.fig

    def scatter_de(self, val_chroma: list, rgb: list, de, title):
        """
        Plot the scatter, x-axis: chroma, y-axis: value

        Parameters
        ----------
        val_chroma:
            value and chroma list or array by each hue
        rgb:
            rgb list by each hue
        de:
            color differance by each hue
        title:
            hue name
        """
        val_arr = np.array(val_chroma[:, 0])
        chroma_arr = np.array(val_chroma[:, 1])
        de_arr = np.array(de)
        face_color = np.where(de_arr > 0, '#C5C5C5', '#696969')

        self._basic_scatter(chroma_arr, val_arr, rgb)
        self.ax.scatter(
            chroma_arr,
            val_arr,
            s=900,
            facecolors=face_color,
            edgecolor='w'
        )

        for i in range(len(de_arr)):
            text_color = 'w'
            text_color = 'r' if de_arr[i] > 2.0 else text_color
            self.ax.text(
                chroma_arr[i],
                val_arr[i],
                round(de_arr[i], 1),
                c=text_color,
                ha='center',
                va='center_baseline',
                fontsize=13
            )
            self._scatter_axis(title)
        return self.fig


class ContourChart:
    def __init__(self):
        pass
        self.fig, self.ax = plt.subplots(figsize=(10, 9))

    def contourf(self, val_chroma, color_different, title):
        """
        Plot the contour fig

        Parameters
        ----------
        val_chroma:
            value and chroma list or array by each hue
        color_different:
            color different list by each hue
        title:
            hue name
        """
        val_arr = val_chroma[:, 0]
        chroma_arr = val_chroma[:, 1]
        dz = np.array(color_different)

        lv = np.linspace(np.min(dz), np.max(dz), 10)
        cont = self.ax.tricontourf(chroma_arr, val_arr, dz, levels=lv, cmap='Reds')

        self.ax.set_xlim(min(chroma_arr), max(chroma_arr))
        self.ax.set_ylim(min(val_arr), max(val_arr))
        self.fig.colorbar(cont, ax=self.ax)

        # Axis setting
        self.ax.set_title(title)
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')

        x_ticks = np.arange(2, 21, 2)
        self.ax.set_xticks(x_ticks)
        self.ax.set_xticklabels(f'/{x}' for x in x_ticks)
        y_ticks = np.arange(1, 10, 1)
        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels(f'{y}' for y in y_ticks)

        return self.fig


class Polar:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.hue_num = 40
        self.angle_step = 360 / self.hue_num

    def rotation(self, coordinate, degree):
        """
        caculate the new coordinate by angle
        """
        rad = math.radians(degree)
        rotaion_mat = np.array(
            [
                [math.cos(rad), -math.sin(rad)],
                [math.sin(rad), -math.cos(rad)]
            ]
        )
        rotate_cor = np.dot(rotaion_mat, coordinate)
        return rotate_cor.tolist()

    def polar(self, val_chroma):
        """

        Parameters
        ----------
        val_chroma:
            value and chroma list or array by each hue
        """
        # use data
        for i in range(self.hue_num):
            rotation_cor = self.rotation()



# TODO: class CIE1931Diagram
