"""
Django command to wait for database to be available
"""
import time

from psycopg2 import OperationalError as Psycopg2OPError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("Waiting for database...")
        db_up = False
        while not db_up:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OPError, OperationalError):
                self.stdout.write(
                    self.style.WARNING(
                        "Database unavailable. Waiting 1 second..."
                    )
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
