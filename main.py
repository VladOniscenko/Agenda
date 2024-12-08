from src.agenda.agenda import Agenda  # Import the class explicitly
import sys
import os


def main():
    agenda = Agenda()
    agenda.create_task('vlad', 'ahahhaha')
    print(agenda)

if __name__ == '__main__':
    main()