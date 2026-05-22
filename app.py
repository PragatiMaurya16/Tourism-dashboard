import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Tourism Analytics Dashboard",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(os.path.join("data", "booking_reviews.csv"))

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
st.markdown("Interactive insights from hotel reviews dataset")

st.markdown("---")

# ---------------- KPI CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Reviews", len(filtered_df))
col2.metric("Avg Rating", round(filtered_df["rating"].mean(), 2))
col3.metric("Hotels", filtered_df["hotel_name"].nunique())
col4.metric("Countries", filtered_df["nationality"].nunique())

st.markdown("---")

# ---------------- TOP HOTELS (PLOTLY) ----------------
st.subheader("Top Hotels by Average Rating")

top_hotels = (
    filtered_df.groupby("hotel_name")["rating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig1 = px.bar(
    top_hotels,
    x="rating",
    y="hotel_name",
    orientation="h",
    color="rating",
    title="Top Rated Hotels"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- NATIONALITY DISTRIBUTION ----------------
st.subheader("Customer Nationality Distribution")

country_counts = (
    filtered_df["nationality"]
    .value_counts()
    .head(10)
    .reset_index()
)

country_counts.columns = ["nationality", "count"]

fig2 = px.pie(
    country_counts,
    names="nationality",
    values="count",
    title="Top Customer Nationalities"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- HOTEL REVIEWS ----------------
st.subheader("Hotel Review Explorer")

selected_hotel = st.selectbox(
    "Choose Hotel",
    filtered_df["hotel_name"].unique()
)

hotel_data = filtered_df[filtered_df["hotel_name"] == selected_hotel]

st.dataframe(
    hotel_data[["rating", "review_text"]].head(10),
    use_container_width=True
)

# ---------------- RATING DISTRIBUTION ----------------
st.subheader("Rating Distribution")

rating_counts = (
    filtered_df["rating"]
    .value_counts()
    .sort_index()
    .reset_index()
)

rating_counts.columns = ["rating", "count"]

fig3 = px.bar(
    rating_counts,
    x="rating",
    y="count",
    title="Rating Distribution",
    color="count"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built with Streamlit + Plotly | Tourism Analytics Dashboard")
