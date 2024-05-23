from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal
from .dataSaver import dataSaver

class AutoSaver(QObject):
    autoSaveEvent = pyqtSignal(str)

    def __init__(self, saveSteps = 10) -> None:
        super().__init__()
        self.counter = 0
        self.saveSteps = saveSteps
    
    def onData(self):
        self.counter += 1
        if self.counter >= self.saveSteps:
            self.autoSaveEvent.emit(f".backup.{self.counter}")
            self.counter = 0
