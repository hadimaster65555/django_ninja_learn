from datetime import date
from ninja import NinjaAPI, Schema, UploadedFile, File
from django_ninja_learn.models import Employee
from django.shortcuts import get_object_or_404
from typing import List

api = NinjaAPI()


class HelloSchema(Schema):
    name: str = "world"


class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class UserSchema(Schema):
    username: str
    email: str = None
    first_name: str = None
    last_name: str = None


class Error(Schema):
    message: str


@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    if not request.user.is_authenticated:
        return 403, {'message': 'Please sign in first'}
    return request.user

@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello, {data.name}"


@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}


@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: UploadedFile = File(...)):
    payload_dict = payload.dict()
    employee = Employee(**payload_dict)
    employee.cv.save(cv.name, cv)
    return {"id": employee.id}


@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs


@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}


@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}