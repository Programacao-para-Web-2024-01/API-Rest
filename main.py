from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Student(BaseModel):
    id: int | None
    name: str
    age: int
    email: str
    phone: str


students = [
    Student(id=1,
            name="John Doe",
            age=20,
            email="john.doe@example.com",
            phone="123456789")
]

global id_counter
id_counter = 1


@app.get("/students")
async def get_students():
    return students


@app.get("/students/{id}")
async def get_student_by_id(id: int):
    index, s = get_student(id)

    if s is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return s


@app.post("/students")
async def create_student(student: Student):
    if student.id is not None:
        raise HTTPException(status_code=400, detail="ID is not a valid field")

    student.id = new_id()

    students.append(student)
    return student


@app.put("/students/{id}")
async def update_student(id: int, student: Student):
    if id != student.id:
        raise HTTPException(status_code=400, detail="ID from path is not equals to body ID")

    index, s = get_student(id)

    if index is None:
        raise HTTPException(status_code=404, detail="Student not found")

    students[index] = student

    return student


def new_id():
    global id_counter
    id_counter += 1

    return id_counter


def get_student(id: int):
    for index, s in enumerate(students):
        if s.id == id:
            return index, s

    return None, None
