# %%
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# %%
df = pd.read_csv('/Users/jeevu/Desktop/notes_backend/api/tmdb_5000_movies.csv')

# %%
# df["overview"].fillna('', inplace=True)
df.fillna({"overview": ""}, inplace=True)

# %%
tfid = TfidfVectorizer(stop_words="english")
tfid_matrix = tfid.fit_transform(df["overview"])

# %%
movies = pd.Series(df.index, index=df["original_title"]).drop_duplicates()

# %%
cosine_sim = cosine_similarity(tfid_matrix, tfid_matrix)

# %%


def get_recommendation(title, cosine_sim=cosine_sim):
    try:
        id = movies[title]
        score = enumerate(cosine_sim[id])
        score = sorted(score, key=lambda x: x[1], reverse=True)
        score = score[1:6]
        sim_index = [i[0] for i in score]
        return (df["original_title"].iloc[sim_index].tolist())
    except:
        return ("")


# %%


# %%
