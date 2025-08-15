import psycopg2
from secret import *
import telebot

def open_connection():
    conn = psycopg2.connect(database = 'attendence1',
                            user = 'postgres',
                            host = 'localhost',
                            password = passw,
                             port = 5432 )
    return conn
def close_connection(conn,cur):
    conn.close()
    cur.close()

bot = telebot.TeleBot(API_KEY)

def create_db_group():
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"""create table if not exists attendence_group(
                name varchar(50),
                time time without time zone,
                price numeric(6,2),
                description text);""")
    conn.commit()
    close_connection(conn,cur)

def create_db_user():
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"""create table if not exists attendence_student(
                name varchar(250),
                age integer,
                phone varchar(13),
                address varchar(150),
                group_id bigint default 1 null,
                tg_id varchar(20));""")
    conn.commit()
    close_connection(conn,cur)

def create_db_attendence():
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"""create table if not exists attendence_attendence(
                arrived_at datetime,
                left_at datetime,
                status varchar(50),
                student_id bigint);""")
    conn.commit()
    close_connection(conn,cur)

def create_reason():
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(f"""create table if not exists attendence_apsent(
                reason text,
                student_id bigint);""")
    conn.commit()
    close_connection(conn,cur)

    