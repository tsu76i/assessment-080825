# 📊 AI Engineer Assessment (08/08/2025)


## ⚙️ Installation
```
git clone https://github.com/tsu76i/assessment-080825.git
cd assessment-080825
pip install -r requirements.txt
```

## 🚀 Usage

To run the app locally:
```
streamlit run main.py
```



## 📜 Pages

- Home page: Interactive product viewer with basic filters.
- Pickup page: Recommendation viewer based on user preferences.

## ✨ Selected AI Feature
Option C - **Recommendation System**. 

On the `Pickup` page, users can specify their preferences (product categories and a budget). The system then generates a list of recommended articles based on a rule-based recommendation algorithm that assigns different weights to parameters such as product rating, price proximity to the average price, and the number of reviews. The algorithm follows these steps:

1. Load the entire data.
1. Filter by preferred categories.
1. Extract price midpoint  `(min price + max price) / 2`.
1. Calculate score for each product.
    - price score = $\text{max}\left(0, 1 - \dfrac{|\text{price}_{\text{product}} - \text{price}_{\text{midpoint}}|}{\text{price}_{\text{max}} - \text{price}_{\text{min}}}\right)$ (Inverse normalised deviation measure that provides closer prices with higher scores)
    - rating score = $\dfrac{\text{product's score}}{5} $ (Normalised)
    - review score = $\dfrac{\text{product's review counts}}{\text{max review counts}}$
1. Combine the scores with assigned weights (rating: 50%, price: 30%, reviews: 20%):
    $$
    \text{score}_{\text{product}} = 0.5 \times \text{rating score} + 0.3 \times \text{price score} + 0.2 \times \text{review score}
    $$
1. Sort the filtered products in descending order of scores, then return 3 top products as recommendations.


## 💰 Application in Blockchain
In the context of blockchain technology, rule-based recommender systems can be encoded within smart contracts. This approach ensures that the process remains transparent and immutable, and, due to the reliance on lightweight arithmetic operations, it operates effectively within the computational limits of on-chain execution.

## 🛠️ Tools and Libraries Used
- Visual Studio Code
- Python (3.13.3)
- Numpy
- Pandas
- Streamlit

