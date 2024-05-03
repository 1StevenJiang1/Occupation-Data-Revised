from typing import TextIO
from typing import List, Dict

import numpy as np
import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill
import os

cwd = os.getcwd()
data = os.path.join(cwd, "data")


def check_invalid(target, invalid_input):
    if target == invalid_input:
        return True
    return False


if __name__ == "__main__":
    data = os.path.join(data, "File_3.dta")
    df = pd.read_stata(data)
    df = df[df["occ"] != 0]
    df = df[df["sex"] != 0]
    contains_zero = df['occ'].apply(check_invalid, args=(0,))
    contains_zero = df['sex'].apply(check_invalid, args=(0,))

    print("Contains 0:", contains_zero.any())
    print(df)

    df.info(show_counts=True)
