import os
import pandas as pd


class InputTable:
    def __init__(self, path: str):
        self.path = path
        self.df = pd.read_csv(self.path)
        self.name = os.path.basename(path).lower()
