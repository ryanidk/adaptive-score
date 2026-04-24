"""
Database utility functions
ICS3U-01
Ryan
This file represents the utility functions used to access and modify the database for Adaptive Score
Last modified: Apr 24, 2026
"""

import sqlite3

from flask import current_app, g


def get_db():
    """
    Gets the database. g represents the global context

    Returns:
        db (sqlite3): The sqlite3 database
    """

    # If the database has not been loaded into the global context, connect to it
    if "db" not in g:
        g.db = sqlite3.connect(
            "sqlite_db", detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    # Return the database
    return g.db


def close_db():
    """
    Closes the database and removes it from the global context
    """

    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """
    Initializes the database by executing the schema script in sqlite_db
    """

    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def init_db_command(app):
    """
    Runs the init_db() function with app context.

    Args:
        app (Flask): The app
    """

    with app.app_context():
        init_db()
        print("Initialized the database")


def init_app(app):
    """
    Initialization command for the app, tears down the app context.

    Args:
        app (flask): The app
    """

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
