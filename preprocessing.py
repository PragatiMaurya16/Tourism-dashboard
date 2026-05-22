import pandas as pd

def load_data():

    df = pd.read_csv(
        "data/booking_reviews.csv"
    )

    df = df[
        [
            'hotel_name',
            'nationality',
            'rating',
            'review_text'
        ]
    ]

    df.dropna(
        inplace=True
    )

    df['review_length'] = (
        df['review_text']
        .apply(len)
    )

    return df


if __name__=="__main__":

    df = load_data()

    print(df.head())