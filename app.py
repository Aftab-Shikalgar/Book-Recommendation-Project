# App

import streamlit as st
import pickle
from collections import defaultdict


# ------------------------------
# Load predictions from pickle
# ------------------------------


with open("matrix_and_df.pkl", "rb") as f:
    loaded = pickle.load(f)

user_item_df = loaded["user_item_df"]
books_df = loaded["books_df"]
best_model = loaded["model"]

final_predictions = []

all_users = user_item_df['User-ID'].unique()
all_books = user_item_df['ISBN'].unique()

for user_id in all_users:
    user_rated_books = set(user_item_df[user_item_df['User-ID'] == user_id]['ISBN'])
    for item_id in all_books:
        if item_id not in user_rated_books:
            pred = best_model.predict(user_id, item_id)
            final_predictions.append(pred)
    
def get_top_n(predictions, n=10):
    top_n = defaultdict(list)
    for user_id, item_id, true_r, est, _ in predictions:
        top_n[user_id].append((item_id, est))
    # Sort and take top-N
    for user_id, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[user_id] = [item_id for (item_id, _) in user_ratings[:n]]
    return top_n

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🎬 Recommendation System (SVD)")

# User ID input
user_id = st.number_input("Enter User ID:", min_value=1, step=1)

# Number of recommendations
n = st.slider("Number of Recommendations", 1, 20, 5)

# Button to generate recommendations
if st.button("Get Recommendations"):
    
    top_n_preds_final = get_top_n(final_predictions, n)
  
    if user_id not in top_n_preds_final.keys():
        st.write(f"Message: User {user_id} not found")
        
    else:
        results = top_n_preds_final.get(user_id, [])
        recommended_books = books_df[books_df.ISBN.isin(results)]
        st.write("✅ Top Recommendations:")
        df_display = recommended_books[['ISBN','Book-Title','Book-Author','Publisher']].reset_index(drop=True)
        df_display.index = df_display.index + 1   # start from 1
        st.dataframe(df_display)