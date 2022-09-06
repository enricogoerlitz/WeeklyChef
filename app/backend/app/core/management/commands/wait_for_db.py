"""
Django command to wait for database to be available
"""
import time

from psycopg2 import OperationalError as Psycopg2OPError  # type: ignore

from django.db.utils import OperationalError
from django.db.backends.utils import CursorWrapper
from django.db import connections
from django.core.management.base import BaseCommand

from core.utils import db_query


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("Waiting for database...")
        db_connection = connections["default"]
        db_up = False
        while not db_up:
            try:
                self.check(databases=["default"])
                db_cursor = db_connection.cursor()
                self._execute_insert_db_query(db_cursor)
                db_up = True
            except (Psycopg2OPError, OperationalError):
                self.stdout.write(
                    self.style.WARNING(
                        "Database unavailable. Waiting 1 second..."
                    )
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
    
    def _execute_insert_db_query(self, cursor: CursorWrapper):
        """Executes the create table sql statement"""
        self.stdout.write("Execute insert table query.")
        cursor.execute(db_query.create_table_query)
        self.stdout.write("Finished insert table query.")