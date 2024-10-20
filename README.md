# Task Management API

The Task Management API is a RESTful web service designed to help users manage their to-do list. This API allows users to perform CRUD operations on tasks, manage user accounts, and filter and sort tasks based on various criteria.

## Features

- **User Authentication**: Secure user authentication system for task management.
- **Task CRUD Operations**: Users can create, read, update, and delete tasks.
- **Task Filtering**: Filter tasks by status, priority, and due date.
- **Task Sorting**: Sort tasks based on due date or priority.
- **Task Ownership**: Users can only access and modify their own tasks.

## Installation

Before you can run the server, you'll need to set up your Python environment and install the required dependencies.

1. Clone the repository:

git clone https://github.com/yourusername/task_management_api.git
cd task_management_api

2. It is recommended to set up a virtual environment:

python -m venv venv

Activate the virtual environment:

- For Windows:

  ```
  venv\Scripts\activate
  ```

- For Mac/Linux:

  ```
  source venv/bin/activate
  ```

3. Install the required dependencies:

pip install -r requirements.txt

4. Apply the migrations to create the database schema:

python manage.py migrate

5. Start the development server:

python manage.py runserver

6. The API should now be accessible at `http://localhost:8000/api/`.


## Usage

### User Registration

- **Endpoint**: `/users/`
- **Method**: `POST`
- **Body**:

```json
{
 "username": "newuser",
 "email": "newuser@example.com",
 "password": "newpassword"
}
```

### Task Management

Create Task: Send a POST request to /tasks/ with the task details.

List Tasks: Send a GET request to /tasks/ to retrieve a list of tasks.

Retrieve Task: Send a GET request to /tasks/<task_id>/ to retrieve a single task.

Update Task: Send a PUT/PATCH request to /tasks/<task_id>/ with the updated details.

Delete Task: Send a DELETE request to /tasks/<task_id>/.