# TASKTIFY: A Task Management System

---

TASKTIFY is a desktop-based task management system developed using Python and PyQt6. It allows users to create, view, update, and delete tasks while keeping track of important task information such as title, description, category, priority, due date, and status.

The system uses SQLite as its database for storing task records. It also provides a dashboard where users can view task statistics and upcoming tasks. An Easter Egg feature is also included, which displays a randomly selected Bible verse.

TASKTIFY was developed using modular programming and Object-Oriented Programming (OOP) to organize the system into separate modules based on their responsibilities.

---

## Objectives

---

The main objectives of TASKTIFY are:

- To provide a simple task management system.
- To allow users to create, view, update, and delete tasks.
- To organize tasks using categories and priorities.
- To monitor task status and due dates.
- To provide search and filtering functions.
- To store task information using an SQLite database.
- To apply modular programming in organizing the project.
- To apply Object-Oriented Programming concepts.
- To provide a dashboard for monitoring tasks.
- To include an Easter Egg feature that provides motivational Bible verses.

---

## Features

---

| # | Feature | Description | Functions / Details |
|---|---|---|---|
| 1 | **Dashboard** | Provides an overview of the user's tasks. | Total Tasks, Pending Tasks, Completed Tasks, Overdue Tasks, Due Soon Tasks, Upcoming Tasks, and access to the Easter Egg |
| 2 | **Task Management** | Allows users to manage their task records through the My Tasks page. | Add, view, edit, delete, search, and filter tasks |
| 3 | **Add Task** | Allows users to create a new task and save it to the database. | Task Title, Description, Category, Priority, Due Date, and Status |
| 4 | **Edit Task** | Allows users to modify an existing task. | Edit Title, Description, Category, Priority, Due Date, and Status |
| 5 | **Delete Task** | Allows users to remove an existing task from the database. | Delete task with confirmation dialog |
| 6 | **Search and Filtering** | Helps users find and organize tasks. | Search by Title, Description, or Category; filter by Category, Priority, or Status |
| 7 | **Task Status** | Allows users to track the current status of a task. | Pending and Completed |
| 8 | **Due Date Tracking** | Automatically determines the state of a task based on its due date and status. | Upcoming, Due Soon, Overdue, and Completed. A task is Due Soon when its due date is within two days |
| 9 | **Easter Egg** | Provides an interactive egg that reveals a randomly selected Bible verse. | Animated egg, random Bible verse selection, and verse display dialog |

---

## Technologies Used

---

| Category | Technologies / Tools |
|---|---|
| Programming Language | Python |
| GUI Framework | PyQt6 |
| Database | SQLite, Python `sqlite3` module |
| Python Libraries and Modules | `sqlite3`, `pathlib`, `dataclasses`, `random`, `datetime`, `sys` |
| PyQt6 Modules | `PyQt6.QtWidgets`, `PyQt6.QtCore`, `PyQt6.QtGui` |
| Development Tools | PyCharm, Git, GitHub |

---

## Project Structure

---


```text
TASKTIFY_/
├── main.py                         # Entry point; initializes the application and main window
├── main_window.py                  # Main window, dashboard, task management, and feature integration
├── styles.py                       # Custom PyQt6 styles for the TASKTIFY interface
│── tasktify.db                     # Local SQLite database that stores task records
|
├── database/
│   └── database.py                 # SQLite connection manager and database query handler
|
└── features/
    ├── easter_egg/                 # Easter Egg feature for displaying random Bible verses
    │   ├── model.py                # Verse dataclass and data structure
    │   ├── repository.py           # Stores and retrieves the available Bible verses
    │   ├── service.py              # Easter Egg business logic and verse handling
    │   └── view.py                 # Easter Egg interface, animations, and verse dialog
    │
    └── tasks/                      # Task management and CRUD operations
        ├── model.py                # Task dataclass and task data structure
        ├── repository.py           # SQL queries for task records
        ├── service.py              # Task validation, business logic, and due-date processing
        └── view.py                 # Task entry and editing dialogs
```


### Main Components

`main.py`  
Serves as the entry point of TASKTIFY. It initializes the PyQt6 application, connects the SQLite database, creates the main window, and starts the application event loop.

`database/database.py`  
Handles the SQLite database connection, creates the tasks table, and provides functions for executing queries and retrieving database records.

`features/tasks/`  
Handles task management, including task data, validation, database operations, CRUD operations, due-date processing, searching, filtering, and the task interface.

