import os
from datetime import datetime, date

# Set file paths for user.txt, tasks.txt, task_overview.txt, and user_overview.txt
USER_FILE_PATH = "C:/Users/Ilie Corcodel/OneDrive/Documents/HYPERIONDEV SE BOOTHCAMP WORK/TASK 17/user.txt"
TASKS_FILE_PATH = "C:/Users/Ilie Corcodel/OneDrive/Documents/HYPERIONDEV SE BOOTHCAMP WORK/TASK 17/tasks.txt"
TASK_OVERVIEW_FILE = "C:/Users/Ilie Corcodel/OneDrive/Documents/HYPERIONDEV SE BOOTHCAMP WORK/TASK 17/task_overview.txt"
USER_OVERVIEW_FILE = "C:/Users/Ilie Corcodel/OneDrive/Documents/HYPERIONDEV SE BOOTHCAMP WORK/TASK 17/user_overview.txt"

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to load tasks from file
def load_tasks():
    with open(TASKS_FILE_PATH, 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t.strip()]  # Remove empty lines
    
    task_list = []
    for t_str in task_data:
        task_components = t_str.split(";")
        curr_t = {
            'username': task_components[0],
            'title': task_components[1],
            'description': task_components[2],
            'due_date': datetime.strptime(task_components[3], DATETIME_STRING_FORMAT).date(),
            'assigned_date': datetime.strptime(task_components[4], DATETIME_STRING_FORMAT).date(),
            'completed': task_components[5] == "Yes"
        }
        task_list.append(curr_t)
    
    return task_list

# Function to save tasks to file
def save_tasks(task_list):
    with open(TASKS_FILE_PATH, "w") as task_file:
        for t in task_list:
            task_str = ";".join([
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ])
            task_file.write(task_str + "\n")

# Load tasks
task_list = load_tasks()

# User login
def login():
    print("LOGIN")
    while True:
        username = input("Username: ")
        password = input("Password: ")
        with open(USER_FILE_PATH, 'r') as user_file:
            for line in user_file:
                # Skip empty lines or improperly formatted lines
                if not line.strip() or ';' not in line:
                    print("Warning: Ignoring improperly formatted line in user.txt")
                    continue
                
                stored_username, stored_password = line.strip().split(';')
                if username == stored_username and password == stored_password:
                    print("Login Successful!")
                    return username, task_list  # Return task_list along with username
            print("Username or password is incorrect. Please try again.")

# Main menu
def main_menu(curr_user, task_list):
    while True:
        print("\nSelect one of the following Options below:")
        print("r - Registering a user")
        print("a - Adding a task")
        print("va - View all tasks")
        print("vm - View my tasks")
        print("ds - Display statistics")
        print("gr - Generate report")
        print("e - Exit")
        choice = input(": ").lower()

        if choice == 'r':
            register_user()
        elif choice == 'a':
            add_task(curr_user)
        elif choice == 'va':
            view_all_tasks()
        elif choice == 'vm':
            view_my_tasks(curr_user)
        elif choice == 'ds':
            display_statistics(task_list)
        elif choice == 'gr':
            generate_reports(task_list)
        elif choice == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("You have made a wrong choice, Please Try again")

# Register user
def register_user():
    new_username = input("Enter new username: ")
    new_password = input("Enter new password: ")
    with open(USER_FILE_PATH, "a") as user_file:
        user_file.write(f"{new_username};{new_password}\n")
    print("User registered successfully!")

# Add task
def add_task(curr_user):
    task_username = input("Name of person assigned to task: ")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    task_due_date = input("Due date of task (YYYY-MM-DD): ")
    due_date = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT).date()
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    save_tasks(task_list)
    print("Task successfully added.")

# View all tasks
def view_all_tasks():
    for i, task in enumerate(task_list, start=1):
        print(f"Task {i}:")
        print_task(task)

# View tasks assigned to current user
def view_my_tasks(curr_user):
    for i, task in enumerate(task_list, start=1):
        if task['username'] == curr_user:
            print(f"Task {i}:")
            print_task(task)

# Print task details
def print_task(task):
    print(f"Title: {task['title']}")
    print(f"Assigned to: {task['username']}")
    print(f"Date Assigned: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Description: {task['description']}")
    print(f"Completed: {'Yes' if task['completed'] else 'No'}")

# Display statistics
def display_statistics(task_list):
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < date.today())
    
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks != 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks != 0 else 0

    print("=== Task Statistics ===")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Incomplete tasks: {incomplete_tasks}")
    print(f"Overdue tasks: {overdue_tasks}")
    print(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%")
    print(f"Percentage of overdue tasks: {overdue_percentage:.2f}%")

# Generate reports
def generate_reports(task_list):
    generate_task_report(task_list)
    generate_user_report(task_list)

# Generate task report
def generate_task_report(task_list):
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100

    today = date.today()
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < today)
    overdue_percentage = (overdue_tasks / total_tasks) * 100

    print("Task Overview:")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Uncompleted tasks: {uncompleted_tasks}")
    print(f"Total tasks overdue: {overdue_tasks}")
    print(f"Percentage of incomplete tasks: {incomplete_percentage}%")
    print(f"Percentage of tasks overdue: {overdue_percentage}%")

    # Write to task overview file
    with open(TASK_OVERVIEW_FILE, "w") as task_overview_file:
        task_overview_file.write("Task Overview:\n")
        task_overview_file.write(f"Total tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Total tasks overdue: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of incomplete tasks: {incomplete_percentage}%\n")
        task_overview_file.write(f"Percentage of tasks overdue: {overdue_percentage}%\n")

# Generate user report
def generate_user_report(task_list):
    user_tasks = {}
    for task in task_list:
        username = task['username']
        if username not in user_tasks:
            user_tasks[username] = {'total': 0, 'completed': 0, 'overdue': 0}
        user_tasks[username]['total'] += 1
        if task['completed']:
            user_tasks[username]['completed'] += 1
        elif task['due_date'] < date.today():
            user_tasks[username]['overdue'] += 1
    
    with open(USER_OVERVIEW_FILE, "w") as user_overview_file:
        user_overview_file.write("User Overview:\n")
        user_overview_file.write(f"Total users: {len(user_tasks)}\n")
        for username, tasks in user_tasks.items():
            total = tasks['total']
            completed = tasks['completed']
            overdue = tasks['overdue']
            user_overview_file.write(f"\n{username}:\n")
            user_overview_file.write(f"Total tasks assigned: {total}\n")
            user_overview_file.write(f"Percentage of total tasks: {(total / len(task_list)) * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of completed tasks: {(completed / total) * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of incomplete tasks: {((total - completed) / total) * 100:.2f}%\n")
            user_overview_file.write(f"Percentage of overdue tasks: {(overdue / total) * 100:.2f}%\n")
    print("User report generated successfully!")

# Main program
def main():
    curr_user, task_list = login()  # Unpack the returned tuple into curr_user and task_list
    main_menu(curr_user, task_list)

if __name__ == "__main__":
    main()