from fabric.api import run, env
from fabric.context_managers import settings

env.use_ssh_config = True

def _get_manage_dot_py(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'

def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{host}'):
        run(f'{manage_dot_py} flush --noinput')

def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    print("creating session on server")
    print(f'Host = {host}')
    with settings(host_string=f'{host}'):
        session_key = run(f'{manage_dot_py} create_session {email}')
        return session_key.strip()
