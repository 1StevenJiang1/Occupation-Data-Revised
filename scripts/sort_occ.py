from typing import TextIO
from typing import List, Dict

import numpy as np
import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill
import os

cwd = os.getcwd()
data = os.path.join(cwd, "data")

if __name__ == "__main__":
    print(cwd)
    print(data)
