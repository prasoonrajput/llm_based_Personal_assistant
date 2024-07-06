import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

class Evaluator:
    def __init__(self):
        self.results = []

    def evaluate(self, user_input, assistant_output, expected_output, user_rating=None):
        result = {
            "user_input": user_input,
            "assistant_output": assistant_output,
            "expected_output": expected_output,
            "correct": expected_output in assistant_output,
            "user_rating": user_rating
        }
        self.results.append(result)

    def get_metrics(self):
        df = pd.DataFrame(self.results)
        accuracy = accuracy_score(df["correct"], [True] * len(df))
        precision, recall, f1, _ = precision_recall_fscore_support(df["correct"], [True] * len(df), average='binary')
        avg_user_rating = df["user_rating"].mean() if "user_rating" in df else None
        
        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "avg_user_rating": avg_user_rating
        }