`features/easter_egg/`  
Handles the Easter Egg feature, including Bible verse data, random verse selection, the animated egg interaction, and the verse display interface.

`main_window.py`  
Contains the main TASKTIFY interface and connects the dashboard, My Tasks page, task operations, search and filtering, task statistics, upcoming tasks, and Easter Egg feature.

`styles.py`  
Contains the custom PyQt6 styles used throughout the TASKTIFY graphical interface, including the main window, buttons, tables, dialogs, and input fields.

`tasktify.db`  
Contains the local SQLite database used to store the task records created and managed by the user.


---

## Installation and Setup

---

### Requirements:

Before running TASKTIFY, make sure the following are installed:

- Python 
- PyQt6
- Git, if cloning the project from GitHub

### 1. Clone the Repository

```bash
git clone https://github.com/frd-1/TASKTIFY_.git

```
### 2. Create a Virtual Environment (Optional)

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install PyQt6

```bash
pip install PyQt6
```

### 5. Run the Application

```bash
python main.py
```

The application connects to the local SQLite database and uses the tasktify.db file to store task records.

---


## How to Use the System

---

### Step 1: Open TASKTIFY

Run:

```bash
python main.py
```
The TASKTIFY main window will appear.

### Step 2: Dashboard


The Dashboard displays task statistics and upcoming tasks.


### Step 3: Adding a Task

Select **Add Task** and enter:

- Title
- Description
- Category
- Priority
- Due Date
- Status

Save the task to store it in the database.

### Step 4: Viewing Tasks

Open **My Tasks** to view the stored task records.

### Step 5: Searching Tasks

Enter a keyword in the search field.

The system searches through the task:

- Title
- Description
- Category

### Step 6. Filtering Tasks

Use the filters to filter tasks by:

- Category
- Priority
- Status

### Step 7: Editing a Task

Select an existing task and use the edit function to modify its information.

### Step 8: Deleting a Task

Select an existing task and use the delete function to remove it from the database.

### 9. Easter Egg

Click the Easter Egg feature from the dashboard to interact with the egg and reveal a randomly selected Bible verse.

---

## Object-Oriented Programming Implementation

---

TASKTIFY applies Object-Oriented Programming through classes and objects.

### Important Classes

| Class | Purpose |
|---|---|
| `Database` | Handles SQLite database operations |
| `Task` | Represents a task |
| `TaskRepository` | Handles task database operations |
| `TaskService` | Handles task validation and business logic |
| `TaskDialog` | Provides the task input/edit interface |
| `Verse` | Represents a Bible verse |
| `VerseRepository` | Stores and selects Bible verses |
| `VerseService` | Handles verse-related logic |
| `VerseDialog` | Displays Bible verses |
| `EggWidget` | Provides the interactive Easter Egg |
| `MainWindow` | Provides the main application interface|

### Encapsulation

Encapsulation is applied by separating responsibilities among different classes. Database operations are handled by the database and repository classes, while task validation and business logic are handled by `TaskService`.

### Inheritance

PyQt6 classes are extended to create custom GUI components.

Examples include:

```text
MainWindow → QMainWindow
TaskDialog → QDialog
VerseDialog → QDialog
EggWidget → QFrame
```

This allows TASKTIFY to use existing PyQt6 functionality while adding its own behavior.

### Polymorphism

Polymorphism is demonstrated through customized PyQt6 event methods.

For example, `EggWidget` overrides methods such as:

- `mousePressEvent()`
- `paintEvent()`

These allow the widget to respond to user interaction and display the egg differently based on its current state.

### Abstraction

TASKTIFY applies abstraction by hiding the internal implementation of database operations and business logic from the graphical user interface.

For example, `MainWindow` does not need to directly handle SQL statements when managing tasks. Instead, task operations are handled through `TaskService`, `TaskRepository`, and `Database`.

This allows the interface to use the required functionality without directly managing the database implementation.


### Modular Programming

TASKTIFY separates its features into modules according to their responsibilities.

The task feature follows this structure:

```text
model.py
repository.py
service.py
view.py
```

The Easter Egg feature follows the same structure.

| Module | Responsibility |
|---|---|
| Model | Represents application data |
| Repository | Handles data storage and retrieval |
| Service | Handles validation and business logic |
| View | Handles the graphical user interface |

This structure separates the different responsibilities of the system and makes the project easier to maintain and modify.


---

## Database

---

TASKTIFY uses SQLite for local data storage.

The database file is:

```text
tasktify.db
```

The database is managed through the `Database` class in `database/database.py`.

