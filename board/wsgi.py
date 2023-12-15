
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board.settings')

application = get_wsgi_application()


# Custom server setup (if not using Gunicorn)
from django.core.servers.basehttp import get_internal_wsgi_application
import os

if __name__ == "__main__":
    from django.core.management.commands.runserver import Command as runserver
    runserver.default_port = os.environ.get('PORT', '8000')

