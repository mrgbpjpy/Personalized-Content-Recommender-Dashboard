# Import necessary modules
from flask import Flask, request, jsonify  # Flask: Official docs - https://flask.palletsprojects.com/en/3.0.x/
from flask_cors import CORS  # Flask-CORS: Official docs - https://flask-cors.readthedocs.io/en/latest/
import numpy as np  # NumPy: Official docs - https://numpy.org/doc/stable/
from sklearn.metrics.pairwise import cosine_similarity  # scikit-learn: Official docs - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html

app = Flask(__name__)
CORS(app)  # Enables Cross-Origin Resource Sharing for frontend-backend communication.

# Mock user data: Dictionary simulating user preferences (user_id: list of liked content ratings).
# In a real app, this would come from a database like SQLite or PostgreSQL.
users = {
    1: {'preferences': [5, 4, 0, 0, 5]},  # Ratings for mock contents: Movie1, Movie2, etc.
    2: {'preferences': [0, 0, 5, 4, 3]},
}

# Mock content data: List of content items with features (e.g., genres encoded as vectors).
contents = [
    {'id': 1, 'title': 'Action Adventure', 'features': [1, 0, 0, 0, 1]},
    {'id': 2, 'title': 'Sci-Fi Epic', 'features': [0, 1, 0, 0, 1]},
    {'id': 3, 'title': 'Comedy Special', 'features': [0, 0, 1, 1, 0]},
    {'id': 4, 'title': 'Drama Series', 'features': [0, 0, 1, 0, 0]},
    {'id': 5, 'title': 'Fantasy Tale', 'features': [1, 0, 0, 0, 1]},
]

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """
    Endpoint to get personalized recommendations.
    - Receives user_id via JSON POST.
    - Computes cosine similarity between user preferences and content features.
    - Returns top 3 recommended contents.
    
    Flask route decorator: Official docs - https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.route
    cosine_similarity: Computes the cosine similarity between vectors. Official docs - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
    """
    data = request.json  # Parses JSON from request. Official docs - https://flask.palletsprojects.com/en/3.0.x/api/#flask.Request.json
    user_id = data.get('user_id')
    
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404  # jsonify: Converts dict to JSON response. Official docs - https://flask.palletsprojects.com/en/3.0.x/api/#flask.json.jsonify
    
    user_prefs = np.array([users[user_id]['preferences']])  # np.array: Creates a NumPy array. Official docs - https://numpy.org/doc/stable/reference/generated/numpy.array.html
    
    # Compute similarities
    similarities = []
    for content in contents:
        content_features = np.array([content['features']])
        sim = cosine_similarity(user_prefs, content_features)[0][0]  # Computes similarity score.
        similarities.append((content['id'], sim))
    
    # Sort by similarity descending and get top 3
    top_recs = sorted(similarities, key=lambda x: x[1], reverse=True)[:3]  # sorted: Sorts list. Official docs - https://docs.python.org/3/library/functions.html#sorted
    rec_titles = [next(c['title'] for c in contents if c['id'] == rec[0]) for rec in top_recs]
    
    return jsonify({'recommendations': rec_titles})

if __name__ == '__main__':
    app.run(debug=True)  # Runs the Flask app. Official docs - https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.run
