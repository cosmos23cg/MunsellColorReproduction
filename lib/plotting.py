from lib import utilities

import numpy as np
import matplotlib.pyplot as plt


class Gamut:
    """
    1. plot single gamut (finished)
    2. plot multiple gamut via args (finished)
    3. choose the diagram (CIE xy, CIE 1976Lab, CIE 1976Luv)
    """
    def __init__(self, nrows=1, ncols=1, **kwarg):
        self.fig, self.axs = plt.subplots(nrows, ncols, **kwarg)  # Create a figure and axis
        self.points = []
        self.area = []
        self._basic_axis_setting()

    def _basic_axis_setting(self):
        self.axs.set_aspect(aspect='equal', adjustable='box')
        self.axs.grid(which='both', alpha=0.4)

        self.axs.set_xlabel("a*", labelpad=10)
        self.axs.set_ylabel("b*", labelpad=10)

        ## close frame line
        # self.axs.spines['top'].set_color('none')
        # self.axs.spines['right'].set_color('none')
        # self.axs.spines['bottom'].set_color('none')
        # self.axs.spines['left'].set_color('none')

        # x, y axis more thick
        self.axs.axhline(linewidth=0.7, color='black')
        self.axs.axvline(linewidth=0.7, color='black')

    def axis_setting(self, xlim=(-110, 110), ylim=(-90, 130)):
        self.axs.set_xlim(xlim[0], xlim[1])
        self.axs.set_ylim(ylim[0], ylim[1])

        self.axs.legend(ncols=2, loc='upper center', bbox_to_anchor=(0.5, 1.07))

        # handles, labels = self.axs.get_legend_handles_labels()
        # if handles and labels:
        #     new_labels = [f'{label}\u2003: {area[1]:>.1f}%' for label, area in zip(labels, self.area)]
        #     self.axs.legend(handles, new_labels, ncols=2, loc='upper center', bbox_to_anchor=(0.5, 1.1), title='Legend & Area ratio')




    def add_hue_annotate(self, ant_cor, ant_lst):
        for i in range(len(ant_lst)):
            x = ant_cor[i][0]
            y = ant_cor[i][1]
            annotate = ant_lst[i]

            if x > 0 and y > 0:
                xytext = (16, 5)  # Quadrant 1
            elif y > 0 > x:
                xytext = (-15, 15)  # Quadrant 2
            elif x < 0 and y < 0:
                xytext = (-13, -16)  # Quadrant 3
            else:
                xytext = (15, -15)  # Quadrant 4

            self.axs.annotate(f"{annotate}", (x, y), textcoords='offset points', xytext=xytext, ha='center')

    def add_points(self, points: list, c: str, ln: str, m: str, lb: str):
        """
        Parameters
        ----------
        points:
            points list(points, color, label)
        c:
            the color plotted in figure
        ln:
            line symbol
        m:
            marker symbol
        lb:
            label name
        """
        self.points.append((points, c, ln, m, lb))

    def gamut_area(self, *args: list):
        areas = []
        for arg in args:
            crt_area = 0
            for i in range(0, len(arg) - 1):
                a = arg[i]
                b = arg[i + 1]

                area = utilities.triangle_area(a, b, (0, 0))
                crt_area += area

            areas.append(crt_area)

        self.area = utilities.area_ratio(areas[0], areas)

    def plot_gamut(self):
        for points, color, line, marker, label in self.points:
            x = [x[0] for x in points]
            y = [x[1] for x in points]

            self.axs.plot(x, y, c=color, linestyle=line, label=label, marker=marker)

        self.axis_setting()

        return self.fig

    def plot_scatter(self, x, y, marker, c, edge_c, label):
        self.axs.scatter(x, y, s=20, marker=marker, c=c, edgecolor=edge_c, linewidths=1.0, label=label)


