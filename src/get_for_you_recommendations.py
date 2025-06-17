
from preprocess import tfidf_matrix
import streamlit as st
from recommend import df
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_for_you_recommendations(df, tfidf_matrix, top_n=10):
    selected_indices = df[df['title'].isin(st.session_state.history)].index.tolist()

    if not selected_indices:
        return None  # No history, no recommendations

    # Mean → convert to array → flatten to 1D
    user_profile_vector = np.asarray(tfidf_matrix[selected_indices].mean(axis=0)).flatten()

    # Now define sim_scores (it was missing in your code!)
    sim_scores = cosine_similarity([user_profile_vector], tfidf_matrix).flatten()

    # Sort scores descending and remove already seen movies
    top_indices = sim_scores.argsort()[::-1]
    recommended_indices = [i for i in top_indices if i not in selected_indices][:top_n]

    result_df = df[['title']].iloc[recommended_indices].reset_index(drop=True)
    result_df.index = result_df.index + 1  # Start from 1
    result_df.index.name = "S.No."

    return result_df

