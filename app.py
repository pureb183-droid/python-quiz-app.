import streamlit as st
import pandas as pd
import os
import io
import html
import base64
from datetime import datetime

# 1. Веб-сайттын негизги жөндөөлөрү
st.set_page_config(page_title="Python тести & Аналитика", layout="wide")

# 2. Сессиялык абалдарды аныктоо
if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = None
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "login"

# 3. Сайттын CSS стилдери
st.markdown("""
<style>
    .main { 
        background-color: #f0f2f6; 
    }
    .card-3d {
        background: #ffffff;
        border-radius: 16px;
        padding: 25px;
        margin: 10px 0px;
        box-shadow: 6px 6px 8px #c5c9d1, -6px -6px 12px #ffffff;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .card-title { 
        color: #5a67d8; 
        font-size: 16px; 
        font-weight: bold; 
        margin-bottom: 5px; 
    }
    .card-value { 
        color: #2d3748; 
        font-size: 32px; 
        font-weight: 900; 
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; 
        border-radius: 12px; 
        padding: 12px 28px;
        font-weight: bold; 
        border: none;
        box-shadow: 3px 3px 8px #b8b8b8, -3px -3px 8px #ffffff;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 5px 5px 12px #9c9c9c, -5px -5px 12px #ffffff;
    }
    .cert-box {
        border: 12px double #4a5568; 
        padding: 45px; 
        text-align: center;
        background: #ffffff; 
        border-radius: 20px;
        box-shadow: 10px 10px 25px rgba(0,0,0,0.1);
        max-width: 750px; 
        margin: 30px auto;
    }
    .stage-header {
        background: linear-gradient(90deg, #ebf8ff 0%, #bee3f8 100%);
        padding: 15px; 
        border-radius: 10px;
        color: #2b6cb0; 
        font-weight: bold; 
        margin-bottom: 25px;
        border-left: 5px solid #3182ce;
    }
</style>
""", unsafe_allow_html=True)

# 4. Базаларды түзүү жана жүктөө
USERS_DB = "users_database.csv"
DB_FILE = "quiz_database.csv"

if not os.path.exists(USERS_DB):
    pd.DataFrame(columns=["fio", "clazz", "username", "password", "avatar_bytes"]).to_csv(USERS_DB, index=False)

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["ФИО", "Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли", "Учурдагы_Этап", "Жооптор"]).to_csv(DB_FILE, index=False)

def load_users():
    if os.path.exists(USERS_DB):
        try:
            return pd.read_csv(USERS_DB)
        except:
            return pd.DataFrame(columns=["fio", "clazz", "username", "password", "avatar_bytes"])
    return pd.DataFrame(columns=["fio", "clazz", "username", "password", "avatar_bytes"])

def register_user(fio, clazz, username, password, avatar_bytes=""):
    df = load_users()
    if username in df["username"].values.astype(str):
        return False
    new_user = pd.DataFrame([{"fio": fio, "clazz": clazz, "username": username, "password": password, "avatar_bytes": avatar_bytes}])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USERS_DB, index=False)
    return True

def verify_user(username, password):
    df = load_users()
    match = df[(df["username"].astype(str) == str(username)) & (df["password"].astype(str) == str(password))]
    if not match.empty:
        return match.iloc[0].to_dict()
    return None

def load_db():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame(columns=["ФИО", "Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли", "Учурдагы_Этап", "Жооптор"])
    return pd.DataFrame(columns=["ФИО", "Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли", "Учурдагы_Этап", "Жооптор"])

def save_to_db(fio, clazz, time_str, score_str, percent, level, stage, answers_str):
    df = load_db()
    if fio in df["ФИО"].values:
        df.loc[df["ФИО"] == fio, ["Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли", "Учурдагы_Этап", "Жооптор"]] = [clazz, time_str, score_str, percent, level, stage, answers_str]
    else:
        new_row = pd.DataFrame([{"ФИО": fio, "Класс": clazz, "Убактысы": time_str, "Туура жооп": score_str, "Процент (%)": percent, "Деңгээли": level, "Учурдагы_Этап": stage, "Жооптор": answers_str}])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# 5. Тест суроолору
QUESTIONS = [
    {"q": "Pythonдо кайсы өзгөрмөнүн аты ката жазылган?", "options": ["my_var", "_age", "userAge", "1st_place"], "answer": "1st_place"},
    {"q": "Pythonдо 5 / 2 туюнтмасы кандай типти кайтарат?", "options": ["int", "float", "str", "bool"], "answer": "float"},
    {"q": "print('A' * 2) буйругу экранга эмнени чыгарат?", "options": ["A * 2", "A 2", "AA", "Ката кетет"], "answer": "AA"},
    {"q": "Тизменин аягына элемент кошуучу метод кайсы?", "options": ["add()", "append()", "push()", "insert()"], "answer": "append()"},
    {"q": "print('A', 'B', sep='-') эмнени чыгарат?", "options": ["A B", "A,B", "A-B", "AB"], "answer": "A-B"},
    {"q": "input() аркылуу кирген маалымат демейки боюнча кайсы типте болот?", "options": ["str", "int", "float", "list"], "answer": "str"},
    {"q": "len() функциясы кандай маани берет?", "options": ["1", "2", "3", "0"], "answer": "3"},
    {"q": "Pythonдо 17 % 5 туюнтмасынын калдыгы канча?", "options": ["3", "2", "1", "5"], "answer": "2"},
    {"q": "Шарттуу операторду (эгерде) ачуучу ачкыч сөз кайсы?", "options": ["if", "else", "for", "while"], "answer": "if"},
    {"q": "Барабарлыкты текшерүүчү операторду көрсөтүңүз?", "options": ["=", "===", "is", "=="], "answer": "=="},
    {"q": "Pythonдо логикалык 'ЖАНА' оператору кайсы?", "options": ["&&", "and", "AND", "not"], "answer": "and"},
    {"q": "Pythonдо логикалык 'ЖЕ' оператору кайсы сөз?", "options": ["||", "or", "OR", "xor"], "answer": "or"},
    {"q": "Кайсы маалымат тиби өзгөрүлбөйт (immutable)?", "options": ["list", "dict", "set", "tuple"], "answer": "tuple"},
    {"q": "Сапты бүтүн санга айландыруучу функция?", "options": ["str()", "int()", "float()", "num()"], "answer": "int()"},
    {"q": "Коддогу бир саптуу комментарий кайсы символ менен башталат?", "options": ["//", "/*", "#", "--"], "answer": "#"},
    {"q": "for i in range(3): циклы канча жолу айланат?", "options": ["2 жолу", "3 жолу", "4 жолу", "Чексиз"], "answer": "3 жолу"},
    {"q": "range(3) функциясы кайсы сандарды берет?", "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2
