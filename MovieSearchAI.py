import pymongo
from bson.binary import Binary
from bson import ObjectId
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai

# Connect to MongoDB Atlas
client = pymongo.MongoClient("YOUR_MONGODB_ATLAS_CONNECTION_STRING")
db = client["movie_database"]
collection = db["movies"]

# Connect to OpenAI API
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Sample movie data
movies_data = [
    {"title": "Die Hard", "description": "Action movie involving a cop and bad guys."},
    {"title": "The Dark Knight", "description": "Superhero movie with action and a corrupt cop."},
    {"title": "Heat", "description": "Crime thriller with cops and robbers."},
    {"title": "Training Day", "description": "Drama about corrupt cops."},
    {"title": "Lethal Weapon", "description": "Buddy cop action-comedy."},
    {"title": "Fargo", "description": "Crime drama with kidnappers and cops."},
    {"title": "Point Break", "description": "Action movie about surfing and bank robbers."},
    {"title": "RoboCop", "description": "Sci-fi action movie with a cop who's part machine."},
    {"title": "The Departed", "description": "Crime drama about moles in the police force."},
    {"title": "Bad Boys", "description": "Action-comedy about two cops."},
]

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english')

# Vectorize movie descriptions and store in MongoDB
vectorized_descriptions = vectorizer.fit_transform([movie['description'] for movie in movies_data])
for i, movie in enumerate(movies_data):
    movie['Vector_embeddings'] = Binary(vectorized_descriptions[i].toarray())

# Insert movies into MongoDB
collection.insert_many(movies_data)

# Create Atlas vector search index for Vector_embeddings attribute
collection.create_index([("Vector_embeddings", "2dsphere")])

# Function to search for movies based on user prompt
def search_movies(user_prompt):
    # Vectorize user prompt
    user_prompt_vectorized = vectorizer.transform([user_prompt])

    # Search for similar movies using cosine similarity
    similar_movies = collection.find({}, {"Vector_embeddings": 1})
    results = []
    for movie in similar_movies:
        movie_vector = np.frombuffer(movie['Vector_embeddings'], dtype=np.float64).reshape(1, -1)
        similarity = cosine_similarity(user_prompt_vectorized, movie_vector)
        results.append((movie['_id'], similarity[0][0]))

    # Sort results by similarity score
    results.sort(key=lambda x: x[1], reverse=True)
    movie_ids = [result[0] for result in results]

    # Retrieve movie titles based on IDs
    movie_titles = [movie['title'] for movie in collection.find({"_id": {"$in": movie_ids}})]

    return movie_titles

# Example user prompt
user_prompt = "Movies with action involving cops and bad guys"

# Search for movies based on the user prompt
movie_titles = search_movies(user_prompt)

# Display the search results
print("Movies matching the user prompt:")
for title in movie_titles:
    print(title)







# In this code:

#     We connect to MongoDB Atlas and OpenAI's API using their respective credentials.
#     Sample movie data is provided with titles and descriptions, including those related to cops, bad guys, and action.
#     We use TF-IDF vectorization to convert movie descriptions into numerical vectors.
#     The vectorized descriptions are stored in MongoDB along with other movie attributes.
#     We create an Atlas vector search index for the Vector_embeddings attribute.
#     The search_movies function retrieves similar movies based on a user prompt by calculating cosine similarity between the vectorized user prompt and movie descriptions.
#     We demonstrate the process by searching for movies based on the user prompt "Movies with action involving cops and bad guys" and printing the matching titles.

# Please replace 'YOUR_MONGODB_ATLAS_CONNECTION_STRING' and 'YOUR_OPENAI_API_KEY' with your actual MongoDB Atlas connection string and OpenAI API key, respectively. Additionally, ensure you have installed the necessary Python packages like pymongo, scikit-learn, and openai.