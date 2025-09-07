import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

class Categorizer:
    def __init__(self, categories):
        self.categories = categories

    def categorize_with_source(self, description: str):
        desc = description.upper()
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.upper() in desc:
                    return category, f"Rule: '{keyword}'"
        return "Unknown", "Rule: None"

    def apply(self, df, description_col, category_col="Category"):
        results = df[description_col].apply(self.categorize_with_source)
        df[[category_col, "CategorySource"]] = pd.DataFrame(results.tolist(), index=df.index)
        return df
