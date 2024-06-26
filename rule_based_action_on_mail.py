from datetime import datetime, timedelta
from dateutil import relativedelta
from mail_ops import FileManager, GmailOps
from database_op import DatabaseUtils
from models import EmailData
from sqlalchemy import and_, or_
from config import OPERATOR_MAPPING, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_TYPE, FILE_NAME


def fetch_mails(query_obj, session):
    try:
        print(query_obj)
        query_obj = query_obj.all()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return query_obj

def update_mail_data(session, message_ids, update_actions):
    try:
        session.query(EmailData).filter(EmailData.message_id.in_(message_ids)).update(update_actions)
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

def process_actions(actions, update_actions, query):
    mail_obj = GmailOps()
    mail_obj.build_service_obj()

    for action in actions:
        if action == 'move':
            update_actions['folder'] = actions[action]
            for message_data in query:
                email_data = mail_obj.move_email_to_folder('me', message_data.message_id, actions['move'])

        if action == 'mark' and actions.get('mark') == 'read':
            update_actions['is_read'] = 1
            for message_data in query:
                mail_obj.mark_as_read('me', message_data.message_id)

        elif actions.get(action) == 'unread':
            update_actions['is_read'] = 0
            for message_data in query:
                mail_obj.mark_as_unread('me', message_data.message_id)
    return update_actions

def build_query_with_conditions(query, rule, conditions, filters):

    for condition in conditions:
        field = condition.get('field')
        operator = condition.get('operator')
        value = condition.get('value')
        unit = condition.get('unit')

        if field and OPERATOR_MAPPING.get(operator) and value:
            if field in ['received_date']:
                today = datetime.now()
                value = today - timedelta(days=int(value)) if unit == 'day' else today - relativedelta.relativedelta(months=int(value))
            build_filter = getattr(getattr(EmailData, field), OPERATOR_MAPPING.get(operator))(value)
            filters.append(build_filter)

    if rule.get('conditions_satisfied') == 'all':
        query = query.filter(and_(*filters))
    else:
        query = query.filter(or_(*filters))

    return query

def process_rules(rules, session):
    query = session.query(EmailData.message_id)
    filters = []
    
    for rule in rules:
        conditions = rule.get('conditions')
        query = build_query_with_conditions(query, rule, conditions, filters)
        query = fetch_mails(query, session)
        actions = rule.get('actions')
        update_actions = {'is_processed': 1}
        message_ids =[message_data.message_id for message_data in query]
        update_actions = process_actions(actions, update_actions, query)
        update_mail_data(session, message_ids, update_actions)

def main():
    fm = FileManager(FILE_NAME)
    rules = fm.load_file()
    if not rules:
        print('no rules found cannot process further')
        exit()

    db_utils = DatabaseUtils()
    session = db_utils.build_conn_obj(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_TYPE)
    process_rules(rules, session)


if __name__ == "__main__":
    main()