class Contour:
    def __init__(self, nrows=1, ncols=1, **kwargs):
        self.fig, self.axs = plt.subplots(nrows, ncols, **kwargs)
        self.points = []
        self.cont = None
        self.cbar = None

    def _axis_setting_contour(self, cont):
        # The z number show by legend
        self.fig.subplots_adjust(right=0.8)

        artists, labels = cont.legend_elements(str_format='{:.0f}'.format)
        artists = artists[::-1]
        labels = labels[::-1]
        labels = [x.replace('x = ', '') for x in labels]

        self.axs[1].legend(artists,
                           labels,
                           handleheight=2,
                           framealpha=1,
                           loc='center left',
                           bbox_to_anchor=(1.1, 0.5),
                           title='dE2000\n')

    def _axis_setting_contourf(self, cont, lv):
        if self.cbar is None:
            self.fig.subplots_adjust(right=0.8)

            cbar_ax = self.fig.add_axes([0.85, 0.11, 0.02, 0.78])  # setting color bar, (left, bottom, width, height)
            self.cbar = self.fig.colorbar(cont, cax=cbar_ax, format='%.0f', ticks=lv)  # .0f: rounding

    def _axis_setting(self, cont, lv, plotm, **kwargs):
        # Common settings

        # sub_figure settings
        for ax in self.axs.ravel():
            ax.set_aspect(aspect='equal', adjustable='box')
            ax.grid(True, alpha=0.1)

        # set x, y limit
        if 'xlim' in kwargs and 'ylim' in kwargs:
            for ax in self.axs.flat:
                ax.set_xlim(kwargs['xlim'])
                ax.set_ylim(kwargs['ylim'])

        # Custom settings
        if plotm == 'unfilled':
            self._axis_setting_contour(cont)

        if plotm == 'filled':
            self._axis_setting_contourf(cont, lv)

        # Set common x, y label
        self.fig.supxlabel("a*")
        self.fig.supylabel("b*")

        self.fig.supxlabel("a*", y=0.04)
        self.fig.supylabel("b*", x=0.04)

    def add_points(self, x, y, z, lv, cmap, title: str, ax_pos):
        self.points.append((x, y, z, lv, cmap, title, ax_pos))

    def plot_tricontour(self, addition_lv, **kwargs):
        for idx, (x, y, z, lv, cmap, title) in enumerate(self.points):
            # Plot the contour line
            cont = self.axs[idx].tricontour(x, y, z, lv, cmap=cmap)
            self.axs[idx].set_title(title)
            self._axis_setting(cont, lv, plotm="unfilled", **kwargs)

            # Plot the area border
            cs = self.axs[idx].tricontourf(x, y, z, addition_lv, colors='none')
            for c in cs.collections:
                c.set_edgecolor('black')
                c.set_linewidth(0.5)

        # self.fig.suptitle(main_title, y=0.961, ha='center', size=14, weight='bold')

        return self.fig

    def plot_tricontourf(self, **kwargs):
        for idx, (x, y, z, lv, cmap, title, ax_pos) in enumerate(self.points):
            cont = self.axs[ax_pos[0]][ax_pos[1]].tricontourf(x, y, z, lv, cmap=cmap)
            self.axs[ax_pos[0]][ax_pos[1]].set_title(title)
            self._axis_setting(cont, lv, plotm='filled', **kwargs)

        # self.fig.suptitle(main_title, y=0.961, ha='center', size=14, weight='bold')

        return self.fig


