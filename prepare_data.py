
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("movies.csv")
df['overview'] = df['overview'].fillna('')

vectorizer = TfidfVectorizer(stop_words='english')
vector_matrix = vectorizer.fit_transform(df['overview'])

similarity = cosine_similarity(vector_matrix)

pickle.dump(df, open("movies_list.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))
print("movies_list.pkl and similarity.pkl created successfully.")
