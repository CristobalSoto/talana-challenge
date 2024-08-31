## Introduction

This README outlines the steps required to set up and run this project on a local machine. It provides a systematic approach to ensure the project is correctly configured for development and execution.

## Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)

## Setup Instructions

### Step 1: Create a Virtual Environment

To isolate and manage dependencies, create a virtual environment in your project directory:
python -m venv venv

### Step 2: Activate the Virtual Environment

Activate the virtual environment with the following command:

On Windows:

```cmd
.\venv\Scripts\activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

With the virtual environment activated, install the required dependencies:

```python
pip install -r requirements.txt
```

### Step 4: Create database

Run the creation of the database (this will create the tables and some sample data)

```python
python seed_data.py
```


### Step 5: Run the Project

Finally, run the project from the root directory:

```python
python run.py
```

## Additional information

The use of a migration tool like Alembic was not deemed necessary due to the small amount of data
so the migration I used is to create sample data for testing purposes in the seed_data.py
this file deletes the database and create a new one.

the services_legacy.py file has the previous iteration of the solution, at the begining the skills and available values were 
stored in a column as a list so the solution may not work as before but the logic is there.



