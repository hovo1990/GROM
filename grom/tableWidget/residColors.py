AMINOACID_COLORS = {'ALA': [200, 200, 200],
                    'ARG': [20, 90, 255],
                    'ASN': [0, 220, 220],
                    'ASP': [230, 10, 10],
                    'CYS': [230, 230, 0],
                    'GLN': [0, 220, 220],
                    'GLU': [230, 10, 10],
                    'GLY': [235, 235, 235],
                    'HIS': [130, 130, 210],
                    'ILE': [15, 130, 15],
                    'LEU': [15, 130, 15],
                    'LYS': [20, 90, 255],
                    'MET': [230, 230, 0],
                    'PHE': [50, 50, 170],
                    'PRO': [220, 150, 130],
                    'SER': [250, 150, 0],
                    'THR': [250, 150, 0],
                    'TRP': [180, 90, 180],
                    'TYR': [50, 50, 170],
                    'VAL': [15, 130, 15],
                    'ASX': [255, 105, 180],
                    'GLX': [255, 105, 180],
                    'other': [190, 160, 110]}

NUCLEOTIDES = {"DA": [160, 160, 255],
               "DT": [160, 255, 160],
               "DG": [255, 112, 112],
               "DC": [255, 140, 75]}

#: Idea need to make a separator in List

comboBoxList = list(AMINOACID_COLORS.keys()) + list(NUCLEOTIDES.keys())
# print(comboBoxList)


RESID_COLORS_RGB = dict(list(AMINOACID_COLORS.items()) + list(NUCLEOTIDES.items()))
# print(RESID_COLORS)
