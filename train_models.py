import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv("data/booking_reviews.csv")

df = df.dropna(subset=["review_text","rating"])

df["sentiment"] = df["rating"].apply(
    lambda x: 1 if x >= 4 else 0
)

X = df["review_text"]
y = df["sentiment"]

X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = Pipeline([
    ("tfidf",TfidfVectorizer()),
    ("clf",LogisticRegression())
])

model.fit(X_train,y_train)

pred = model.predict(X_test)

print(
    "Accuracy:",
    accuracy_score(y_test,pred)
)

joblib.dump(
    model,
    "models/sentiment_model.pkl"
)

print("Model Saved")