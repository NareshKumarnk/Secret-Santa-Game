# Test cases for SecretSanta class
from src.secret_santa import SecretSanta

employee_file = "tests/input/test_employees.xlsx"  # Input file with employee data
previous_assignments_file = "tests/input/test_previous.xlsx"  # Last year's assignments
output_file = "tests/output/test_output.xlsx"  # Output file


def test_load_employees():
    secret_santa = SecretSanta(employee_file)
    assert len(secret_santa.team_members) > 0, "Employee details should not be empty"
    assert isinstance(secret_santa.team_members, list)
    assert isinstance(secret_santa.team_members[0], tuple)


def test_load_previous_assignments():
    secret_santa = SecretSanta(employee_file, previous_assignments_file)
    assert isinstance(secret_santa.past_matches, dict)


def test_assign_secret_santa():
    secret_santa = SecretSanta(employee_file, previous_assignments_file)
    assignments = secret_santa.assign_secret_santa()
    assert len(assignments) == len(
        secret_santa.team_members), "Each Employee should be assigned exactly one Secret Child"
    assigned_children = set(child[3] for child in assignments)
    assert len(assigned_children) == len(secret_santa.team_members), "Each Secret Child should be unique"


def test_no_repeated_assignments():
    secret_santa = SecretSanta(employee_file, previous_assignments_file)
    assignments = secret_santa.assign_secret_santa()
    for emp_name, emp_email, child_name, child_email in assignments:
        assert child_email != secret_santa.past_matches.get(emp_email,
                                                            None), f"Employee {emp_email} was incorrectly assigned the same Secret Child as last year: {child_email}."


def test_each_employee_has_one_secret_child():
    secret_santa = SecretSanta(employee_file, previous_assignments_file)
    assignments = secret_santa.assign_secret_santa()
    assigned_employees = {emp_email for emp_name, emp_email, _, _ in assignments}
    assert len(assigned_employees) == len(assignments), "Each employee should be assigned exactly one Secret Child."


def test_employee_not_assigned_to_self():
    secret_santa = SecretSanta(employee_file, previous_assignments_file)
    assignments = secret_santa.assign_secret_santa()
    for emp_name, emp_email, child_name, child_email in assignments:
        assert emp_email != child_email, f"Employee {emp_email} was assigned to themselves, which is not allowed."


def test_each_secret_child_only_assigned_once():
    secret_santa = SecretSanta(employee_file, previous_assignments_file)
    assignments = secret_santa.assign_secret_santa()
    assigned_children = [child_email for _, _, _, child_email in assignments]
    assert len(assigned_children) == len(set(assigned_children))  # Ensure uniqueness


def test_save_assignments(tmp_path):
    secret_santa = SecretSanta(employee_file, previous_assignments_file)
    assignments = secret_santa.assign_secret_santa()
    output_file = tmp_path / "test_output.xlsx"
    secret_santa.save_results(output_file, assignments)
    assert output_file.exists(), "Output file should be created successfully."
