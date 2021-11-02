# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import sqlite3
from sqlite3 import Error
from fuzzywuzzy import process

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
            slot_code = check_code(slot_code)

        # Check for course variations
        if slot_value is not None:
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
            dispatcher.utter_message("Here are your results!")
            for row in rows:
                dispatcher.utter_message('{} {}'.format(row[0], row[1]))
            dispatcher.utter_message("Please respond with the correct code.")
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
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            if slot_name == None:
                dispatcher.utter_message("Here are results for {}".format(slot_code))
            elif slot_code == None:
                dispatcher.utter_message("Here are results for {}".format(slot_name))
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
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            if slot_name == None:
                dispatcher.utter_message("Here are results for {}".format(slot_code))
            elif slot_code == None:
                dispatcher.utter_message("Here are results for {}".format(slot_name))
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
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            if slot_name == None:
                dispatcher.utter_message("Here are results for {}".format(slot_code))
            elif slot_code == None:
                dispatcher.utter_message("Here are results for {}".format(slot_name))
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
            rows = DbQueryingMethods.select_by_slot(conn, 'sub_structures', 'id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'sub_structures', 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            if slot_name == None:
                dispatcher.utter_message("Here are results for {}".format(slot_code))
            elif slot_code == None:
                dispatcher.utter_message("Here are results for {}".format(slot_name))
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

        slot_code = tracker.get_slot("code")
        slot_name = tracker.get_slot("name")

        # Recommended full-time study worth of credit points in a year
        full_load = 48

        if slot_name == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            if slot_name == None:
                dispatcher.utter_message("Here are results for {}".format(slot_code))
            elif slot_code == None:
                dispatcher.utter_message("Here are results for {}".format(slot_name))
            for row in rows:
                # Calculate years of full-time study
                years = round(row[7]/full_load)
                dispatcher.utter_message("{} {} has {} credit points which can be completed for {} years full time.".format(row[0], row[1], row[7], years))

        return

class ActionDetails(Action):
    def name(self) -> Text:
        return "action_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conn = DbQueryingMethods.create_connection("./uts.db")

        slot_code = tracker.get_slot("code")
        slot_name = tracker.get_slot("name")

        if slot_name == None:
            rows = DbQueryingMethods.query_tables(conn, 'id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.query_tables(conn, 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            if slot_name == None:
                dispatcher.utter_message("Here are results for {}".format(slot_code))
            elif slot_code == None:
                dispatcher.utter_message("Here are results for {}".format(slot_name))
            for row in rows:
                dispatcher.utter_message("{} {} is a {} at UTS. For more info, visit {}.".format(row[0], row[1], get_type(row[0]), get_url(row[0])))

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
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_by_slot(conn, 'courses', 'name', slot_name)
        
        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            if slot_name == None:
                dispatcher.utter_message("Here are results for {}".format(slot_code))
            elif slot_code == None:
                dispatcher.utter_message("Here are results for {}".format(slot_name))
            for row in rows:
                if not row[2]:
                    dispatcher.utter_message("There is no ATAR cutoff for {} {}.".format(row[0], row[1]))
                else:
                    dispatcher.utter_message("The ATAR cutoff for {} {} is {}.".format(row[0], row[1], row[2]))
                    #print(f"The ATAR cutoff for {row[0]} {row[1]} is {row[2]}.")
        return

class ActionChildren(Action):
    """
    Retrieve sub_structures under a course
    """
    def name(self) -> Text:
        return "action_children"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection("./uts.db")

        slot_code = tracker.get_slot("code")
        slot_name = tracker.get_slot("name")

        if slot_name == None:
            rows = DbQueryingMethods.select_children(conn, 'id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_children(conn, 'name', slot_name)

        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            if slot_name == None:
                dispatcher.utter_message("Here are children results for {}".format(slot_code))
            elif slot_code == None:
                dispatcher.utter_message("Here are children results for {}".format(slot_name))
            for row in rows:
                dispatcher.utter_message("{} {}".format(row[0], row[1]))
            dispatcher.utter_message("Feel free to learn more by responding with code.")
        return

class ActionParent(Action):
    """
    Retrieve courses from sub_structure
    """
    def name(self) -> Text:
        return "action_parent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection("./uts.db")

        slot_code = tracker.get_slot("code")
        slot_name = tracker.get_slot("name")

        if slot_name == None:
            rows = DbQueryingMethods.select_parent(conn, 'id', slot_code)
        elif slot_code == None:
            rows = DbQueryingMethods.select_parent(conn, 'name', slot_name)

        if len(list(rows)) < 1:
            dispatcher.utter_message("There are no matches for your query.")
        else:
            if slot_name == None:
                dispatcher.utter_message("Here are course results for {}".format(slot_code))
            elif slot_code == None:
                dispatcher.utter_message("Here are course results for {}".format(slot_name))
            for row in rows:
                dispatcher.utter_message("{} {}".format(row[0], row[1]))
            dispatcher.utter_message("Feel free to learn more by responding with code.")
        return

class ResetSlot(Action):
    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("name",None), SlotSet("code",None), SlotSet("type",None)]
####################################################################################################################################################
# Database query functions
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
    
    def query_tables(conn, field, value):
        """
        Query courses and sub_structure tables
        :param conn: the Connection object
        :param priority:
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM courses WHERE "+field+" LIKE ? UNION SELECT id, name FROM sub_structures WHERE "+field+" LIKE ?", ('%'+value+'%','%'+value+'%',))

        rows = cur.fetchall()
        return(rows)

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

    def select_children(conn, field, value):
        cur = conn.cursor()
        cur.execute("SELECT * FROM sub_structures WHERE id IN (SELECT struc_id FROM relations WHERE course_id IN (SELECT id FROM courses WHERE "+field+" LIKE ?))", ('%'+value+'%',))
        rows = cur.fetchall()
        return(rows)

    def select_parent(conn, field, value):
        cur = conn.cursor()
        cur.execute("SELECT * FROM courses WHERE id IN (SELECT course_id FROM relations WHERE struc_id IN (SELECT id FROM sub_structures WHERE "+field+" LIKE ?))", ('%'+value+'%',))
        rows = cur.fetchall()
        return(rows)

####################################################################################################################################################
# Helper functions

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

def get_type(x):
    if 'cbk' in x:
        return "choice block"
    elif 'smj' in x:
        return "sub-major"
    elif 'maj' in x:
        return "major"
    elif 'stm' in x:
        return "stream"
    elif 'c0' in x:
        return "course"
    elif 'c1' in x:
        return "course"
    else:
        return "subject"

def check_type(x):
    if 'cbk' in x:
        return "Directory"
    elif 'smj' in x:
        return "Directory"
    elif 'maj' in x:
        return "Directory"
    elif 'stm' in x:
        return "Directory"
    elif 'c0' in x:
        return "Course"
    elif 'c1' in x:
        return "Course"
    else:
        return "Subject"

def get_url(x):
    head_url = 'https://handbook.uts.edu.au/'
    
    if check_type(x) == 'Directory':
        return head_url + 'directory/' + x + '.html'
    elif check_type(x) == 'Course':
        return head_url + 'courses/' + x + '.html'
    elif check_type(x) == 'Subject':
        return head_url + 'subjects/' + x + '.html'
    else:
        return 'No URL found'