class MunsellHuePage:
    def __init__(self, nrows=1, ncols=1, **kwarg):
        self.fig, self.ax = plt.subplots(nrows, ncols, **kwarg)

    def _axis_setting(self, title=None):
        # axis x
        self.ax.set_xlim(0.5, 10.5)
        self.ax.set_xticks(list(range(1, 11, 1)))
        self.ax.set_xticklabels([f'/{x}' for x in range(2, 21, 2)])
        self.ax.set_xlabel('Chroma', labelpad=15)

        # axis y
        self.ax.set_ylim(0.5, 9.5)
        self.ax.set_yticks(list(range(1, 10, 1)))
        self.ax.set_yticklabels([f'{x}/' for x in range(1, 10, 1)])
        self.ax.set_ylabel('Value', labelpad=15)

        # other setting
        self.ax.tick_params(axis='both', labelsize=12, color="None")
        self.ax.spines.bottom.set_visible(False)
        self.ax.spines.left.set_visible(False)
        self.ax.spines.right.set_visible(False)
        self.ax.spines.top.set_visible(False)

        self.ax.set_title(title, loc='right', fontsize=28, fontweight='roman')
        self.ax.set_aspect(aspect='equal', adjustable='box')
        self.fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    @staticmethod
    def _get_ctext(de_value):
        if de_value > 2.0:
            return "#FD4141"
        elif 1.0 < de_value <= 2.0:
            return "#FFF347"
        else:
            return "#000000"

    def _text_de(self, x, y, de):
        for i in range(len(de)):
            ctext = self._get_ctext(de[i])
            self.ax.text(x[i], y[i], round(de[i], 1), c=ctext, ha='center', va='center_baseline', fontsize=10)

    @staticmethod
    def _get_cface(de_value):
        if de_value > 2.0:
            return "#000000"
        elif 1.0 < de_value <= 2.0:
            return "#5A5A5A"
        else:
            return "#E6E6E6"

    def _warn_circle_hint(self, x, y, de):
        for i in range(len(de)):
            cface = self._get_cface(de[i])
            # face_color = np.where(de > 2.0, '#C5C5C5', '#696969')
            self.ax.scatter(x[i], y[i], s=650, facecolors=cface, edgecolor='w', linewidth=0.9)

    def _legend_setting(self):
        legend_elements = [
            plt.scatter([], [], color='#000000', label=r'$\Delta E_{00}$ > 2', s=200),
            plt.scatter([], [], color='#5A5A5A', label=r'1 < $\Delta E_{00}$ <= 2', s=200),
            plt.scatter([], [], color='#E6E6E6', label=r'$\Delta E_{00}$ <= 1', s=200)
        ]
        # Customize the legend text colors
        legend = self.ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.9, 1), fontsize=12)
        for text, color in zip(legend.get_texts(), ['#FD4141', '#FFF347', '#000000']):
            text.set_color(color)

        frame = legend.get_frame()
        frame.set_facecolor('#787878')  # Light grey background


    def plot_munsell_hue_page(self, x, y, color, de=None, **kwargs):
        """
        **kwargs: title
        """
        title = kwargs.get('title', None)

        self.ax.scatter(x, y, c=color, marker='s', s=2000)
        self._axis_setting(title=title)

        if de is not None:
            self._text_de(x, y, de)
            self._warn_circle_hint(x, y, de)

            # legend setting
            self._legend_setting()

        return self.fig


class ScatterConfidenceArea:
    def __init__(self, nrows=1, ncols=1, plot_type='hue', **kwarg):
        self.fig, self.axs = plt.subplots(nrows, ncols, **kwarg)
        self.plot_type = plot_type

    def _axis_setting(self):
        self.axs.set_ylabel("$\Delta$E$_{00}$")
        # self.fig.subplots_adjust(left=0.1, right=0.88, top=0.9, bottom=0.08)

        self.axs.set_ylim(-0.1, 11.5)

        match self.plot_type:
            case 'hue':
                # self.axs.set_xlabel('Hab', labelpad=10)
                # self.axs.set_xlim(0, 365)
                # self.axs.set_xticks(range(0, 361, 30))
                self.axs.set_xlabel('Hue', labelpad=10)
                self.axs.set_xlim(0.5, 10.5)
                self.axs.set_xticks(range(1, 11, 1))
                self.axs.set_xticklabels(['R', 'YR', 'Y', "GY", 'G', 'BG', 'B', 'PB', 'P', 'RP'])

            case 'value':
                self.axs.set_xlabel('Value', labelpad=10)
                self.axs.set_xlim(0.5, 9.5)
                self.axs.set_xticks(range(1, 10, 1))
                self.axs.set_xticklabels(['1', '2', '3', "4", '5', '6', '7', '8', '9'])

            case 'chroma':
                self.axs.set_xlabel('Chroma', labelpad=10)
                self.axs.set_xlim(0.5, 10.5)
                self.axs.set_xticks(range(1, 11, 1))
                self.axs.set_xticklabels(['2', '4', '6', "8", '10', '12', '14', '16', '18', '20'])

    def plot_scatter(self, x, y, **kwargs):
        match self.plot_type:
            case 'hue':
                c = kwargs.get('c', None)
                label = kwargs.get('label', None)
                self.axs.scatter(x, y, c=c, marker='p', s=10, alpha=0.6, edgecolor=c, linewidths=0.8, label=label)

                if label is not None:
                    self.axs.legend(ncols=10, bbox_to_anchor=(0.5, 1.03), loc='center')
            case 'value':
                c = kwargs.get('c', None)
                alpha = kwargs.get('alpha', None)

                self.axs.scatter(x, y, c=c, marker='p', s=10, alpha=alpha, edgecolor='k', linewidths=0.5)
            case 'chroma':
                c = kwargs.get('c', None)

                self.axs.scatter(x, y, c=c, marker='p', s=10, edgecolor='k', linewidths=0.5, alpha=0.4)

        self._axis_setting()

        return self.fig

    def plot_confidence_area(self, mean, lower, upper):
        mean = np.asarray(mean, np.float32)
        lower = np.asarray(lower, np.float32)
        upper = np.asarray(upper, np.float32)

        self.axs.plot(mean[:, 0], mean[:, 1], 'dimgrey', label='Mean')
        self.axs.plot(lower[:, 0], lower[:, 1], linestyle='-', c='silver', label='Mean\n- 2 Std. Dev.')
        self.axs.plot(upper[:, 0], upper[:, 1], linestyle='-', c='silver', label='Mean\n+ 2 Std. Dev.')
        self.axs.fill_between(mean[:, 0], upper[:, 1], lower[:, 1], color="grey", alpha=0.1)

        return self.fig


