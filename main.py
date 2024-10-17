import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
from context import *
from datetime import datetime

create_db_user()
create_db_come()
create_reason()

@bot.message_handler(commands = ['start'])
def handler(message):
    btn1 = types.InlineKeyboardButton("add_me")
    btn2 = types.InlineKeyboardButton("come")
    btn3 = types.InlineKeyboardButton("left")
    btn4 = types.InlineKeyboardButton("i come")
    btn5 = types.InlineKeyboardButton("i don't come")
    btn6 = types.InlineKeyboardButton("i left")
    btn7 = types.InlineKeyboardButton("show not come")
    btn8 = types.InlineKeyboardButton("change")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if message.chat.id == 1077938369:
        markup.row(btn2,btn3)
        markup.row(btn7,btn8)
    else:
        markup.row(btn1)
        markup.row(btn4,btn5)
        markup.row(btn6)
    bot.send_message(message.chat.id, "Salom xush omaded ba attendence bot!",reply_markup=markup)
    bot.register_next_step_handler(message,m_handler)


@bot.message_handler()
def m_handler(message):
    if message.text == "add_me":
        bot.send_message(message.chat.id,"Enter full name of student: ")
        bot.register_next_step_handler(message,name)
    elif message.text == "come":
        bot.send_message(message.chat.id,"Enter student id to regist his come!")
        bot.register_next_step_handler(message,comer)
    elif message.text == "left":
        bot.send_message(message.chat.id, "Enter students id to reg his left!")
        bot.register_next_step_handler(message,lefter)
    elif message.text == "i come":
        bot.send_message(message.chat.id,"you are welcome)")
        id1 = message.chat.id
        today = datetime.now().date()
        conn = open_connection()
        cur = conn.cursor()
        cur.execute(f"select user_id from come where user_id = '{id1}' and c_time = '{today}' and status = 'come'")
        a = cur.fetchone()
        if a!=None:
            bot.send_message(message.chat.id, "Your come is already reged!")
        else:
            cur.execute(f"""insert into come(user_id,st_name,status) values(
                       (select id from students where id='{id1}'),
                       (select full_name from students where id='{id1}'),
                       'come')""")
            conn.commit()
            bot.send_message(message.chat.id, "you reg your come good luck))!")
        close_connection(conn,cur)
        bot.register_next_step_handler(message,m_handler)
    elif message.text == "i don't come":
        bot.send_message(message.chat.id, "Enter reason why you dont come")
        bot.register_next_step_handler(message,reason)
    elif message.text == "i left":
        bot.send_message(message.chat.id,"Good luck see you next lesson!")
        id1 = message.chat.id
        today = datetime.now().date()
        conn = open_connection()
        cur = conn.cursor()
        cur.execute(f"select user_id from come where user_id = '{id1}' and c_time = '{today}' and status = 'left'")
        a = cur.fetchone()
        if a!=None:
            bot.send_message(message.chat.id, "You already left!")
        else:
            cur.execute(f"""insert into come(user_id,st_name,status) values(
                        (select id from students where id='{id1}'),
                        (select full_name from students where id='{id1}'),
                        'left')""")
            conn.commit()
            bot.send_message(message.chat.id, "Your left registered!")
        close_connection(conn,cur)
        bot.register_next_step_handler(message,m_handler)
        
    elif message.text == "show not come":
        conn = open_connection()
        cur = conn.cursor()
        today = datetime.now().date()
        cur.execute(f"select * from reason where c_time = '{today}'")
        res = cur.fetchall()
        bot.send_message(message.chat.id, str(res))
        bot.register_next_step_handler(message,m_handler)
    elif message.text == "change":
        bot.send_message(message.chat.id, "Enter students id:")
        bot.register_next_step_handler(message,changer)
    
def changer(message):
    st = message.text
    today = datetime.now().date()
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"select user_id from reason where user_id = '{st}'")
    x = cur.fetchone()
    if x!=None:
        bot.send_message(message.chat.id,"This student is no in this list")
    else:
        cur.execute(f"delete from reason where user_id = '{st}' and c_time = '{today}'")
        cur.execute(f"insert into come(user_id,st_name,status)  values(
                    (select id from students where id='{st}'),
                    (select full_name from students where id='{st}'),
                    'come')""")
        conn.commit()
        bot.send_message(message.chat.id, "Student's come registered!")
    close_connection(conn,cur)
    bot.register_next_step_handler(message,m_handler)





def reason(message):
    id_no = message.chat.id
    reas = message.text
    today = datetime.now().date()
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"select user_id from come where user_id = '{id_no}' and c_time = '{today}' and status ='come'")
    b = cur.fetchone()
    if b!=None:
        bot.send_message(message.chat.id,"You are already here!")
    else:
        cur.execute(f"select user_id from reason where user_id = '{id_no}' and c_time = '{today}'")
        a = cur.fetchone()
        if a!=None:
            bot.send_message(message.chat.id, "You alreadu add your reason for not coming!")
        else:
            cur.execute(f"""insert into reason(user_id,st_name,reason) values(
                        (select id from students where id='{id_no}'),
                        (select full_name from students where id='{id_no}'),
                        '{reas}')""")
            conn.commit()
            bot.send_message(message.chat.id, "you reg your not coming try to be apsent less))!")
    close_connection(conn,cur)
    bot.register_next_step_handler(message,m_handler)
    

@bot.message_handler()
def lefter(message):
    id1 = message.chat.id
    today = datetime.now().date()
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"select user_id from come where user_id = '{id1}' and c_time = '{today}' and status = 'left'")
    a = cur.fetchone()
    if a!=None:
        bot.send_message(message.chat.id, "This student is already left!")
    else:
        cur.execute(f"""insert into come(user_id,st_name,status) values(
                    (select id from students where id='{id1}'),
                    (select full_name from students where id='{id1}'),
                    'left')""")
        conn.commit()
        bot.send_message(message.chat.id, "Student's left registered!")
    close_connection(conn,cur)
    bot.register_next_step_handler(message,m_handler)


@bot.message_handler()
def comer(message):
    id1 = message.chat.id
    today = datetime.now().date()
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"select user_id from come where user_id = '{id1}' and c_time = '{today}' and status = 'come'")
    a = cur.fetchone()
    if a!=None:
        bot.send_message(message.chat.id, "This student is already here!")
    else:
        cur.execute(f"""insert into come(user_id,st_name,status) values(
                    (select id from students where id='{id1}'),
                    (select full_name from students where id='{id1}'),
                    'come')""")
        conn.commit()
        bot.send_message(message.chat.id, "Student's come registered!")
    close_connection(conn,cur)
    bot.register_next_step_handler(message,m_handler)

def name(message):
    global f_name
    f_name = message.text
    bot.send_message(message.chat.id, "Enter course that student wanna study!")
    bot.register_next_step_handler(message,course)

def course(message):
    global course_n
    course_n = message.text
    bot.send_message(message.chat.id,"Enter student phone number")
    bot.register_next_step_handler(message,adder)

@bot.message_handler()
def adder(message):
    phone = message.text
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"select id from students where id = '{message.chat.id}'")
    c = cur.fetchone()
    if c!=None:
        bot.send_message(message.chat.id,"You already reged in system!")
    else:
        cur.execute("insert into students(id,full_name,course,phone_number) values(%s,%s,%s,%s)", (message.chat.id,f_name,course_n,phone))
        conn.commit()
    close_connection(conn,cur)
    bot.register_next_step_handler(message,m_handler)

bot.infinity_polling()