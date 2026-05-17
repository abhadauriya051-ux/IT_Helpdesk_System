import imaplib
import email
import sqlite3
import time
from email.utils import parseaddr

DB = "helpdesk.db"

EMAIL = "bashu6693@gmail.com"
PASSWORD = "shjtxuowiwhcwvpn"


def check_emails():

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)

    mail.select("INBOX")

    typ, messages = mail.search(None, 'UNSEEN')

    for num in messages[0].split():

        typ, data = mail.fetch(num, '(RFC822)')

        raw_email = data[0][1]

        msg = email.message_from_bytes(raw_email)

        sender_name, sender_email = parseaddr(msg["From"])

        subject = msg["Subject"]

        message_id = msg["Message-ID"]

        clean_subject = subject.replace("Re:", "").strip()

        body = ""

        if msg.is_multipart():

            for part in msg.walk():

                content_type = part.get_content_type()

                if content_type == "text/plain":

                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass

        else:

            try:
                body = msg.get_payload(decode=True).decode()
            except:
                pass

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            message TEXT,
            sender_email TEXT,
            status TEXT
        )
        """)

        cur.execute(
            "SELECT id,status FROM tickets WHERE subject=?",
            (clean_subject,)
        )

        existing_ticket = cur.fetchone()

        if existing_ticket:

            ticket_id = existing_ticket[0]

            cur.execute(
                """
                UPDATE tickets
                SET message = message || ?
                WHERE id = ?
                """,
                ("\n\n" + body, ticket_id)
            )

            print(f"Ticket Updated: {clean_subject}")

        else:

            cur.execute(
                """
                INSERT INTO tickets(subject,message,sender_email,status)
                VALUES(?,?,?,?)
                """,
                (
                    clean_subject,
                    body,
                    sender_email,
                    "Open"
                )
            )

            print(f"Ticket Created: {clean_subject}")

        conn.commit()
        conn.close()

    mail.logout()


while True:

    print("Checking new mails...")

    try:
        check_emails()
    except Exception as e:
        print("Error:", e)

    time.sleep(15)

