# Add a GET /students endpoint

# Return all students as a list

# If no students exist, return a message "No students found"

# Create GET /students/filter

# Query parameter: min_age

# Return students whose age ≥ min_age

from fastapi import FastAPI, Query
from typing import Optional, List
from pydantic import BaseModel


app = FastAPI()


students ={
    1:{
        'name':'Gunay',
        'surname':'Hummatova',
        'age':25,
    },
    2:{
        'name':'Gunay2',
        'surname':'Hummatova2',
        'age':24,
    },
    3:{
        'name':'Gunay3',
        'surname':'Hummatova3',
        'age':23,
    }
}

class Student(BaseModel):
    name: str
    surname: str
    age: int




# Return all students as a list

@app.get('/all-students')
def get_students():
    if len(students) == 0:
        return {'Error':'There is no student'}
    return list(students.values())

# Create GET /students/filter
# Query parameter: min_age
# Return students whose age ≥ min_age

@app.get('/students/filter/', response_model=List[Student])
def filter_students(min_age: int = Query(..., ge=5)):
    return [student for student in students.values() if student['age']>=min_age]

