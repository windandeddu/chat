# chat(master)

to run the app on Linux:
-open console
(if you have pip, miss next step)
______________________________________
-$ sudo apt-get install python3-pip
______________________________________
-go to folder chat 
-$ python3 -m venv venv
-$ source venv/bin/activate
-(venv)$ export FLASK_APP=chat.py
-(venv)$ pip install flask, flask_sqlalchemy, flask_migrate, flask_login, flask_wtf, email_validator
-(venv)$ flask run

to start chating, you need to register new user
then on index page, you can use search to find other users
and press the button 'send massage', then you will be taken to the chat page

Я использовал Flask, потому что, лучше всего с ним разобрался во время моего самообучения.
На нём я сделал примитивный интернет магазин, который вы можете увидеть [здесь](https://github.com/windandeddu/eshop).
В процессе работы столкнулся с трудностью подключения websocket, для мгновенного получения и отправки сообщений, без перезагрузки страницы.
