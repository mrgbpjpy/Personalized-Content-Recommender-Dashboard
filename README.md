# Flask Content Recommendation API

A minimal Flask-based API that returns content recommendations using **cosine similarity** between a user's preference vector and each content item's feature vector.

## 🚀 Overview

This project demonstrates a tiny recommender service:
- Accepts a `user_id` via `POST /api/recommend`
- Looks up the user's preference ratings (mock data)
- Computes cosine similarity vs. each content's feature vector
- Returns the **top 3** recommended titles

> This is for learning/demo purposes and uses in-memory mock data. Swap in a real database for production.

---

## 🧰 Tech Stack

- **Python 3.10+**
- **Flask** — lightweight web framework  
  Docs: https://flask.palletsprojects.com/en/3.0.x/
- **Flask-CORS** — enable Cross-Origin Resource Sharing for browser frontends  
  Docs: https://flask-cors.readthedocs.io/en/latest/
- **NumPy** — numeric vectors & arrays  
  Docs: https://numpy.org/doc/stable/
- **scikit-learn** — cosine similarity utility  
  Docs: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html

---

## 📦 Project Structure

```
.
├─ app.py                # Your Flask app (the code you provided)
├─ requirements.txt      # (optional) Dependencies
└─ README.md             # This file
```

Example `requirements.txt`:

```
flask==3.0.3
flask-cors==4.0.1
numpy==2.0.1
scikit-learn==1.5.1
```

> Versions are examples—pin to what you use.

---

## 🔧 Setup & Run (Local)

1) **Create & activate a virtual environment (recommended):**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

2) **Install dependencies:**

```bash
pip install -r requirements.txt
# or, individually:
pip install flask flask-cors numpy scikit-learn
```

3) **Run the server:**

```bash
python app.py
# Flask dev server will start, e.g. http://127.0.0.1:5000
```

---

## 🔌 API

### `POST /api/recommend`

**Request body (JSON):**
```json
{
  "user_id": 1
}
```

**Success response (200):**
```json
{
  "recommendations": ["Action Adventure", "Fantasy Tale", "Sci-Fi Epic"]
}
```

**Error response (404):**
```json
{
  "error": "User not found"
}
```

#### cURL Example
```bash
curl -X POST http://127.0.0.1:5000/api/recommend   -H "Content-Type: application/json"   -d '{"user_id": 1}'
```

#### `fetch` Example (Frontend)
```js
fetch("http://127.0.0.1:5000/api/recommend", {
  method: "POST",
  headers: { "Content-Type: "application/json" },
  body: JSON.stringify({ user_id: 1 }),
})
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

---

## 🧠 How Recommendations Work

- Each **user** has a vector of **preference ratings** (e.g., `[5, 4, 0, 0, 5]`).
- Each **content** item has a **feature vector** (e.g., genre encoding `[1, 0, 0, 0, 1]`).
- We compute **cosine similarity** between the user vector and each content vector:
  - Higher similarity ⇒ stronger match ⇒ higher rank
- We sort by similarity and return the **top 3** titles.

> Cosine similarity docs:  
> https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html

---

## 🌐 CORS

`Flask-CORS` is enabled with `CORS(app)`, allowing calls from browser frontends during development. For production, **restrict allowed origins**:

```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": ["https://your-frontend.com"]}})
```

Docs: https://flask-cors.readthedocs.io/en/latest/

---

## 🗂️ Mock Data (Replace with DB)

- Users are stored in an in-memory dict:
  ```python
  users = {
      1: {"preferences": [5, 4, 0, 0, 5]},
      2: {"preferences": [0, 0, 5, 4, 3]},
  }
  ```
- Content items are also in-memory with feature vectors:
  ```python
  contents = [
      {"id": 1, "title": "Action Adventure", "features": [1, 0, 0, 0, 1]},
      {"id": 2, "title": "Sci-Fi Epic", "features": [0, 1, 0, 0, 1]},
      {"id": 3, "title": "Comedy Special", "features": [0, 0, 1, 1, 0]},
      {"id": 4, "title": "Drama Series", "features": [0, 0, 1, 0, 0]},
      {"id": 5, "title": "Fantasy Tale", "features": [1, 0, 0, 0, 1]},
  ]
  ```

To persist data, integrate a database (SQLite, PostgreSQL) and replace the dict lookups with DB queries.

---

## 🧪 Quick Tests

- Try `user_id: 1` and `user_id: 2` to see different recommendations.
- Try an unknown user (e.g., `999`) to trigger the 404 response.

---

## 🧱 Production Tips

- Use a production WSGI server (e.g., **gunicorn** or **waitress**).
- Add input validation and schema checks (e.g., **pydantic** or **marshmallow**).
- Restrict CORS to known origins.
- Configure logging and error handling.
- Add health checks and metrics.

### Gunicorn example
```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

---

## 🐳 (Optional) Docker

**Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

**Build & Run**
```bash
docker build -t flask-recommender .
docker run -p 5000:5000 flask-recommender
```

---

## 📝 License

MIT (or your preferred license).
