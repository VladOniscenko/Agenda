from controllers.agenda_controller import AgendaController  # Import the class explicitly
import sys
import os


def main():
    agenda = AgendaController()

    box_w = 20

    methods = {
        1: agenda.create_task
    }

    actions = [
        '1: Create task',
        # '2: Read task',
        # '3: Update task',
        # '4: Delete task'
    ]

    inputs = {
        1: ['title', 'description']
    }

    while True:
        print('+' + '-' * box_w + '+')
        print('|' + 'Actions:'.center(box_w) + '|')
        print('+' + '-' * box_w + '+')

        for act in actions:
            print('|' + f'{act}'.center(box_w) + '|')
            print('+' + '-' * box_w + '+')

        try:
            action = int(input('Select action: '))
        except ValueError as e:
            print(f'Invalid input:')
            continue

        func = methods.get(action)
        if not func:
            print('Action not found!')
            continue

        required_inputs = inputs.get(action)
        func(*[input(f'Input {x}: ') for x in required_inputs])

if __name__ == '__main__':
    main()