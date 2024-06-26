
import unittest
from fetch_and_insert_mail import fetch_mail_from_gmail, insert_mail
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_TYPE
from database_op import DatabaseUtils
from models import EmailData


class TestMailOps(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("Setting up test...")
        self.session = DatabaseUtils().build_conn_obj(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_TYPE)

    @classmethod
    def tearDownClass(self):
        print("Tearing down test...")


    def test_mail_being_fetched_from_api(self):
        self.assertEqual(len(fetch_mail_from_gmail()), 10)

    def test_insert_mail_into_db(self):
        self.assertEqual(insert_mail(self.session, {}), True)


if __name__ == '__main__':
    unittest.main()