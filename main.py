import streamlit as st

home_page = st.Page(
    "home.py",
    title="Catalogue",
    default=True,
)
pickup_page = st.Page(
    "pickup.py",
    title="Pickups",
)
pg = st.navigation([home_page, pickup_page])
pg.run()
