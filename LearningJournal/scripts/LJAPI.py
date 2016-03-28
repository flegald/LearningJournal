# coding=utf-8
import os
import requests
import transaction


from LearningJournal.models import Entry
from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


database_url = os.environ.get('DATABASE_URL', None)
engine = engine_from_config({'sqlalchemy.url': database_url})
DBSession.configure(bind=engine)

json_entries = {}


def get_json():
    """Get and store journal json data."""
    resp = requests.get('https://sea401d2.crisewing.com/api/export?apikey=' + os.environ.get('API_KEY'))

    if resp.status_code == 200:
        json_entries = resp.json()
        return json_entries
    else:
        return None


def search_and_create(new_title, new_text):
    """See if entries already exist, then add to DB."""
    try:
        in_db = DBSession.query(Entry).filter(Entry.title == new_title)
        DBSession.query(Entry).filter(Entry.id == in_db.id).update({'title': new_title, "text": new_title})
        return True
    except AttributeError:
        new_entry = Entry(title=new_title, text=new_text)
        DBSession.add(new_entry)
        return False

def add_to_db(json):
    """Commit all json dict to DB."""
    for entry in json:
        search_and_create(entry['title'], entry['text'])
        transaction.commit()


if __name__ == "__main__":
    json = get_json()
    add_to_db(json)
