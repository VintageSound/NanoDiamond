
import numpy as np
import pandas as pd
import os

class dataSaver():
    def __init__(self) -> None:
        pass

    def save(self, filePath, metadata, data : pd.DataFrame):
        print(filePath)
        directory = os.path.dirname(filePath)
        os.makedirs(directory, exist_ok=True)
        pdMetadata = pd.Series(metadata)

        with open(filePath, 'w') as fout:
            pdMetadata.to_csv(fout)
            data.to_csv(fout)