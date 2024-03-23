import asyncio
import os
import random
import time

import asyncpg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://0.0.0.0:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

database_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
}


class Database:
    def __init__(self):
        self.conn = None

    async def connect(self):
        self.conn = await asyncpg.connect(**database_config)

    async def disconnect(self):
        await self.conn.close()

    async def execute_query(self, query, *args):
        try:
            result = await self.conn.fetch(query, *args)
            return [dict(row) for row in result]
        except Exception as e:
            print(f"Error executing query: {e}")
            raise HTTPException(status_code=500, detail="Database error")

    async def create_tables(self):
        create_tables_queries = [
            """
            CREATE TABLE IF NOT EXISTS teams (
                team_id SERIAL PRIMARY KEY,
                team_name TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS questions (
                question_id SERIAL PRIMARY KEY,
                question_text TEXT,
                option1 TEXT,
                option2 TEXT,
                option3 TEXT,
                correct_option INTEGER
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS answers (
                answer_id SERIAL PRIMARY KEY,
                team_id INTEGER REFERENCES teams(team_id),
                question_id INTEGER REFERENCES questions(question_id),
                chosen_option INTEGER,
                response_time INTEGER
            );
            """,
        ]
        for query in create_tables_queries:
            await self.execute_query(query)

    async def initialize(self):
        await self.connect()
        await self.create_tables()


db = Database()


@app.on_event("startup")
async def startup_event():
    await db.initialize()


async def get_unanswered_question_id():
    answered_question_ids = await get_answered_question_ids()
    all_question_ids = await get_all_question_ids()
    unanswered_question_ids = list(set(all_question_ids) - set(answered_question_ids))
    if not unanswered_question_ids:
        return None
    return random.choice(unanswered_question_ids)


async def get_answered_question_ids():
    query = "SELECT DISTINCT question_id FROM answers"
    rows = await db.execute_query(query)
    return [row["question_id"] for row in rows]


async def get_all_question_ids():
    query = "SELECT question_id FROM questions"
    rows = await db.execute_query(query)
    return [row["question_id"] for row in rows]


async def get_question_by_id(question_id):
    query = "SELECT question_id, question_text, option1, option2, option3, correct_option FROM questions WHERE question_id = $1"
    return await db.execute_query(query, question_id)


async def get_question():
    question_id = await get_unanswered_question_id()
    if not question_id:
        return None
    questions = await get_question_by_id(question_id)
    if questions:
        return questions[0]
    else:
        return None


async def record_answer(team_id, question_id, chosen_option, response_time):
    query = "INSERT INTO answers (team_id, question_id, chosen_option, response_time) VALUES ($1, $2, $3, $4)"
    await db.execute_query(query, team_id, question_id, chosen_option, response_time)


async def get_scores():
    query = """
    SELECT teams.team_id, team_name, COUNT(*) AS score 
    FROM teams 
    JOIN answers ON teams.team_id = answers.team_id 
    JOIN questions ON answers.question_id = questions.question_id
    WHERE answers.chosen_option = questions.correct_option
    GROUP BY teams.team_id, teams.team_name 
    ORDER BY score DESC;
    """
    return await db.execute_query(query)


@app.get("/api/question")
async def get_question_api():
    question = await get_question()
    if not question:
        raise HTTPException(status_code=404, detail="No questions available")
    return {
        "question_id": question["question_id"],
        "question_text": question["question_text"],
        "options": [question["option1"], question["option2"], question["option3"]],
    }


@app.post("/api/answer")
async def submit_answer_api(team_id: int, question_id: int, chosen_option: int):
    response_time = int(time.time())
    await record_answer(team_id, question_id, chosen_option, response_time)
    return {"message": "Answer submitted successfully"}


@app.get("/api/scores")
async def get_scores_api():
    scores = await get_scores()
    return {"scores": scores}


@app.get("/api/")
async def api():
    return {"message": "Ok"}
