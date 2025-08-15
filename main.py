import psycopg2
from secret import *
import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
from datetime import datetime
from context import *
from geopy.distance import geodesic

correct_location = (40.712776, -74.005974)

# Database functions (same as in your original code)
def open_connection():
    conn = psycopg2.connect(database='attendence1',
                            user='postgres',
                            host='localhost',
                            password=passw,
                            port=5432)
    return conn

def close_connection(conn, cur):
    conn.close()
    cur.close()

bot = telebot.TeleBot(API_KEY)

# Create necessary tables
create_db_group()
create_db_user()
create_db_attendence()
create_reason()

# Commands handler
@bot.message_handler(commands=['start'])
def handler(message):
    btn1 = types.InlineKeyboardButton("add_me")
    btn2 = types.InlineKeyboardButton("come")
    btn3 = types.InlineKeyboardButton("left")
    btn4 = types.InlineKeyboardButton("i come")
    btn5 = types.InlineKeyboardButton("i don't come")
    btn6 = types.InlineKeyboardButton("i left")
    btn7 = types.InlineKeyboardButton("show not come")
    btn8 = types.InlineKeyboardButton("change")
    location_btn = types.KeyboardButton("Share location", request_location=True)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if message.chat.id == 1077938369:  # Admin user ID
        markup.row(btn2, btn3)
        markup.row(btn7, btn8)
    else:
        markup.row(btn1)
        markup.row(btn4, btn5)
        markup.row(btn6)
        markup.add(location_btn)
    bot.send_message(message.chat.id, "Salom xush omaded ba attendence bot!", reply_markup=markup)
    bot.register_next_step_handler(message, m_handler)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_location = message.location
    
    # Extract latitude and longitude from the user's message
    user_coords = (user_location.latitude, user_location.longitude)
    print(f"User's location: {user_coords}")
    
    # Define your correct location (e.g., New York City coordinates)
    correct_location = (38.563642, 68.758958)  # Replace with your desired location coordinates
    
    # Calculate the distance between the user's location and the correct location
    distance = geodesic(user_coords, correct_location).meters
    print(f"Distance from correct location: {distance} meters")
    
    # Define an acceptable radius (e.g., 100 meters)
    if distance <= 600:  # If the user is within 100 meters
        bot.send_message(message.chat.id, "You are in the correct location!")
        # You can now register attendance or other actions here
        id1 = message.chat.id
        today = datetime.now().date()
        conn = open_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT student_id FROM attendence_attendence WHERE student_id = '{id1}'  AND status = 'come'")
        a = cur.fetchone()
        if a:
            bot.send_message(message.chat.id, "Your attendance is already registered!")
        else:
            cur.execute(f"""INSERT INTO attendence_attendence(student_id, arrived_at, status) 
                            VALUES((SELECT id FROM attendence_student WHERE tg_id='{id1}'), NOW(), 'come')""")
            conn.commit()
            bot.send_message(message.chat.id, "You have successfully registered your arrival!")
        close_connection(conn, cur)
    else:
        bot.send_message(message.chat.id, "You are not in the correct location!")
    
    # You can continue with your logic here after checking the location
    bot.register_next_step_handler(message, m_handler)


