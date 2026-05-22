import pandas as pd

df = pd.read_csv(
"data/booking_reviews.csv"
)

hotel_scores = (
df.groupby(
"hotel_name"
)["rating"]
.mean()
.sort_values(
ascending=False
)
)

def recommend():

    print(
    hotel_scores.head(5)
    )

recommend()