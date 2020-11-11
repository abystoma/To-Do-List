from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
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


def add_task():
    new_task = input("Enter task\n")
    date = datetime.strptime(input("Enter deadline\n"), "%Y-%m-%d") 
    new_row = Table(task=new_task, deadline=date)
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def todays_task():
    today = datetime.today()
    print(f"Today {today.day} {today.strftime('%b')}:")
    tasks = session.query(Table).filter(Table.deadline == today.date()).all()
    if not tasks:
        print("Nothing to do!")
    else:
        for todo in tasks:
            print(f"{todo.id}. {todo.task}")


def all_tasks():
    tasks = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    for index, row in enumerate(tasks):
        print(
            f"{index+1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")


def weeks_task():
    today = datetime.today().date()
    for i in range(7):
        current_day = today + timedelta(days=i)
        print(
            f"{weekdays[current_day.weekday()]} {current_day.day} {current_day.strftime('%b')}:")
        tasks = session.query(Table).filter(
            Table.deadline == current_day).all()
        if not tasks:
            print("Nothing to do!")
        else:
            for enum, todo in enumerate(tasks):
                print(f"{enum+1}. {todo.task}")
        print()


while True:
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit")
    choice = int(input())
    if choice == 1:
        todays_task()
    elif choice == 2:
        weeks_task()
    elif choice == 3:
        all_tasks()
    elif choice == 4:
        add_task()
    elif choice == 0:
        break
    else:
        print("Invalid choice - try again.")
print("Bye!")
