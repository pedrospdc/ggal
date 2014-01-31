from django.template import Template, Context
from django.conf import settings

import os
import subprocess


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'etc')
DATABASE_FILE = os.path.join(BASE_DIR, 'gal', 'db.py')
SETUP_LOCK = os.path.join(BASE_DIR, '.setup')

settings.configure()


def render_template(template_name, context):
    with open(os.path.join(TEMPLATE_DIR, template_name)) as f:
        template = Template(f.read())
        context = Context(context)
        return template.render(context)


def install_requirements():
    install_input = raw_input('Do you want do install the requirements? [y/n]: ')
    if install_input == 'y':
        subprocess.call(('pip', 'install', '-r', 'requirements.txt'))
    elif install_input == 'n':
        return
    else:
        print 'Please type y or n\n'
        install_input()


def sync_db():
    subprocess.call(('python', 'manage.py', 'syncdb'))
    subprocess.call(('python', 'manage.py', 'migrate'))


def setup_db():
    def setup_mysql():
        db_name = raw_input('Type in the database name. [gal]: ') or 'gal'
        db_user = raw_input('Type in the database username. [root]: ') or 'root'
        db_password = raw_input('Type in the database password. [root]: ') or 'root'
        db_host = raw_input('Type in the database host. [localhost]: ') or 'localhost'
        db_port = raw_input('Type in the database port. [3306]: ') or '3306'

        template = render_template('mysql_template.html', locals())
        write_database_file(DATABASE_FILE, template)

    def setup_sqlite():
        context = {}
        db_file = raw_input('Type in which the database filename. [db.sqlite3]: ')
        context.update(db_file=db_file or 'db.sqlite3')

        template = render_template('sqlite_template.html', context)
        write_database_file(DATABASE_FILE, template)

    def write_database_file(file_, template):
        print 'Creating database file... (%s) ' % file_

        with open(file_, 'wb') as f:
            f.write(template)

    db_choice = raw_input('Which DB you want to use? [mysql/sqlite]: ')
    if db_choice == 'mysql':
        setup_mysql()
    elif db_choice == 'sqlite':
        setup_sqlite()
    else:
        print 'Please type mysql or sqlite\n'
        setup_db()


def lock():
    with file(SETUP_LOCK, 'a'):
        os.utime(SETUP_LOCK, None)

if not os.path.exists(SETUP_LOCK):
    install_requirements()
    setup_db()
    sync_db()
    lock()

subprocess.call(('python', 'manage.py', 'runserver'))