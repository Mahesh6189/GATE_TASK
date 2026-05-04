# GATE Question Bank REST API

A Django REST Framework backend for a GATE self-study platform. It supports subjects, topics, questions, user registration, attempts, and stats.

## Local setup

### 1. Clone repository

```bash
git clone https://github.com/Mahesh6189/GATE_TASK.git
cd GATE_TASK
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django djangorestframework
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Load seed data

```bash
python manage.py seed_questions
```

### 6. Run the server

```bash
python manage.py runserver
```

The API will run at `http://127.0.0.1:8000/`.

## Authentication flow

### Register a new user

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

Example response:

```json
{
  "message": "User created successfully",
  "token": "<token>"
}
```

### Login and get token

```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

Example response:

```json
{
  "message": "Login success",
  "user_id": 1,
  "username": "testuser",
  "token": "<token>"
}
```

### Make an authenticated request

```bash
curl -X POST http://127.0.0.1:8000/api/attempts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{"question":1,"selected_option":"B"}'
```

## Key endpoints

- `POST /api/register/` — register and receive a token
- `POST /api/login/` — login and receive a token
- `GET /api/questions/` — list questions
- `GET /api/questions/<id>/` — question details
- `POST /api/questions/` — create question (admin only)
- `PUT/PATCH /api/questions/<id>/` — update question (admin only)
- `DELETE /api/questions/<id>/` — delete question (admin only)
- `POST /api/attempts/` — submit an attempt (authenticated users)
- `GET /api/attempts/` — list current user attempts
- `GET /api/stats/` — get current user stats

## Design decisions

- **Token authentication** was chosen because the spec explicitly asks for DRF Token Authentication.
- **Questions are public to read** but restricted to admin users for creation, update, and deletion.
- **UserAttempt is tied to the authenticated user** and `user` is automatically set from the token, not provided by the client.
- **Duplicate attempts are prevented** with a unique constraint on `(user, question)` and validation in the serializer.
- **Seed command** loads sample data from `seed_data/questions.json` and safely skips duplicates.
- **Question filtering** is implemented on the list endpoint using query params for `subject`, `topic`, and `difficulty`.

## Notes

- If you want admin access, run `python manage.py createsuperuser`.
- The seed file includes at least 15 questions across multiple subjects.
- The project uses SQLite by default but can be updated to PostgreSQL in production.
