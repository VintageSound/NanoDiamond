from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal
import numpy as np
import pandas as pd

class MeasurementProcessor(QObject):
    photonsAVGRecivedEvent = pyqtSignal(float)

    def __init__(self) -> None:
        super().__init__()
        self.photonsAVGHistory = pd.DataFrame([], columns=["photonsAVG"])

    def reciveODMRDataHandler(self, data, count):
        y_label = data.columns[1]
        photonsAVG = np.average(data[y_label])
        self.photonsAVGHistory = self.photonsAVGHistory.append({ "photonsAVG": photonsAVG }, ignore_index=True)
        self.photonsAVGRecivedEvent.emit(photonsAVG)
        return photonsAVG