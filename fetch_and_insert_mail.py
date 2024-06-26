from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_TYPE
from mail_ops import GmailOps
from database_op import DatabaseUtils
from models import EmailData

def fetch_mail_from_gmail():
    mail_obj = GmailOps()
    mail_obj.build_service_obj()
    email_data = mail_obj.get_messages()
    return email_data

def insert_mail(session, email_data):
    try:
        for email in email_data:
            data_obj = EmailData(**email)
            session.add(data_obj)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error occurred while inserting into database: {str(e)}")
    finally:
        session.close()
    return True

def main():
    db_utils = DatabaseUtils()
    session = db_utils.build_conn_obj(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_TYPE)
    email_data = fetch_mail_from_gmail()
    insert_mail(session, email_data)

if __name__ == "__main__":
    main()
