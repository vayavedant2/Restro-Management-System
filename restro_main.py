import json
from datetime import datetime

# -------------------- Employee Class --------------------
class Employee:
    def __init__(self, name, salary, emp_id, added_on=None, updated_on=None):
        self.name = name
        self.salary = salary
        self.emp_id = emp_id
        self.added_on = added_on if added_on else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_on = updated_on  # Will update when salary or name changes

    def show_details(self):
        print(f"Employee ID: {self.emp_id}, Name: {self.name}, Salary: {self.salary}, Added On: {self.added_on}, Last Updated: {self.updated_on if self.updated_on else 'Never'}")

    def __str__(self):
        return f"Employee ID: {self.emp_id}, Name: {self.name}, Salary: {self.salary}, Added On: {self.added_on}"

# -------------------- Load Existing Employees --------------------
try:
    with open("employees.json", "r") as f:
        data = json.load(f)
        employees = {k: Employee(v["name"], v["salary"], v["emp_id"], v.get("added_on"), v.get("updated_on")) for k, v in data.items()}
except (FileNotFoundError, json.JSONDecodeError):
    employees = {}

# -------------------- Main Menu Loop --------------------
while True:
    print("\n----- Employee Management System -----")
    print("1. Add Employee")
    print("2. View All Employees")
    print("3. Update Employee Salary")
    print("4. Remove Employee")
    print("5. Exit")

    choice = input("Enter your choice: ").strip()

    # --------------- Add Employee ---------------
    if choice == '1':
        emp_id = input("Enter Employee ID: ").strip().lower()
        if emp_id in employees:
            print("Employee ID already exists.")
            continue

        name = input("Enter Employee Name: ").strip().capitalize()
        try:
            salary = float(input("Enter Salary: "))
            if salary <= 0:
                print("Salary must be greater than 0.")
                continue
        except ValueError:
            print("Invalid input! Salary must be a number.")
            continue

        employees[emp_id] = Employee(name, salary, emp_id)
        try:
            with open("employees.json", "w") as f:
                json.dump({k: vars(v) for k, v in employees.items()}, f, indent=4)
        except Exception as e:
            print(f"Error saving file: {e}")
        print("✅ Employee added successfully!")

    # --------------- View Employees ---------------
    elif choice == '2':
        d = input("Enter management password (or 'c' to go back): ").strip()
        if d == '1234':
            if not employees:
                print("No employees found.")
            else:
                print("\nEmployee List:")
                for emp in employees.values():
                    emp.show_details()
        elif d.lower() == 'c':
            print("Returning to main menu...")
            continue
        else:
            print("Wrong password.")

    # --------------- Update Salary ---------------
    elif choice == '3':
        d = input("Enter management password (or 'c' to go back): ").strip()
        if d == '1234':
            emp_id = input("Enter Employee ID to update: ").strip().lower()
            emp = employees.get(emp_id)
            if emp:
                try:
                    new_salary = float(input(f"Enter new salary for {emp.name}: "))
                    emp.salary = new_salary
                    emp.updated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("employees.json", "w") as f:
                        json.dump({k: vars(v) for k, v in employees.items()}, f, indent=4)
                    print("✅ Salary updated successfully!")
                except ValueError:
                    print("Invalid input! Salary must be a number.")
            else:
                print("Employee not found.")
        elif d.lower() == 'c':
            print("Returning to main menu...")
            continue
        else:
            print("Wrong password.")

    # --------------- Remove Employee ---------------
    elif choice == '4':
        d = input("Enter management password (or 'c' to go back): ").strip()
        if d == '1234':
            if not employees:
                print("No employees found.")
            else:
                emp_id = input("Enter Employee ID to remove: ").strip().lower()
                emp = employees.get(emp_id)
                if emp:
                    print("\nEmployee Details:")
                    emp.show_details()
                    confirm = input("Type 'y' to confirm deletion: ").strip().lower()
                    if confirm == 'y':
                        del employees[emp_id]
                        with open("employees.json", "w") as f:
                            json.dump({k: vars(v) for k, v in employees.items()}, f, indent=4)
                        print("🗑 Employee deleted successfully.")
                    else:
                        print("❎ Deletion cancelled.")
                else:
                    print("Employee not found.")
        elif d.lower() == 'c':
            print("Returning to main menu...")
            continue
        else:
            print("Wrong password.")

    # --------------- Exit Program ---------------
    elif choice == '5':
        print(" Saving data and exiting...")
        try:
            with open("employees.json", "w") as f:
                json.dump({k: vars(v) for k, v in employees.items()}, f, indent=4)
        except Exception as e:
            print(f"Error saving file: {e}")
        print("👋 Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")