@bot.message_handler()
def m_handler(message):
    if message.text == "add_me":
        bot.send_message(message.chat.id, "Enter full name of student: ")
        bot.register_next_step_handler(message, name)
    elif message.text == "come":
        bot.send_message(message.chat.id, "Enter student id to register his arrival!")
        bot.register_next_step_handler(message, changer)
    elif message.text == "left":
        bot.send_message(message.chat.id, "Enter student id to register his departure!")
        bot.register_next_step_handler(message, changer)
    elif message.text == "i come":
        bot.send_message(message.chat.id, "You are welcome!")
        id1 = message.chat.id
        today = datetime.now().date()
        conn = open_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT student_id FROM attendence_attendence WHERE student_id = '{id1}'  AND status = 'come'")
        a = cur.fetchone()
        if a:
            bot.send_message(message.chat.id, "Your attendance is already registered!")
        else:
            cur.execute(f"""INSERT INTO attendence_attendence(student_id, arrived_at, status) 
                            VALUES((SELECT id FROM attendence_student WHERE tg_id='{id1}'), NOW(), 'come')""")
            conn.commit()
            bot.send_message(message.chat.id, "You have successfully registered your arrival!")
        close_connection(conn, cur)
        bot.register_next_step_handler(message, m_handler)
    elif message.text == "i don't come":
        bot.send_message(message.chat.id, "Enter the reason why you are not coming")
        bot.register_next_step_handler(message, reason)
    elif message.text == "i left":
        bot.send_message(message.chat.id, "Good luck, see you next time!")
        id1 = message.chat.id
        today = datetime.now().date()
        conn = open_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT student_id FROM attendence_attendence WHERE student_id = '{id1}'  AND status = 'left'")
        a = cur.fetchone()
        print(a)
        if a:
            bot.send_message(message.chat.id, "You have already left!")
        else:
            cur.execute(f"""INSERT INTO attendence_attendence(student_id, left_at, status) 
                            VALUES((SELECT id FROM attendence_student WHERE tg_id='{id1}'), NOW(), 'left')""")
            conn.commit()
            bot.send_message(message.chat.id, "Your departure has been registered!")
        close_connection(conn, cur)
        bot.register_next_step_handler(message, m_handler)
    elif message.text == "show not come":
        conn = open_connection()
        cur = conn.cursor()
        today = datetime.now().date()
        cur.execute(f"SELECT * FROM attendence_apsent WHERE student_id IN (SELECT id FROM attendence_student WHERE tg_id != '') AND student_id NOT IN (SELECT student_id FROM attendence_attendence WHERE EXTRACT(DAY FROM arrived_at) = {today} AND status = 'come')")
        res = cur.fetchall()
        bot.send_message(message.chat.id, str(res))
        bot.register_next_step_handler(message, m_handler)
    elif message.text == "change":
        bot.send_message(message.chat.id, "Enter student id to change their attendance status:")
        bot.register_next_step_handler(message, changer)

def changer(message):
    student_id = message.text
    today = datetime.now().date()
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT student_id FROM attendence_apsent WHERE student_id = '{student_id}' AND reason IS NOT NULL")
    x = cur.fetchone()
    if x:
        bot.send_message(message.chat.id, "This student's attendance is marked as absent, changing status...")
        cur.execute(f"DELETE FROM attendence_apsent WHERE student_id = '{student_id}' AND reason IS NOT NULL")
        cur.execute(f"""INSERT INTO attendence_attendence(student_id, arrived_at, status) 
                        VALUES('{student_id}', NOW(), 'come')""")
        conn.commit()
        bot.send_message(message.chat.id, "Student's attendance updated to 'come'.")
    else:
        bot.send_message(message.chat.id, "This student is not in the absence list!")
    close_connection(conn, cur)
    bot.register_next_step_handler(message, m_handler)

def reason(message):
    student_id = message.chat.id
    reason = message.text
    today = datetime.now().date()
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT student_id FROM attendence_attendence WHERE student_id = '{student_id}' ")
    if cur.fetchone():
        bot.send_message(message.chat.id, "You are already marked as present!")
    else:
        cur.execute(f"""INSERT INTO attendence_apsent(student_id, reason) 
                        VALUES((SELECT id FROM attendence_student WHERE tg_id='{student_id}'), '{reason}')""")
        conn.commit()
        bot.send_message(message.chat.id, "Your absence reason has been registered.")
    close_connection(conn, cur)
    bot.register_next_step_handler(message, m_handler)

def name(message):
    global f_name
    f_name = message.text
    bot.send_message(message.chat.id, """Enter course that student wants to study 
python-1
c++ - 2:""")
    bot.register_next_step_handler(message, course)

def course(message):
    global course_n
    course_n = message.text
    bot.send_message(message.chat.id, "Enter student phone number:")
    bot.register_next_step_handler(message, adder)

def adder(message):
    phone = message.text
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM attendence_student WHERE tg_id = '{message.chat.id}'")
    if cur.fetchone():
        bot.send_message(message.chat.id, "You are already registered in the system!")
    else:
        cur.execute("INSERT INTO attendence_student(id, tg_id, name, group_id, phone) VALUES(%s, %s, %s, %s, %s)",
                    (message.chat.id, message.chat.id, f_name, course_n, phone))
        conn.commit()
        bot.send_message(message.chat.id, "You have been successfully registered!")
    close_connection(conn, cur) 
    bot.register_next_step_handler(message, m_handler)

bot.infinity_polling()
