# UTS - 41030 Engineering Capstone - UTS FEIT Chatbot
41030 Engineering Capstone - Spring 2021

Project name: AI Chatbot Development  
Student: Christian Cabato (12915892)  
Major: Data Engineering  

Supervisor: [Wei Liu](https://www.uts.edu.au/staff/wei.liu)  
Co-adivsor: [Xinghao Yang](https://xinghaoyang.github.io/)  
Original chatbot repository: [UTS FEIT Chatbot](https://github.com/XinghaoYang/UTSChatbot)  

Chatbot widget source: [Chatbot Widget](https://github.com/JiteshGaikwad/Chatbot-Widget)  
Conversational AI: [Rasa](https://rasa.com/)  

Video Demonstration: [Chatbot Demonstration](https://youtu.be/7U9V1K7qq-4)  

# Description
The UTS FEIT Chatbot is a chatbot system that responds to user queries regarding courses and underlying sub-structures at the University of Technology Sydney (UTS). My primary responsibility revolves around the improvement of the data management aspects of the current [UTS FEIT Chatbot](https://github.com/XinghaoYang/UTSChatbot) and migrate its Rasa system into the current version of [Rasa X](https://rasa.com/docs/rasa-x/).  

# Functionality
### Greeting/Introduction
The chatbot responds with greetings, gratitude and farewell. Additionally, the chatbot can inform the user of what it is capable of doing.  

### Description of item by code(ID) or name
The chatbot describes an item upon provision of name and/or code(unique identification). An item may refer to a course, subject, major, sub-major, choice block or stream. This short description is followed by an URL to the UTS Handbook.  

### Maintaining contextual conversations
The chatbot stores current entities into slots to maintain the same context within a conversation.  

### Questions about items
The chatbot responds to user queries about items such as credit points, duration or whether a course is a combined/honours degree etc.  

### Structure information
The chatbot can retrieve sub-structures of a course or related sub-structured and vice-versa. For example, what subjects are under a course or what majors are under a course. This needs to be further developed as it currently only works from course -> sub-structure and vice-versa.  

# Rasa Installation  
### Rasa Guide  
For Rasa installation and setup, these resources may assist you.  

 - [Rasa Installation Documentation](https://rasa.com/docs/rasa-x/installation-and-setup/install/local-mode)
 - [Rasa Installation/Setup Video Guide](https://www.youtube.com/watch?v=GwaSJUlB8oA)  

Disregard steps to run `rasa init` as this involves creating an entirely new project.

### Basic Installation
Assuming that Python and a virtual environment has been setup, these basic steps may immediately complete installation.
   ```
   pip install rasa-x --extra-index-url https://pypi.rasa.com/simple
   pip install rasa[spacy]
   python -m spacy download en_core_web_md
   python -m spacy download en_core_web_sm
   ```  
If you followed the [video setup guide](https://www.youtube.com/watch?v=GwaSJUlB8oA), you may find that the `python -m spacy link en_core_web_md en` command does not work. As outlined above, run `python -m spacy download en_core_web_sm` instead. In saying that, the [video guide](https://www.youtube.com/watch?v=GwaSJUlB8oA) helped me in setting up Rasa X.  

There may be conflicts in software packages depending on the environment that you run your system, seek out online assistance for this.  

### Software/OS Versions
 - Python 3.8.10  
 - pip 20.0.2  
 - Rasa 2.8.2  
 - Rasa X 0.42.0  
 - spaCy 3.1.1  
 - Ubuntu 20.04.2 LTS

# System Instructions
### Setup
Train the chatbot.
   ```
   rasa train
   ```
### Webchat  
Please ensure that the Rasa system has been fully set up on your server and underlying packages have been installed.

 - The Chatbot communicates with the Rasa server using the `rest` channel. Ensure that this is enabled or added in the `credentials.yml` file.
 - Open two terminals and run the following commands (from root directory):
    ```
    rasa run actions --cors "*" --debug
    ```
    ```
    rasa run -m models --enable-api --cors "*" --debug
    ```
 - Once the Rasa server is running, interact with the chatbot by running `index.html` file in the browser.  

### Rasa X  
 - To initialise Rasa X for training and validation, open two terminals and run the following commands (from root directory):
    ```
    rasa run actions -vv
    ```
    ```
    rasa x
    ```  

### Other helpful commands
Each of the following commands needs `rasa run actions` to be run on a separate terminal.
 - To test conversation in the command line, run:
    ```
    rasa shell
    ```  
 - To train and validate conversation in the command line, run:
    ```
    rasa interactive
    ```
---------------------------------------------------------------------------------------------------------
# Datasets  
### Database  
The chatbot is supported by a dataset extracted from [UTS FEIT Chatbot](https://github.com/XinghaoYang/UTSChatbot). This contains information about UTS courses, subjects, majors, sub-majors etc. However, it is important to note that this is currently being used as a sample dataset as it does not compose of all the details about UTS courses as there are no publicly available APIs to be used for complete access. The datasets are stored under `data/csv/` which were trasnformed into a SQLite3 database `uts.db`.  

### NLU
`data/nlu.yml` contains training data of structured information about user messages to determine the intent of the user.  
   ```
   - intent: intent_name
     examples: |
      - sample sentence with [entity](entity_type)

   - intent: list
     examples: |
      - Can you show me the [courses](type) at UTS
      - I would like to know the [subjects](code) at UTS
      - [Majors](code) please
      - Tell me the [subjects](code) at UTS please
      - I would like to hear the [Subjects](code)
      - I would loke to hear the [sub-majors](code), please
      - Can you tell me the [submajors](code)
      - Please tell me the [streams](code) at UTS
   ```

### Stories
`data/stories.yml` contains training data to train the chatbot's conversation and dialogue management that represents the conversation between user and chatbot.  
   ```
   - story: story_name
     steps:
     - intent: intent_name
     - action: action_name

   - story: story_what_can_you_do_02
     steps:
     - intent: greet
     - action: utter_greet
     - intent: what_can_you_do
     - action: utter_what_can_you_do
     - intent: thanks
     - action: utter_thanks
     - intent: goodbye
     - action: utter_goodbye
   ```

### Domain  
`domain.yml` establishes the universe in which the chatbot operates and defines its inputs and outputs. This also includes information about intents, entities, slots and actions. Additionally, basic utterances or responses are defined here (as opposed to custom actions - which will be discussed later). For example:
   ```
   responses:
      utter_code_does_not_exist:
      - text: '{code} does not exist in the UTS directory.'
      - text: Sorry, I could not find {code} in the UTS directory.
      - text: I cannot find {code} in the UTS directory.
      utter_fallback:
      - text: Sorry I did not recognise that input. Can you try again?
      - text: Sorry I did not get that. Could you try that again?
      utter_goodbye:
      - text: Bye
      - text: See you!
   ```
# Intents
Stored in `nlu.yml`, intents represent the user messages that denote the objectives of a user. In essence, these are the types of questions that the user can ask the chatbot.  

| Intent           | Description                                                                       |
| ---------------- |:---------------------------------------------------------------------------------:|
| affirm           | User confirms or acknowledges chatbot response                                    |
| atar             | User queries about ATAR requirement of course                                     |
| children         | User queries about sub-structures under a course or other related sub-structures  |
| combined         | User queries whether the course is a combined degree                              |
| deny             | User rejects chatbot response                                                     |
| details          | User queries detailed information about course or sub-structure                   |
| duration         | User queries completion duration of course                                        |
| fees             | User queries about course fees                                                    |
| goodbye          | User bids farewell to chatbot and concludes conversation                          |
| greet            | User addresses chatbot                                                            |
| honours          | User queries whether the course is an honours degree                              |
| list             | User queries a list of courses or sub-structures                                  |
| parent           | User queries about courses or related sub-structures containing a sub-structure   |
| prof_prac        | User queries whether the course offers a diploma in professional practice         |
| thanks           | User offers gratitude to chatbot                                                  |
| what_you_can_do  | User asks about the features of the chatbot                                       |

# Actions
### Custom Actions
The chatbot will predict an action that is most relevant to the user message after it has been analysed based on the training components such as stories and NLU. These actions can be regular responses or custom actions that query a database to extract information based on said user query. The following table outlines describes each custom action developed to query the database.   

| Action                 | Description                                                                  |
| ---------------------- |:----------------------------------------------------------------------------:|
| action_atar            | Retrieve ATAR requirements of a course                                       |
| action_children        | Retrieve list of sub-structures under a course or sub-structure              |
| action_credit_points   | Retrieve number of credit points associated to course or sub-structure       |
| action_combined        | Retrieve whether a course is a combined degree                               |
| action_details         | Retrieve details about a course or sub-structure, including its website link |
| action_duration        | Retrieve number of years to complete a course                                |
| action_fees            | Retrieve information about fees                                              |
| action_honours         | Retrieve whether a course is a honours degree                                |
| action_list            | Retrieve list of sub-structures or courses associated to query               |
| action_parent          | Retrieve list of parent courses or sub-structures associated to sub-structure|
| action_prof_prac       | Retrieve whether a course offers a diploma in professional practice          |
| utter_greet            | Responds to user with a regular greeting along with several buttons          |

### Python Script
`actions.py` contains the backend processing involved to transform data and query the database in addition to running custom action calls that have been described above. Each action name corresponds to the same class in the Python file derived by the `name` method.  

Some special functions include:  
   ```
   class DbQueringMethods [Database querying class]
      create_connection()        ->    returns database connection
      query_tables()             ->    returns query results from courses and sub_structures tables
      select_by_slot()           ->    returns query results from table with entity filter
      select_by_multiple_slot()  ->    returns query results from table with multiple entity filters
      select_children()          ->    returns children query results
      select_parent()            ->    returns parent query results

   check_code()                  ->    returns item type acronym, e.g. cbk, maj, smj
   get_type()                    ->    returns item type full name
   check_type()                  ->    returns item type from an item to supply URL
   get_url()                     ->    returns URL link of associated item
   ```

# SQLite3 Database
To access the database from the command line, run (from root directory):
   ```
   sqlite3 uts.db
   ```  
To view available tables while in the sqlite3 terminal:
   ```
   .tables
   ```  
To view tables in readable structure while in the sqlite3 terminal:
   ```
   .header on
   .mode column
   SELECT * FROM courses;
   ```  
# Chatbot Snippets
### Home screen  
![ScreenShot](static/img/home.PNG)  
### Chatbot  
![ScreenShot](static/img/chatbot.PNG)  

# Recommendations
### Official UTS Database Connection
The database does not possess every single type of information available to UTS courses and sub-structures. This is the reason the chatbot has a feature for providing a website link to their corresponding UTS Handbook pages to find more information.  

It would be ideal for the chatbot system to be connected to the official UTS database so that it parses every type of information. This could be done through an API (Application Programming Interface) connection.  

### UTS Handbook Integration
The UTS FEIT Chatbot would find its most appropriate location to be integrated in the UTS Handbook website. As a result, users can interact with the chatbot and find convenience in talking to what appears to be human. As an alternative domain of information, users would be able to simply query their request rather than spending significant amounts of time browsing through various webpages to locate their objective.  

### Further Training
The chatbot development can be expanded by training the machine learning components more. At this stage, the UTS FEIT Chatbot may have not considered every single possible human request. As such, more extensive training will only develop the chatbot scope further.  

### Data Management in Conversations
Future research can be conducted in the sector of data management in chatbot conversations or dialogues. As explored in this paper, this topic possesses significance in completely portraying human behaviour to cover more applications and uses.  

In the context of this project, this would assist in the chatbot being able to further comprehend the context of conversations. The result would be the chatbot being more convenient to students as they can imitate human behaviour. Instead of relying on the university call centre, this chatbot could replicate that procedure and output similar responses.  

### Chatbot Expansion
The scope of this project has been for engineering and information technology courses at UTS. This could be expanded to include every single course and sub-structure at the university. However, this would require modifications to the data structure and entity relationships of the implemented database system. Additionally, a change in database software would be necessary to something more scalable. As stated, it would be ideal if this system is plugged into the official UTS database which is assumed to be run on the cloud. The immense amount of data should this type of expansion be implemented would be enormous.  

The chatbot can expand further by not only narrowing down its scope to information about courses and sub-structures, but also general information about the university. It can become an alternative source of information in contrast to Ask UTS, which is the primary centre for student inquiries.  
