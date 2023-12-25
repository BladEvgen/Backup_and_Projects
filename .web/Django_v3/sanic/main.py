import aiosqlite
from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import NotFound
from pathlib import Path


class AsyncDatabase:
    def __init__(self, database_path: str):
        self.database_path = database_path

    async def query(
        self,
        query_str: str,
        args: tuple = (),
        many: bool = True,
        commit: bool = False,
    ) -> list | None:
        async with aiosqlite.connect(self.database_path) as connection:
            cursor = await connection.cursor()
            await cursor.execute(query_str, args)
            try:
                if many:
                    result = await cursor.fetchall()
                else:
                    result = await cursor.fetchone()
                if commit:
                    await connection.commit()
                return result
            except Exception as error:
                print(f"Error executing query {str(error)} ")
                return None


app = Sanic("ApiApp")


@app.post("/api")
async def handle_request(request):
    data = request.json
    database_id = data.get("database_id")
    match database_id:
        case 1:
            database_path = Path(__file__).resolve().parent.parent / "db.sqlite3"
        case 2:
            database_path = (
                Path(__file__).resolve().parent.parent / "database" / "database.db"
            )
        case _:
            raise NotFound("Invalid database_id")

    db = AsyncDatabase(database_path)

    result = await db.query(
        data["query"],
        data.get("args", ()),
        data.get("many", True),
        data.get("commit", False),
    )

    return json({"result": result})


@app.get("/")
async def home(request):
    return text("Home")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001, debug=True)
