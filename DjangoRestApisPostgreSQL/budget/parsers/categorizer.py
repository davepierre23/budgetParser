import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

class Categorizer:
    def __init__(self, categories=None):
        self.categories = categories or {}
        self.model = None
        self.is_trained = False

    # Rule-based matching
    def categorize_rule_based(self, description: str) -> str:
        desc = description.lower()
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in desc:
                    return category
        return None

    # Train ML model
    def train_model(self, df: pd.DataFrame):
        self.model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        self.model.fit(df["Description"], df["Category"])
        self.is_trained = True

    # ML prediction
    def categorize_ml(self, description: str) -> str:
        if not self.is_trained:
            return "Unknown"
        return self.model.predict([description])[0]

    # Combined categorization
    def categorize(self, description: str) -> str:
        category = self.categorize_rule_based(description)
        if category:
            return category
        return self.categorize_ml(description)  # fallback
