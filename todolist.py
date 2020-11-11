from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, update
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Create database file
engine = create_engine('sqlite:///todo.db')

# Base object for table below
Base = declarative_base()

# Describe table as a class


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


# Create table in database
Base.metadata.create_all(engine)
# Open a session to access table
Session = sessionmaker(bind=engine)
session = Session()

weekdays = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}


def print_tasks(tasks):
    if not tasks:
        print("Nothing to do!")
    else:
        for index, row in enumerate(tasks):
            print(
                f"{index+1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
    print()


def get_task_input():
    task = input("Enter task\n")
    deadline = datetime.strptime(input("Enter deadline\n"), "%Y-%m-%d")
    return [task, deadline]


def add_task():
    task, deadline = get_task_input()
    new_row = Table(task=task, deadline=deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added!")
    print()


def todays_task():
    today = datetime.today()
    print(f"{today.day} {today.strftime('%b')}:")
    tasks = session.query(Table).filter(Table.deadline == today.date()).all()
    print_tasks(tasks)


def all_tasks():
    tasks = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    print_tasks(tasks)


def weeks_task():
    today = datetime.today().date()
    for i in range(7):
        current_day = today + timedelta(days=i)
        print(
            f"{weekdays[current_day.weekday()]} {current_day.day} {current_day.strftime('%b')}:")
        tasks = session.query(Table).filter(
            Table.deadline == current_day).all()
        print_tasks(tasks)


def missed_task():
    print("Missed tasks:")
    tasks = session.query(Table).filter(
        Table.deadline < datetime.today().date()).all()
    print_tasks(tasks)


def delete_task():
    print("Choose the index of the tasks you want to delete separated by space:")
    tasks = session.query(Table).all()
    print_tasks(tasks)
    indexes = [int(i) - 1 for i in input().split(" ")]
    for i in indexes:
        session.delete(tasks[i])
    session.commit()

    print(f"{len(indexes)} task(s) has been deleted!")
    print()


def update_task():
    tasks = session.query(Table).order_by(Table.deadline).all()
    if not tasks:
        print("Nothing to do!")
        print()
        return
    print("Enter the index of the task you want to edit")
    print_tasks(tasks)
    index = int(input()) - 1
    task, deadline = get_task_input()
    tasks[index].task = task
    tasks[index].deadline = deadline
    session.commit()
    print("Task updated")
    print()


while True:
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Update task\n7) Delete task\n0) Exit")
    choice = int(input())
    if choice == 1:
        todays_task()
    elif choice == 2:
        weeks_task()
    elif choice == 3:
        all_tasks()
    elif choice == 4:
        missed_task()
    elif choice == 5:
        add_task()
    elif choice == 6:
        update_task()
    elif choice == 7:
        delete_task()
    elif choice == 0:
        break
    else:
        print("Invalid choice - try again.")
print("Bye!")
