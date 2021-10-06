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
    """
    Query course details
    """
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
    """
    Generate list of courses and sub-structures
    """
    def name(self) -> Text:
        return "action_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection("./uts.db")

        slot_value = tracker.get_slot("type")
        slot_code = tracker.get_slot("code")
        slot_name = tracker.get_slot("name")

        # Check for variations of slot code
        if slot_code is not None:
            slot_code = DbQueryingMethods.check_code(slot_code)

        # Check for course variations
        if slot_value == 'course':
            slot_value = 'courses'

        # List all courses or sub_structures
        if slot_code == None and slot_name == None:
            cur = conn.cursor()
            cur.execute('SELECT * FROM {}'.format(str(slot_value)))
            #cur.execute("SELECT * FROM ?", (str(slot_value),))
            rows = cur.fetchall()
        # Or list all majors, subjects, streams, choice blocks or sub-majors | courses by name
        else:
            # Filter courses by course name
            if slot_value == 'courses':
                rows = DbQueryingMethods.select_by_slot(conn, slot_value, 'name', slot_name)
            else:
                if slot_name == None:
                    rows = DbQueryingMethods.select_by_slot(conn, 'sub_structures', 'type', slot_code)
                else:
                    rows = DbQueryingMethods.select_by_multiple_slot(conn, 'sub_structures', 'type', 'name', slot_name, slot_code)
                    
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            for row in rows:
                dispatcher.utter_message('{} {}'.format(row[0], row[1]))

        return        

class ActionHonours(Action):
    """
    Retrieve whether course is a honours degree
    """
    def name(self) -> Text:
        return "action_hons"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = DbQueryingMethods.create_connection("./uts.db")

        slot_code = tracker.get_slot("code")
        slot_name = tracker.get_slot("name")

        if slot_name == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'course_id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            for row in rows:
                if row[3] == 0:
                    dispatcher.utter_message("{} {} is not a honours degree.".format(row[0], row[1]))
                elif row[3] == 1:
                    dispatcher.utter_message("{} {} is a honours degree.".format(row[0], row[1]))
        
        return

class ActionProfPrac(Action):
    """
    Retrieve whether course offers a diploma in professional practice
    """
    def name(self) -> Text:
        return "action_prof_prac"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = DbQueryingMethods.create_connection("./uts.db")

        slot_code = tracker.get_slot("code")
        slot_name = tracker.get_slot("name")

        if slot_name == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'course_id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            for row in rows:
                if row[4] == 0:
                    dispatcher.utter_message("{} {} does not come with a Diploma in Professional Practice.".format(row[0], row[1]))
                elif row[4] == 1:
                    dispatcher.utter_message("{} {} comes with a Diploma in Professional Practice.".format(row[0], row[1]))
        
        return

class ActionCombined(Action):
    """
    Retrieve whether course is a combined degree
    """
    def name(self) -> Text:
        return "action_combined"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = DbQueryingMethods.create_connection("./uts.db")

        slot_code = tracker.get_slot("code")
        slot_name = tracker.get_slot("name")

        if slot_name == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'course_id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            for row in rows:
                if row[5] == 0:
                    dispatcher.utter_message("{} {} is not a combined degree.".format(row[0], row[1]))
                elif row[5] == 1:
                    dispatcher.utter_message("{} {} is a combined degree.".format(row[0], row[1]))

        return

class ActionCreditPoints(Action):
    def name(self) -> Text:
        return "action_credit_points"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = DbQueryingMethods.create_connection("./uts.db")
        
        slot_code = tracker.get_slot("code")
        slot_name = tracker.get_slot("name")

        if slot_name == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'sub_structures', 'struc_id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'sub_structures', 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            for row in rows:
                if not row[3]:
                    dispatcher.utter_message("{} {} does not have any specified credit points.".format(row[0], row[1]))
                else:
                    dispatcher.utter_message("{} {} is worth {} credit points.".format(row[0], row[1], row[3]))

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
    """
    Link URL for course fees
    """
    def name(self) -> Text:
        return "action_fees"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        url = 'https://cis.uts.edu.au/fees/course-fees.cfm'

        dispatcher.utter_message('For fee details please visit {}.'.format(url))
        
        return

class ActionAtar(Action):
    """
    Retrieve ATAR requirements of course
    """
    def name(self) -> Text:
        return "action_atar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection("./uts.db")

        slot_code = tracker.get_slot("code")
        slot_name = tracker.get_slot("name")

        if slot_name == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'course_id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            for row in rows:
                if not row[2]:
                    dispatcher.utter_message("There is no ATAR cutoff for {} {}.".format(row[0], row[1]))
                else:
                    dispatcher.utter_message("The ATAR cutoff for {} {} is {}.".format(row[0], row[1], row[2]))
                    #print(f"The ATAR cutoff for {row[0]} {row[1]} is {row[2]}.")
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

    def check_code(value):

        if value.lower() == 'subject' or value.lower() == 'subjects':
            value = 'sbj'
        elif value.lower() == 'major' or value.lower() == 'majors':
            value = 'maj'
        elif value.lower() == 'submajor' or value.lower() == 'submajors' or value.lower() == 'sub-major' or value.lower() == 'sub-majors':
            value = 'smj'
        elif value.lower() == 'stream' or value.lower() == 'streams':
            value = 'stm'
        elif value.lower() == 'choice block' or value.lower() == 'choice blocks':
            value = 'cbk'

        return value

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

    def select_by_slot(conn, table, slot_name, slot_value):
        """
        Query all rows by slot
        :param conn: the Connection object
        :return:
        """

        if slot_value == 'sbj':
            cur = conn.cursor()
            cur.execute("SELECT * FROM "+table+" WHERE ifnull("+slot_name+",'') = ''")
        else:
            cur = conn.cursor()
            cur.execute("SELECT * FROM "+table+" WHERE "+slot_name+" LIKE ?", ('%'+slot_value+'%',))

        rows = cur.fetchall()
        return(rows)

    def select_by_multiple_slot(conn, table, slot_name1, slot_name2, slot_code, slot_value):
        """
        Query all rows by slot
        :param conn: the Connection object
        :return:
        """

        if slot_value == 'sbj':
            cur = conn.cursor()
            cur.execute("SELECT * FROM "+table+" WHERE ifnull("+slot_name1+",'') = '' AND "+slot_name2+" LIKE ?", ('%'+slot_code+'%',))
        else:
            cur = conn.cursor()
            cur.execute("SELECT * FROM "+table+" WHERE "+slot_name1+" LIKE ? AND "+slot_name2+" LIKE ?", ('%'+slot_value+'%','%'+slot_code+'%',))

        rows = cur.fetchall()
        return(rows)

