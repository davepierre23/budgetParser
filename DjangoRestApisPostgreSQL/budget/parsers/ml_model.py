from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def train_model(df, desc_col, category_col):
    train_df = df[df[category_col] != "Unknown"]
    if train_df.empty:
        return None, None

    X, y = train_df[desc_col], train_df[category_col]
    vectorizer = TfidfVectorizer(stop_words="english")
    X_vec = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)
    print(f"✅ Training complete. Accuracy: {acc:.2%}")
    return model, vectorizer

def predict_unknowns(df, model, vectorizer, desc_col, category_col):
    mask = df[category_col] == "Unknown"
    if not mask.any():
        return df

    preds = model.predict(vectorizer.transform(df.loc[mask, desc_col]))
    df.loc[mask, category_col] = preds
    df.loc[mask, "CategorySource"] = "ML Model"
    return df
