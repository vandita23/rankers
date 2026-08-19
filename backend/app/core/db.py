import psycopg2
from psycopg2.extras import RealDictCursor

from app.core.config import DATABASE_URL


def get_connection():
    """Create a new PostgreSQL connection."""
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured.")

    return psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor,
    )


def query(
    sql: str,
    params: tuple | None = None,
    *,
    fetch_one: bool = False,
    fetch_all: bool = True,
):
    """
    Execute a SQL query.

    Kept as the main database helper because the existing services
    use this function.
    """
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)

            result = None

            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()

        connection.commit()
        return result

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def execute_query(
    sql: str,
    params: tuple | None = None,
    *,
    fetch_one: bool = False,
    fetch_all: bool = False,
):
    """
    Generic database helper for new code.

    Kept separately so we can use explicit behavior when adding
    new database operations.
    """
    return query(
        sql,
        params,
        fetch_one=fetch_one,
        fetch_all=fetch_all,
    )