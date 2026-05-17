from database.db import connect_db

def create_user(name, email, password, role):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users(name,email,password,role)
    VALUES(?,?,?,?)
    """, (name, email, password, role))

    conn.commit()
    conn.close()

