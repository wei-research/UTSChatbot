# UTS - 41030 Engineering Capstone - UTS FEIT Chatbot
41030 Engineering Capstone - Spring 2021

Project name: AI Chatbot Development
Student: Christian Cabato (12915892)
Major: Data Engineering

Supervisor: Wei Liu
Co-adivsor: Xinghao Yang
Original chatbot repository: https://github.com/XinghaoYang/UTSChatbot

Chatbot widget source: https://github.com/JiteshGaikwad/Chatbot-Widget

# System Instructions
Please ensure that the Rasa system has been fully set up on your server and underlying packages have been installed.

 - The Chatbot communicates with the Rasa server using `rest` channel. Ensure that this is enabled or added in the `credentials.yml` file.
 - Open two terminals and run the following commands on each:
    ->
    ```
    rasa run -m models --enable-api --cors "*" --debug
    ```
    ->
    ```
    rasa run actions --cors "*" --debug
    ```
 - Once the Rasa server is running, interact with the chatbot by running `index.html` file in the browser.
