# manage.py
from flask.ext.script import Manager

from trans import app
manager = Manager(app)

@manager.command
def hello():
    print "hello"

if __name__ == "__main__":
    manager.run()
