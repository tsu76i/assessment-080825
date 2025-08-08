import streamlit as st
import requests
import pandas as pd
from typing import List, Generator


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
st.title("🛍 Simple Product Catalogue Viewer")


# ! === UTILITY FUNCTION ===
def chunk_list(lst: List, n: int) -> Generator[List, None, None]:
    """
    Split a list into consecutive chunks of size n.

    Args:
        lst: The list to be split.
        n: The chunk size.

    Yields:
        Subsequent chunks of the original list.
    """
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


# ! === SIDEBAR ===
df = load_data()
category_options = sorted(df["category"].unique())
selected_category = st.sidebar.multiselect(
    "Filter by Category:", category_options, default=category_options
)

min_price, max_price = float(df["price"].min()), float(df["price"].max())
price_range = st.sidebar.slider(
    "Select Price Range (£):",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
)
min_rating = st.sidebar.number_input(
    "Select Minimum Rating (1.0 - 5.0):",
    format="%.1f",
    step=0.1,
    min_value=1.0,
    max_value=5.0,
)
# Filtering logic
filtered = df[
    (df["rate"] >= min_rating)
    & (df["category"].isin(selected_category))
    & (df["price"] >= price_range[0])
    & (df["price"] <= price_range[1])
]

# ! === MAIN WINDOW ===
st.write(f"Showing {len(filtered)} products")

# Display products 3 per row with columns
for chunk in chunk_list(list(filtered.itertuples()), 3):
    cols = st.columns(3)
    for col, product in zip(cols, chunk):
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