class Box:
    def __init__(self, nrows=1, ncols=1, **kwarg):
        self.fig, self.ax = plt.subplots(nrows, ncols, **kwarg)

    @staticmethod
    def _box_setting(bplot, title):
        # R, YR, Y, GY, G, BG, B, PB, P, RP
        colors = ['red', 'red',
                  'orangered', 'orangered',
                  'yellow', 'yellow',
                  'yellowgreen', 'yellowgreen',
                  'green', 'green',
                  'cyan', 'cyan',
                  'blue', 'blue',
                  'blueviolet', 'blueviolet',
                  'purple', 'purple',
                  'deeppink', 'deeppink'
                  ]

        gray_scale = ['black', 'black',
                      'dimgray', 'dimgray',
                      'gray', 'gray',
                      'darkgray', 'darkgray',
                      'silver', 'silver',
                      'lightgray', 'lightgray',
                      'gainsboro', 'gainsboro',
                      'whitesmoke', 'whitesmoke',
                      'white', 'white']

        alpha = [1.0, 1.0,
                 0.9, 0.9,
                 0.8, 0.8,
                 0.7, 0.7,
                 0.6, 0.6,
                 0.5, 0.5,
                 0.4, 0.4,
                 0.3, 0.3,
                 0.2, 0.2,
                 0.1, 0.1]

        match title:
            case 'hue':
                for patch, color in zip(bplot['boxes'], colors):
                    patch.set_facecolor(color)

            case 'value':
                for patch, scale in zip(bplot['boxes'], gray_scale):
                    patch.set_facecolor(scale)

            case 'chroma':
                for patch, alpha in zip(bplot['boxes'], alpha):
                    patch.set_alpha(alpha)

    def _axes_setting(self, xlabel, ylabel):
        self.ax.grid(alpha=0.3)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

    def plot_box_whisker(self, data, labels, title, write_name):
        bplot = self.ax.boxplot(data, patch_artist=True)
        self.ax.set_xticks(range(1, len(labels) + 1))  # 設置刻度位置
        self.ax.set_xticklabels(labels)  # 設置標籤
        self.ax.set_title(title)
        self._box_setting(bplot, write_name)
        self._axes_setting(xlabel=write_name, ylabel='dE2000')

        return self.fig


def save_plt_figure(figure: plt.Figure, write_path, **kwargs):
    figure.savefig(write_path, **kwargs)
    print(f"Fig saved: {write_path}")
    plt.close()
