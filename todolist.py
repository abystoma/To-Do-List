from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create database file
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

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


def add_task():
    print("Enter task")
    new_task = input()
    new_row = Table(task=new_task)
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def view_tasks():
    print("Today:")
    tasks = session.query(Table).all()
    if not tasks:
        print("Nothing to do!")
    else:
        for todo in tasks:
            print(f"{todo.id}. {todo.task}")


while True:
    print("1) Today's tasks\n2) Add task\n0) Exit")
    choice = input()
    if choice == "1":
        view_tasks()
    elif choice == "2":
        add_task()
    elif choice == "0":
        break
    else:
        print("Invalid choice - try again.")
