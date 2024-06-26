DB_USER = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'email_db'
DB_TYPE = 'mysql'
FILE_NAME = 'rules.json'


OPERATOR_MAPPING = {
    'equal to': '__eq__',  
    'not equal to': '__ne__',  
    'is less than': '__lt__',  
    'is less than equal to': '__le__', 
    'is greater than': '__gt__', 
    'is greater than equal to': '__ge__', 
    'contains': 'icontains',
    'does not contains': 'notilike'

}