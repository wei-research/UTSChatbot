# UTS - 41030 Engineering Capstone - UTS FEIT Chatbot
41030 Engineering Capstone - Spring 2021

Project name: AI Chatbot Development  
Student: Christian Cabato (12915892)  
Major: Data Engineering  

Supervisor: [Wei Liu](https://www.uts.edu.au/staff/wei.liu)  
Co-adivsor: [Xinghao Yang](https://xinghaoyang.github.io/)  
Original chatbot repository: https://github.com/XinghaoYang/UTSChatbot  

Chatbot widget source: https://github.com/JiteshGaikwad/Chatbot-Widget  
Conversational AI: [Rasa](https://rasa.com/)  

# Description
The UTS FEIT Chatbot is a chatbot system that responds to user queries regarding courses and underlying sub-structures at the University of Technology Sydney (UTS). My primary responsibility revolves around the improvement of the data management aspects of the current [UTS FEIT Chatbot](https://github.com/XinghaoYang/UTSChatbot) and migrate its Rasa system into the current version of [Rasa X](https://rasa.com/docs/rasa-x/).  

# Rasa Installation
For Rasa installation and setup, these resources may assist you.  

 - https://rasa.com/docs/rasa-x/installation-and-setup/install/local-mode
 - https://www.youtube.com/watch?v=GwaSJUlB8oA  

# System Instructions
Please ensure that the Rasa system has been fully set up on your server and underlying packages have been installed.

 - The Chatbot communicates with the Rasa server using the `rest` channel. Ensure that this is enabled or added in the `credentials.yml` file.
 - Open two terminals and run the following commands (from root directory) on each:
    ```
    rasa run -m models --enable-api --cors "*" --debug
    ```
    ```
    rasa run actions --cors "*" --debug
    ```
 - Once the Rasa server is running, interact with the chatbot by running `index.html` file in the browser.
---------------------------------------------------------------------------------------------------------

# Dataset  
The chatbot is supported by a dataset extracted from [UTS FEIT Chatbot](https://github.com/XinghaoYang/UTSChatbot). This contains information about UTS courses, subjects, majors, sub-majors etc. However, it is important to note that this is currently being used as a sample dataset as it does not compose of all the details about UTS courses as there are no publicly available APIs to be used for complete access. The datasets are stored under `data/csv/` which were converted into a SQLite3 database.

# To-do
 - Tailor conversation flow and test every type of questions/responses
 - Explore other types of questions
 - To include sub_structure relationships in relations table?