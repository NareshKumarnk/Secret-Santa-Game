# Secret Santa Game

## Overview

This project automates the process of assigning a Secret Santa to each employee while ensuring fairness and avoiding
previous-year assignments.

## Requirements

Before running the project, install the necessary dependencies.

### Install Dependencies

First, create a virtual environment (optional but recommended):

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Then, install the required packages:

```sh
pip install -r requirements.txt
```

## Running the Secret Santa Game

To execute the Secret Santa assignment script, run:

```sh
python main.py
```

Make sure you have the required input files (Employee List and Previous Assignments) in the correct location.

## Running Tests

To run the test cases using pytest, execute:

```sh
pytest
```

This will validate the logic, including ensuring that:

- Employees do not get assigned the same Secret Child as last year.
- Each employee has exactly one Secret Child.
- No employee is assigned to themselves.
- Each Secret Child is assigned to only one employee.

## Output

After running `main.py`, the assigned Secret Santa pairs will be saved in an output Excel file.