### Tasks Table

The system creates a `tasks` table containing the following fields:

| Field | Data Type | Description |
|---|---|---|
| `id` | INTEGER | Primary key and unique task identifier |
| `title` | TEXT | Task title |
| `description` | TEXT | Task description |
| `category` | TEXT | Task category |
| `priority` | TEXT | Task priority |
| `due_date` | TEXT | Task due date |
| `status` | TEXT | Current task status |

---

## CRUD Operations

---

TASKTIFY implements the four basic CRUD (Create, Read, Update, Delete) operations to manage task records stored in the SQLite database. These operations are handled primarily by the `TaskRepository` class, which communicates with the `Database` class to execute the required SQL operations.

| Operation | TASKTIFY Function | Specific Implementation |
|---|---|---|
| **Create** | Add a new task | The user enters the task title, description, category, priority, due date, and status through the `TaskDialog`. The task information is validated and passed to `TaskRepository`, which inserts the new record into the SQLite `tasks` table. |
| **Read** | View and retrieve tasks | `TaskRepository` retrieves task records from the SQLite database. The retrieved tasks are converted into `Task` objects and displayed in the My Tasks page and Dashboard. |
| **Update** | Edit an existing task | The user selects an existing task and modifies its information through the `TaskDialog`. The updated values are validated and passed to `TaskRepository`, which updates the corresponding database record using its task ID. |
| **Delete** | Remove a task | The user selects a task to delete and confirms the deletion through the confirmation dialog. `TaskRepository` then removes the selected task record from the SQLite database using its task ID. |

---

## Search and Filtering

TASKTIFY provides search and filtering functionality.

### Search

Users can search by:

- Title
- Description
- Category

### Filters

Users can filter tasks by:

- Category
- Priority
- Status

---

## Screenshots

---

### Dashboard

![Dashboard](screenshots/dashboard.png)

Shows the TASKTIFY dashboard containing task statistics, upcoming tasks, and access to the Easter Egg.

### My Tasks

![My Tasks](screenshots/my_tasks.png)

Shows the task table containing the saved tasks.

### Add Task

![Add Task](screenshots/add_task.png)

Shows the dialog used to create a new task.

### Edit Task

![Edit Task](screenshots/edit_task.png)

Shows the dialog used to modify an existing task.

### Search and Filter

![Search and Filter](screenshots/search_filter.png)

Shows the search and filtering functionality.

### Easter Egg

![Easter Egg](screenshots/easter_egg.png)

Shows the interactive Easter Egg and Bible verse display.

---

## Testing

---

The following test cases cover the main functions implemented in TASKTIFY.

| Test Area | Test Action | Expected Result | Status |
|---|---|---|---|
| Application | Run `main.py` | TASKTIFY opens successfully | Passed |
| Database | Start the application | Database connects successfully | Passed |
| Add Task | Add a valid task | Task is saved and displayed | Passed |
| View Task | Open My Tasks | Saved tasks are displayed | Passed |
| Edit Task | Edit an existing task | Task information is updated | Passed |
| Delete Task | Delete a task | Task is removed | Passed |
| Validation | Enter invalid or incomplete information | Invalid input is rejected | Passed |
| Search | Search for a task | Matching tasks are displayed | Passed |
| Filter | Filter by category, priority, or status | Matching tasks are displayed | Passed |
| Due State | Use different due dates | Correct due state is displayed | Passed |
| Dashboard | View task statistics | Correct statistics are displayed | Passed |
| Easter Egg | Interact with the egg | A Bible verse is displayed | Passed |
| Data Persistence | Restart the application | Saved tasks remain available | Passed |
---

## Known Issues and Limitations

---

TASKTIFY is designed as a local desktop task management system.

The current system has the following limitations:

- It uses a local SQLite database.
- It does not include user accounts or login functionality.
- It does not provide cloud synchronization.
- It does not support multiple users.
- Search and filtering are performed within the application's task data.
- The Bible verses used by the Easter Egg are predefined.
- The system does not include notifications or reminders.
- The system does not include task export functionality.
- The system does not include automatic database backup.

These limitations can be addressed in future versions of the project.

---

## Future Improvements

Possible improvements for future versions include:

- User login and account management
- Cloud database support
- Task notifications and reminders
- Task export
- Database backup and restore
- More customization options
- Additional motivational features
- More Bible verses for the Easter Egg

---

## Author

**Name:**  *Francesca Anne Marie B. Delosa*

**Section:** *CS26/L (3581)*



