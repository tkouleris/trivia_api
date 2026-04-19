# Trivia API

A Flask-based REST API for a trivia game that uses the Open Trivia Database (OpenTDB) to fetch questions. It includes user authentication, score tracking, and statistics.

## Project Links
- [Trivia API](https://github.com/tkouleris/trivia_api)
- [Mobile App](https://github.com/tkouleris/trivia_app_mobile)
- [Web App](https://github.com/tkouleris/trivia_app_web)

## Prerequisites

- Python 3.8+
- MySQL (or any other SQLAlchemy-supported database)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tkouleris/trivia_api.git
   cd trivia_api
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `env.example` to `.env`:
     ```bash
     cp env.example .env
     ```
   - Edit `.env` and provide your database URI and a secret key:
     ```
     SQLALCHEMY_DATABASE_URI=mysql://username:password@localhost/db_name
     SECRET_KEY=your_super_secret_key
     ```

## Database Setup

Initialize the database and run migrations:

```bash
flask db upgrade
```

## Running the Application

To start the development server:

```bash
flask run
```
The API will be available at `http://127.0.0.1:5000`.

## API Documentation

### Authentication

#### Signup
- **URL:** `/signup`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "username": "your_username",
    "email": "user@example.com",
    "password": "your_password"
  }
  ```

#### Login
- **URL:** `/login`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "your_password"
  }
  ```
- **Response:** Returns a JWT `token`.

#### Refresh Token
- **URL:** `/refresh`
- **Method:** `POST`
- **Headers:** `Authorization: Bearer <token>`

---

### Trivia Endpoints

All endpoints below require a valid JWT token in the `Authorization` header.

#### Get Questions
- **URL:** `/trivia`
- **Method:** `GET`
- **Query Parameters:**
  - `category`: (Optional) Category name (e.g., `GENERAL_KNOWLEDGE`, `SCIENCE_AND_NATURE`, `HISTORY`, etc.)
  - `total_questions`: (Optional) Number of questions (Default: 10)
  - `difficulty`: (Optional) `easy`, `medium`, or `hard` (Default: `easy`)

#### Submit Results
- **URL:** `/submit`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "points": 100,
    "total_questions": 10,
    "correct_answers": 8,
    "wrong_answers": 2,
    "difficulty": "easy"
  }
  ```

#### Get Statistics
- **URL:** `/stats`
- **Method:** `GET`
- **Response:** Returns totals for points, questions, and correct answers for the authenticated user.

## Supported Categories

- GENERAL_KNOWLEDGE
- BOOKS
- FILM
- MUSIC
- MUSICAL_AND_THEATRE
- TELEVISION
- VIDEO_GAMES
- BOARD_GAMES
- SCIENCE_AND_NATURE
- COMPUTERS
- MATH
- MYTHOLOGY
- SPORTS
- GEOGRAPHY
- HISTORY
- POLITICS
- ART
- CELEBRITIES
- ANIMALS
