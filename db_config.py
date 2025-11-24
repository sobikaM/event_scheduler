import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sobika@52',
    'database': 'event'
}


def _init_db_tables():
    """Create required tables if they don't exist (safe to call multiple times)."""
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        if getattr(err, 'errno', None) == errorcode.ER_BAD_DB_ERROR:
            try:
                tmp_cfg = DB_CONFIG.copy()
                tmp_cfg.pop('database', None)
                cnx = mysql.connector.connect(**tmp_cfg)
                cur = cnx.cursor()
                cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
                cnx.commit()
                cur.close()
                cnx.close()
                cnx = mysql.connector.connect(**DB_CONFIG)
            except Exception:
                return
        else:
            return

    cur = cnx.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Event (
        event_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        start_time DATETIME NOT NULL,
        end_time DATETIME NOT NULL,
        description TEXT
    ) ENGINE=InnoDB;
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Resource (
        resource_id INT AUTO_INCREMENT PRIMARY KEY,
        resource_name VARCHAR(255) NOT NULL,
        resource_type VARCHAR(100) NOT NULL
    ) ENGINE=InnoDB;
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS EventResourceAllocation (
        allocation_id INT AUTO_INCREMENT PRIMARY KEY,
        event_id INT NOT NULL,
        resource_id INT NOT NULL,
        FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE,
        FOREIGN KEY (resource_id) REFERENCES Resource(resource_id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    cnx.commit()
    cur.close()
    cnx.close()


def get_db():
    try:
        _init_db_tables()
    except Exception:
        pass

    return mysql.connector.connect(**DB_CONFIG)