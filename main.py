from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

cnx = mysql.connector.connect(user='root', database='classroom')
app = FastAPI()


class Student(BaseModel):
    id: int | None
    name: str
    age: int
    email: str
    phone: str


@app.get("/students")
async def get_students():
    cursor = cnx.cursor(dictionary=True)
    query = 'SELECT * FROM `students`'
    cursor.execute(query)

    return cursor.fetchall()


@app.get("/students/{id}")
async def get_student_by_id(id: int):
    cursor = cnx.cursor(dictionary=True)
    query = 'SELECT * FROM `students` WHERE student_id = %s'
    val = (id, )
    cursor.execute(query, val)

    student = cursor.fetchone()

    if student:
        return student

    raise HTTPException(status_code=404, detail="Student not found")


@app.post("/students")
async def create_student(student: Student):
    cursor = cnx.cursor()
    statement = "INSERT INTO `students` (`student_name`,`student_age`,`student_mail`,`student_phone`) " \
                "VALUES (%s,%s,%s,%s)"
    val = (student.name, student.age, student.email, student.phone)

    cursor.execute(statement, val)

    cnx.commit()

    student.id = cursor.lastrowid

    return student


@app.put("/students/{id}")
async def update_student(id: int, student: Student):
    if id != student.id:
        raise HTTPException(status_code=400, detail="ID from path is not equals to body ID")

    cursor = cnx.cursor()
    statement = """
    UPDATE `students` SET 
        `student_name` = %s, 
        `student_age` = %s,
        `student_mail` = %s,
        `student_phone` = %s
    WHERE `student_id` = %s;
    """
    val = (student.name, student.age, student.email, student.phone, student.id)

    cursor.execute(statement, val)

    cnx.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.delete("/students/{id}")
async def delete_student(id: int):
    cursor = cnx.cursor()
    statement = """DELETE FROM `students` WHERE `student_id` = %s;"""
    val = (id, )

    cursor.execute(statement, val)

    cnx.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"detail": "deleted with success"}
