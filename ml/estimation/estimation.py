
from seaborn import heatmap
from sklearn.metrics import confusion_matrix


class Estimation:
    def __init__(self, y_true, y_pred, labels=None):
        self.y_true = y_true
        self.y_pred = y_pred
        self.labels = labels

    def confusion_matrix(self):
        return confusion_matrix(self.y_true, self.y_pred, labels=self.labels)


