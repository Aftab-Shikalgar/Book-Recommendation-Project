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
list_of_users = loaded["list_of_users"]

all_users = user_item_df['User-ID'].unique()
all_books = user_item_df['ISBN'].unique()

def get_top_n_for_user(user_id, n=10):
    user_rated_books = set(user_item_df[user_item_df['User-ID'] == user_id]['ISBN'])
    predictions = []

    for item_id in all_books:
        if item_id not in user_rated_books:
            pred = best_model.predict(user_id, item_id)
            predictions.append((item_id, pred.est))

    # sort and return top-N
    predictions.sort(key=lambda x: x[1], reverse=True)
    top_items = [item_id for item_id, _ in predictions[:n]]
    return top_items

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🎬 Recommendation System (SVD)")

# User ID input

user_id = st.selectbox(
    "Enter User ID", 
    options=list_of_users
)


#user_id = st.number_input("Enter User ID:", min_value=1, step=1)

# Number of recommendations
n = st.slider("Number of Recommendations", 1, 20, 5)

# Button to generate recommendations
if st.button("Get Recommendations"):
    if user_id not in all_users:
        st.write(f"Message: User {user_id} not found")
    else:
        results = get_top_n_for_user(user_id, n)
        recommended_books = books_df[books_df.ISBN.isin(results)]
        
        st.write("✅ Top Recommendations:")
        df_display = recommended_books[['ISBN','Book-Title','Book-Author','Publisher']].reset_index(drop=True)
        df_display.index = df_display.index + 1
        st.dataframe(df_display)