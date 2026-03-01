!(Employee Management Account)(Images/Employee_Management_Account.png)

# Incubyte Salary Management API
### Overview

This project implements a Salary Management API as part of the Incubyte engineering hiring process.

The application provides:

- Employee CRUD operations

- Salary calculation with country-based deduction rules

- Salary metrics by country and job title

- Persistent storage using SQLite

- Strict Test-Driven Development (TDD) workflow

The API is built using FastAPI and follows a clean separation of concerns between routers, services, and repository layers.

## Tech Stack
- Python 3.13

- FastAPI

- SQLite

- Pytest

- Pydantic

## Architecture Overview
```
app/
 ├── main.py              # FastAPI routes
 ├── database.py          # DB connection & initialization
 ├── repository.py        # Database operations
 ├── services.py          # Business validation logic
 ├── salary_service.py    # Salary calculation logic
 ├── salary_metrics.py    # Salary aggregation logic
tests/
 ├── test_management_crud.py
 ├── test_salary_calculation.py
 ├── test_salary_metrics.py
 ├── test_sqlite_persistence.py

```
## Design Principles
- Thin API layer (routes only coordinate)

- Business logic isolated in services

- Database access abstracted in repository layer

- Clear validation rules

- Deterministic, fast unit tests

- SQLite persistence (no in-memory storage)

## How to Run the Project
 ### Install dependencies
```
pip install -r requirements.txt
```
### Run the API
'''
uvicorn app.main:app --reload
```
### The API will start at:
'''
http://127.0.0.1:8000
```
### Swagger documentation:
```
http://127.0.0.1:8000/docs
```
## Running Tests
```
python -m pytest tests -v
```
## All tests are:
- Fast

- Deterministic

- Independent

- Database-backed (SQLite)
  
## API Endpoints
### Employee CRUD
### Create Employee
```
POST /employees
```
### Get All Employees
```
GET /employees
```
### Get Employee by ID
```
GET /employees/{employee_id}
```
### Update Employee
```
PUT /employees/{employee_id}
```
### Delete Employee
```
DELETE /employees/{employee_id}
```
### Salary Calculation
```
GET /employees/{employee_id}/salary
```
## Deduction Rules

| Country       | Deduction |
| ------------- | --------- |
| India         | 10%       |
| United States | 12%       |
| Others        | 0%        |

## Response example:
```
{
  "gross_salary": 100000,
  "deduction": 10000,
  "net_salary": 90000
}
```
## Salary Metrics
 ### By Country
 ```
  GET /metrics/salary?country=India
 ```
 ### Returns:
 ```
{
  "min_salary": 50000,
  "max_salary": 150000,
  "average_salary": 90000
}
```
### By Job Title
```
GET /metrics/salary?job_title=Backend Engineer
```
### Returns:
```
{
  "average_salary": 120000
}
```
## Business Rules
- Salary must be positive

- Salary cannot decrease during update

- Employee must exist for salary calculation

- Metrics require either country or job_title (not both)

- Proper HTTP status codes are returned for all edge cases

## Test Coverage
The following areas are covered with unit tests:
- Employee CRUD operations

- Salary validation rules

- Salary calculation logic

- Salary metrics aggregation

- SQLite persistence

- Edge cases (non-existing employee, invalid metrics query)

### The development process followed strict TDD:
```
Red → Green → Refactor
```
## Each feature was:

1. Introduced with a failing test

2. Implemented minimally to pass

3. Refactored for clarity and separation of concerns

## AI Usage & Rationale
### AI tools (ChatGPT) were intentionally used to:
- Scaffold initial FastAPI structure

- Generate test skeletons

- Suggest refactoring improvements

- Review architecture for production readiness

- Validate edge cases and API design consistency
  
### All AI-generated suggestions were:
- Manually reviewed

- Adapted to fit project requirements

- Refactored to maintain clean architecture principles
  
### Architectural decisions, business rules, and validation logic were intentionally designed and validated beyond AI-generated drafts.

## Production Readiness Considerations
- SQLite persistence ensures durability

- Context-managed DB connections

- Clear error handling with proper HTTP status codes

- Layered architecture

- Clean separation of concerns

- Deterministic unit tests

### Future improvements could include:

- Dependency injection for DB sessions

- Logging middleware

- Docker containerization

- CI pipeline integration

- Pagination for employee listing

## Final Notes
### This project was implemented with a focus on:
- Clean code

- Test-driven development

- Production-minded structure

- Clear business logic separation

- Maintainability
