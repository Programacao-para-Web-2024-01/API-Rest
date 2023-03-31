from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

import os
import requests

load_dotenv()
from deta import Deta  # Import Deta

deta = Deta(os.environ["PROJECT_KEY"])

db = deta.Base("students")

app = FastAPI()


class Student(BaseModel):
    name: str
    age: int
    email: str
    phone: str


@app.get("/")
async def hello_world():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    return {
        "status_code": response.status_code,
        "headers": response.headers,
        "response": response.json()
    }


@app.get("/students")
async def get_students():
    res = db.fetch()
    all_items = res.items

    # fetch until last is 'None'
    while res.last:
        res = db.fetch(last=res.last)
        all_items += res.items

    return all_items


@app.get("/students/{id}")
async def get_student_by_id(id: str):
    student = db.get(id)

    if student:
        return student

    raise HTTPException(status_code=404, detail="Student not found")


@app.post("/students")
async def create_student(student: Student):
    new_student = db.insert(student.dict())

    return new_student


@app.put("/students/{id}")
async def update_student(id: str, student: Student):
    db.update(student.dict(), id)

    return student


@app.delete("/students/{id}")
async def delete_student(id: str):
    db.delete(id)

    return {"detail": "deleted with success"}
