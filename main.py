from pathlib import Path

from src.secret_santa import SecretSanta

if __name__ == "__main__":
    employee_file = "input/Employee-List.xlsx"  # Input file with employee data
    previous_assignments_file = "input/Secret-Santa-Game-Result-2023.xlsx"  # Last year's assignments

    output_path = Path("output")
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = "output/Secret-Santa-Assignments.xlsx"  # Output file

    secret_santa = SecretSanta(employee_file, previous_assignments_file)
    assignments = secret_santa.assign_secret_santa()
    if assignments:
        secret_santa.save_results(output_file, assignments)
