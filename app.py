import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("customer_360_sample.csv")

# Sidebar filters
st.sidebar.header("Filter Customers")
age_range = st.sidebar.slider("Age Range", int(df["Age"].min()), int(df["Age"].max()), (25, 45))
locations = st.sidebar.multiselect("Location", options=df["Location"].unique(), default=df["Location"].unique())
segments = st.sidebar.multiselect("Segment", options=df["Segment"].unique(), default=df["Segment"].unique())

# Apply filters
filtered_df = df[
    (df["Age"] >= age_range[0]) & 
    (df["Age"] <= age_range[1]) & 
    (df["Location"].isin(locations)) & 
    (df["Segment"].isin(segments))
]

st.title("Customer 360 Dashboard")

# 1. Customer Profile Panel
st.header("Customer Profile Panel")
st.dataframe(filtered_df[["Customer ID", "Name", "Age", "Location", "Segment", "Product Holdings"]])

# 2. Heatmap of Customer Activity
st.header("Heatmap of Customer Activity")
heatmap_data = filtered_df.groupby(["Location", "Segment"])["Activity Score"].mean().unstack()
fig, ax = plt.subplots()
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", ax=ax)
st.pyplot(fig)

# 3. Product Holdings Overview
st.header("Product Holdings Overview")
product_counts = filtered_df["Product Holdings"].str.split(", ").explode().value_counts()
fig2, ax2 = plt.subplots()
product_counts.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Number of Customers")
ax2.set_title("Distribution of Product Holdings")
st.pyplot(fig2)

# 4. Transaction Trends
st.header("Transaction Trends")
trend_option = st.selectbox("Group Transaction Trends By", ["Age", "Segment"])
trend_data = filtered_df.groupby(trend_option)["Monthly Transactions"].mean()
fig3, ax3 = plt.subplots()
trend_data.plot(kind="line", marker="o", ax=ax3)
ax3.set_ylabel("Avg Monthly Transactions")
ax3.set_title(f"Transaction Trends by {trend_option}")
st.pyplot(fig3)
