from Controllers.agenda_controller import AgendaController  # Import the class explicitly
from Controllers.user_controller import UserController  # Import the class explicitly

def add_task_view(response):
    task = response['task']

    print('-' * 36)
    print('Task was successfully added!')

    print('-' * 15, 'TASK', '-' * 15)
    print('Id:', task.id)
    print('Name:', task.name)
    print('Description:', task.description)
    print('Date:', task.date)
    print('Priority:', task.priority)
    print('Status:', task.status)
    print('-' * 36)

def get_tasks_view(response):
    tasks = response['tasks']
    for task in tasks:
        print('-' * 15, 'TASK', '-' * 15)
        print('Id:', task.id)
        print('Name:', task.name)
        print('Description:', task.description)
        print('Date:', task.date)
        print('Priority:', task.priority)
        print('Status:', task.status)

def get_task_view(response):
    task = response['task']
    print('-' * 15, 'TASK', '-' * 15)
    print('Id:', task.id)
    print('Name:', task.name)
    print('Description:', task.description)
    print('Date:', task.date)
    print('Priority:', task.priority)
    print('Status:', task.status)
    print('-' * 36)

def delete_task_view(response):
    print('Task successfully deleted!')

def main():
    agenda = AgendaController(USER.id)

    methods = {
        1: agenda.add_task,
        2: agenda.get_tasks,
        3: agenda.update_task,
        4: agenda.delete_task,
        9: agenda.get_task
    }

    actions = [
        '1: Create task',
        '2: Get tasks',
        '3: Update task',
        '4: Delete task',
        '9: Get task by id',
    ]

    inputs = {
        1: ['name', 'description'],
        2: [],
        3: ['name', 'description'],
        4: ['id'],
        9: ['id']
    }

    views = {
        1: add_task_view,
        2: get_tasks_view,
        # 3: update_task_view,
        4: delete_task_view,
        9: get_task_view
    }

    while True:
        print('+' + '-' * BOX_W + '+')
        print('|' + 'Actions:'.center(BOX_W) + '|')
        print('+' + '-' * BOX_W + '+')

        for act in actions:
            print('|' + f'{act}'.center(BOX_W) + '|')
            print('+' + '-' * BOX_W + '+')

        try:
            action = int(input('Select action: '))
        except ValueError as e:
            print(f'Invalid input:')
            continue

        func = methods.get(action)
        if not func:
            print('Action not found!')
            continue

        required_inputs = inputs.get(action, [])
        response = func(*[input(f'Input {x}: ') for x in required_inputs])

        if not response.get('success'):
            print(response.get('message'))
            continue

        view = views.get(action)
        if not view:
            print('Action completed!')

        view(response)

if __name__ == '__main__':
    BOX_W = 20

    get_user = UserController().get_user(1)
    if not get_user['success']:
        raise UserWarning(get_user['message'])

    USER = get_user['user']
    main()