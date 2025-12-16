from catboost import CatBoostClassifier
import os
from utils import chronological_split

class Predictor():
    def __init__(self, df):
        self.df = df
        self.X_test = None
        self.y_test = None
        self.model = CatBoostClassifier().load_model(os.path.join("models","catboost_20251216.cbm"))

    def predict(self):
        if self.model is None:
            return - 1
        
        self.create_split()

        y_pred = self.model.predict(self.X_test)
        if y_pred is not None:
            return y_pred[y_pred.shape[0]-1]
        
        return -1
    
    def create_split(self):
        features = self.df.columns.drop(['Date', 'Price', 'Open', 'High', 'Low', 'Vol',  'day_lag',
       'Vol_Multiple','MACD', 'SMA_5', 'SMA_20', "Difference",
       'MACD_signal', 'MACD_diff', 'Price_lag1', 'ATR', 'Price_lag3', "Price_lag7", 'Target'])

        X_train, X_test, y_train, y_test = chronological_split(self.df,
                        features = features,
                        target = "Target")
        self.X_test = X_test
        self.y_test = y_test