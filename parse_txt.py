import csv
import os
import glob
from pathlib import Path


class ParseText:
    def __init__(self, path):
        self.p = Path(path)
        self.fields = ["H", "V", "C", "R", "G", "B", "L*", "a*", "b*"]

    def _sub_files(self):
        def sort_key(file_path):
            file_name = file_path.stem
            parts = file_name.split('_')
            return int(parts[1]), int(parts[2].split('.')[0])

        if not self.p.exists():
            raise FileNotFoundError(f'Folder {self.p} not found.')

        if self.p.is_dir():
            txt_files = list(self.p.glob('**/*' + '.txt'))
            sorted_files = sorted(txt_files, key=lambda x: sort_key(x))
            return sorted_files
        elif self.p.is_file():
            return [self.p]
        else:
            raise FileNotFoundError(f'Folder {self.p} not found.')

    def parseFile(self):
        my_ls = []
        for i in self._sub_files():
            with open(i, 'r') as file:
                lines = file.readlines()
                spec_line = int
                for idx, line in enumerate(lines):
                    if "Munsell to RGB and L*a*b" in line:
                        spec_line = idx

                hvc = lines[spec_line + 1].strip('\n').split('\t')
                rgb = lines[spec_line + 2].strip('\n').split('\t')
                lab = lines[spec_line + 3].strip('\n').split('\t')
                hvc = hvc[1:]
                rgb = rgb[1:]
                lab = lab[1:]
                result = hvc + rgb + lab
                my_ls.append(result)
        return my_ls

    def writeCSV(self, filename, input):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.fields)
            writer.writerows(input)


def main(input_path):
    input_p = Path(input_path)
    for child in input_p.iterdir():
        if not child.is_file():
            for grand_child in child.iterdir():
                name_parts = grand_child.parts
                file_name = str(name_parts[-2] + name_parts[-1])
                parse = ParseText(grand_child)
                data = parse.parseFile()
                parse.writeCSV('output/' + file_name + '.csv', data)


if __name__ == "__main__":
    p = r'C:\Users\cghsi\OneDrive\NTUST_CIT\Experiments\Munsell_Reproduction\Dataset_BabelColour_HVC_RGB_Lab_D50\Conversion_txt'
    main(p)
