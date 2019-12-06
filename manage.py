#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config

def main():
    settings_module = config('DJANGO_SETTINGS_MODULE', default=None)

    if sys.argv[1] == 'test':
        if settings_module:
            print("Ignoring config('DJANGO_SETTINGS_MODULE') because it's test. "
                "Using 'django_ecommerce.settings.test'")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ecommerce.settings.test')
    else:
        if settings_module is None:
            print("Unable to find DJANGO_SETTINGS_MODULE. Won't start devserver. "
                "Remember to create .env file at project root. "
                "Check README for more information.")
            sys.exit(1)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
