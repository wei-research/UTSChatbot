# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sqlite3
from sqlite3 import Error

class QueryCourseName(Action):

    def name(self) -> Text:
        return "query_course_name"  #name of action

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = create_connection("../uts.db")

        slot_value = tracker.get_slot("code")   #get slot value?
        #slot_name = "name" #if using name column in courses
        get_query_results = select_course(conn, slot_value)
        dispatcher.utter_message(text=get_query_results)

        return []

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_course(conn, value):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses WHERE name LIKE ?", ('%'+value+'%',))
    #cur.execute(f"""SELECT * FROM courses WHERE name='{value}'"""") #sample fstring

    rows = cur.fetchall()

    for row in rows:
        #print(row) #print all rows from database
        return[print(f"UTS offers {row[1]} at {row[6]}.")]

