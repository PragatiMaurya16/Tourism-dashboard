import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Tourism Analytics Dashboard",
    layout="wide"
)

# Load data
df = pd.read_csv("data/booking_reviews.csv")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("Filters")

hotel_list = df["hotel_name"].unique()
selected_hotels = st.sidebar.multiselect(
    "Select Hotels",
    hotel_list,
    default=hotel_list[:5]
)

country_list = df["nationality"].unique()
selected_countries = st.sidebar.multiselect(
    "Select Nationality",
    country_list,
    default=country_list[:5]
)

filtered_df = df[
    (df["hotel_name"].isin(selected_hotels)) &
    (df["nationality"].isin(selected_countries))
]

# ---------------- TITLE ----------------
st.title("Tourism Experience Analytics Dashboard")
st.markdown("Analyze hotel reviews, ratings, and customer trends.")

# ---------------- KPI CARDS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Reviews", len(filtered_df))

with col2:
    st.metric("Avg Rating", round(filtered_df["rating"].mean(), 2))

with col3:
    st.metric("Hotels Analyzed", filtered_df["hotel_name"].nunique())

st.markdown("---")

# ---------------- TOP HOTELS ----------------
st.subheader("Top Hotels by Rating")

top_hotels = (
    filtered_df.groupby("hotel_name")["rating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_hotels)

# ---------------- NATIONALITY DISTRIBUTION ----------------
st.subheader("Customer Nationality Distribution")

country_counts = filtered_df["nationality"].value_counts().head(10)

st.bar_chart(country_counts)

# ---------------- HOTEL SELECTOR ----------------
st.subheader("Hotel Reviews Explorer")

selected_hotel = st.selectbox(
    "Choose a Hotel",
    filtered_df["hotel_name"].unique()
)

hotel_data = filtered_df[filtered_df["hotel_name"] == selected_hotel]

st.write("Sample Reviews")
st.dataframe(
    hotel_data[["rating", "review_text"]].head(10),
    use_container_width=True
)

# ---------------- PIE STYLE INSIGHT ----------------
st.subheader("Rating Distribution")

rating_counts = filtered_df["rating"].value_counts().sort_index()
st.bar_chart(rating_counts)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built using Streamlit | Tourism Analytics Project")