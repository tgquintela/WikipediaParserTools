

import pandas as pd
from os.path import join


def parse_excel_sheet(f, n=0):
    """Parse a sheet of a xlsx file."""
    xl_file = pd.ExcelFile(f)
    dfs = xl_file.parse(xl_file.sheet_names[n])
    return dfs


def write_dataframe_to_excel(d, name, path=''):
    """Function to write in csv the dataframes."""
    name = name if len(name.split()) == 1 else name
    filepath = join(path, name)
    d.to_excel(filepath)
