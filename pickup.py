import streamlit as st
import requests
import pandas as pd
from typing import List, Optional


# ! === LOADING DATA FROM API ===
@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Fetch product data from the Fake Store API and process ratings.

    Returns:
        DataFrame containing product data including additional columns (rate and count).
    """
    url = "https://fakestoreapi.com/products/"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df["rate"] = df["rating"].apply(lambda x: x["rate"])
    df["count"] = df["rating"].apply(lambda x: x["count"])
    return df


# ! === STREAMLIT CONFIG ===
st.title("🛍 Our Pickups")
st.write('Select your preferences, and we will automatically pick up items for you !')


# ! === SIDEBAR ===
df = load_data()
# Filter options
category_options = sorted(df["category"].unique())
category_preference = st.sidebar.multiselect(
    "Preferred Category:", category_options, default=category_options
)

budget = st.sidebar.number_input(
    "Budget (£)",
    min_value=0.0,
)


# ! === RECOMMEND FUNCTION ===
def recommend_products(
    df: pd.DataFrame,
    category_preference: List[str],
    budget: Optional[float] = None,
) -> pd.DataFrame:
    """
    Recommend top 3 products based on user preferences, considering category and budget.

    Args:
        df: The full product catalogue.
        category_preference: List of preferred product categories.
        budget: Maximum price to consider. Defaults to None.

    Returns:
        DataFrame with top 3 recommended products.
    """
    filtered_df = df[df["category"].isin(category_preference)].copy()

    if filtered_df.empty:
        return filtered_df  # Return empty if no data matching preferences

    max_reviews = filtered_df["count"].max()
    price_min = filtered_df["price"].min()
    price_max = filtered_df["price"].max()
    price_mid = (price_min + price_max) / 2

    # If budget is specified, filter to products within budget
    if budget is not None and budget > 0:
        filtered_df = filtered_df[filtered_df["price"] <= budget]
        if filtered_df.empty:
            return filtered_df

    def score(row):
        rating_score = row["rate"] / 5.0
        # Safety management for division by zero if price_max == price_min
        if price_max == price_min:
            price_score = 1.0
        else:
            price_score = 1 - (abs(row["price"] - price_mid) / (price_max - price_min))
            price_score = max(price_score, 0)  # Clamp to non-negative

        review_score = row["count"] / max_reviews if max_reviews > 0 else 0

        # Weighted composite score - adjust weights as desired
        return rating_score * 0.5 + price_score * 0.3 + review_score * 0.2

    filtered_df["score"] = filtered_df.apply(score, axis=1)
    recommended = filtered_df.sort_values(by="score", ascending=False).head(3)
    return recommended


# ! === MAIN WINDOW ===
# Display 3 recommendations
recommended_products = recommend_products(df, category_preference, budget)

cols = st.columns(3)
for col, product in zip(cols, recommended_products.itertuples()):
    with col:
        if isinstance(product.image, str):
            st.image(product.image, width=100)
        else:
            st.warning("Invalid image format for product.")
        st.markdown(f"### {product.title}")
        st.markdown(
            f"""
            **Price:** £{product.price:.2f}  
            **Category:** {product.category}  
            **Rating:** {product.rate} ({product.count} reviews)  
            """
        )
        with st.expander("Read Description"):
            st.write(product.description)
st.markdown("---")
