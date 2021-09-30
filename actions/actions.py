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
from fuzzywuzzy import process

class QueryCourseName(Action):

    def name(self) -> Text:
        return "query_course_name"  #name of action

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #result = init_code(dispatcher, tracker, domain)

        conn = DbQueryingMethods.create_connection("./uts.db")

        slot_value = tracker.get_slot("code")   #get slot value?
        #slot_name = "name" #if using name column in courses
        get_query_results = DbQueryingMethods.select_course(conn, slot_value)
        dispatcher.utter_message(text=str(get_query_results))

        return

class ActionList(Action):
    def name(self) -> Text:
        return "action_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection("./uts.db")

        slot_value = tracker.get_slot("type")
        cur = conn.cursor()
        cur.execute('SELECT * FROM {}'.format(str(slot_value)))
        #cur.execute("SELECT * FROM ?", (str(slot_value),))
        rows = cur.fetchall()

        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            for row in rows:
                dispatcher.utter_message('{} {}'.format(row[0], row[1]))

        return        

class ActionHonours(Action):
    def name(self) -> Text:
        return "action_hons"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = DbQueryingMethods.create_connection("./uts.db")
        
        return

class ActionProfPrac(Action):
    def name(self) -> Text:
        return "action_prof_prac"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = DbQueryingMethods.create_connection("./uts.db")
        
        return

class ActionCombined(Action):
    def name(self) -> Text:
        return "action_combined"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = DbQueryingMethods.create_connection("./uts.db")

        return

class ActionCreditPoints(Action):
    def name(self) -> Text:
        return "action_credit_points"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = DbQueryingMethods.create_connection("./uts.db")

        return

class ActionDuration(Action):
    def name(self) -> Text:
        return "action_duration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = DbQueryingMethods.create_connection("./uts.db")

        return

class ActionFees(Action):
    def name(self) -> Text:
        return "action_fees"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        url = 'https://cis.uts.edu.au/fees/course-fees.cfm'

        dispatcher.utter_message('For fee details please visit {}.'.format(url))
        
        return

class ActionAtar(Action):
    def name(self) -> Text:
        return "action_atar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection("./uts.db")

        slot_code = tracker.get_slot("code")
        slot_name = tracker.get_slot("name")

        if slot_name == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'course_id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            for row in rows:
                if not row[2]:
                    dispatcher.utter_message("There is no ATAR cutoff for {} {}.".format(row[0], row[1]))
                else:
                    dispatcher.utter_message("The ATAR cutoff for {} {} is {}.".format(row[0], row[1], row[2]))
                    print(f"The ATAR cutoff for {row[0]} {row[1]} is {row[2]}.")
        return

class ActionYear(Action):
    def name(self) -> Text:
        return "action_years"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class DbQueryingMethods:

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
        cur.execute("SELECT * FROM courses WHERE course_id LIKE ?", ('%'+str(value)+'%',))
        #cur.execute(f"""SELECT * FROM courses WHERE name='{value}'""") #sample fstring

        #cur.execute("SELECT * FROM courses WHERE name LIKE '%Science%'")
        rows = cur.fetchall()
        #print(rows)
        
        if len(list(rows)) < 1:
            return "There are no matches for your query."
        else:
            for row in rows:
                #return[print(f"UTS offers {row[1]} at {row[6]}.")]
                return f"UTS offers {row[1]} at {row[6]}."

    def select_all_courses(conn):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM courses")
        rows = cur.fetchall()

        if len(list(rows)) < 1:
            return "There are no matches for your query."
        else:
            for row in rows:
                return

        #for row in rows:
        #    print(row)

    def select_by_slot(conn, slot_name, slot_value):
        """
        Query all rows by slot
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM courses WHERE "+slot_name+" LIKE ?", ('%'+slot_value+'%',))

        rows = cur.fetchall()
        return(rows)

