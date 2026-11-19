import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# 1. Веб-сайттын негизги жөндөөлөрү
st.set_page_config(page_title="Python тести & Аналитика", page_icon="🐍", layout="wide")

# 2. Сессиялык абалдарды аныктоо
if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = None
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None
if "stage" not in st.session_state:
    st.session_state["stage"] = 1
if "answers" not in st.session_state:
    st.session_state["answers"] = {}

# 3. Сайттын CSS стилдери
st.markdown("""
<style>
    .main { background-color: #f0f2f6; }
    .card-3d {
        background: #ffffff;
        border-radius: 16px;
        padding: 25px;
        margin: 10px 0px;
        box-shadow: 6px 6px 8px #c5c9d1, -6px -6px 12px #ffffff;
        text-align: center;
    }
    .card-title { color: #5a67d8; font-size: 16px; font-weight: bold; margin-bottom: 5px; }
    .card-value { color: #2d3748; font-size: 32px; font-weight: 900; }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border-radius: 12px; padding: 10px 24px;
        font-weight: bold; border: none;
        box-shadow: 3px 3px 8px #b8b8b8;
    }
    .cert-box {
        border: 12px double #4a5568; padding: 35px; text-align: center;
        background: #ffffff; border-radius: 20px;
        box-shadow: 10px 10px 25px rgba(0,0,0,0.1);
        max-width: 750px; margin: 20px auto;
    }
    .stage-header {
        background: linear-gradient(90deg, #ebf8ff 0%, #bee3f8 100%);
        padding: 15px; border-radius: 10px;
        color: #2b6cb0; font-weight: bold; margin-bottom: 20px;
        border-left: 5px solid #3182ce;
    }
    .student-row {
        display: flex; align-items: center; background: white;
        padding: 12px 20px; border-radius: 12px; margin-bottom: 10px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.06);
    }
    .avatar-img {
        width: 50px; height: 50px; border-radius: 50%;
        object-fit: cover; margin-right: 15px; border: 2px solid #25D366;
    }
</style>
""", unsafe_allow_html=True)

# 4. Базаларды түзүү жана жүктөө
USERS_DB = "users_database.csv"
DB_FILE = "quiz_database.csv"

if not os.path.exists(USERS_DB):
    pd.DataFrame(columns=["fio", "clazz", "username", "password", "avatar_bytes"]).to_csv(USERS_DB, index=False)

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["ФИО", "Username", "Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли"]).to_csv(DB_FILE, index=False)

def load_users():
    try:
        return pd.read_csv(USERS_DB)
    except Exception:
        return pd.DataFrame(columns=["fio", "clazz", "username", "password", "avatar_bytes"])

def register_user(fio, clazz, username, password, avatar_bytes=""):
    df = load_users()
    if str(username) in df["username"].astype(str).values:
        return False
    new_user = pd.DataFrame([{
        "fio": fio, "clazz": clazz, "username": username, 
        "password": password, "avatar_bytes": avatar_bytes
    }])
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
    try:
        return pd.read_csv(DB_FILE)
    except Exception:
        return pd.DataFrame(columns=["ФИО", "Username", "Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли"])

def save_to_db(fio, username, clazz, time_str, score_str, percent, level):
    df = load_db()
    if str(username) in df["Username"].astype(str).values:
        df.loc[df["Username"].astype(str) == str(username), ["ФИО", "Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли"]] = [
            fio, clazz, time_str, score_str, percent, level
        ]
    else:
        new_row = pd.DataFrame([{
            "ФИО": fio, "Username": username, "Класс": clazz, "Убактысы": time_str, 
            "Туура жооп": score_str, "Процент (%)": percent, "Деңгээли": level
        }])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# 5. Тест суроолору (30 суроо — 3 этапка бөлүнөт)
QUESTIONS = [
    {"q": "Pythonдо кайсы өзгөрмөнүн аты ката жазылган?", "options": ["my_var", "_age", "userAge", "1st_place"], "answer": "1st_place"},
    {"q": "Pythonдо 5 / 2 туюнтмасы кандай типти кайтарат?", "options": ["int", "float", "str", "bool"], "answer": "float"},
    {"q": "print('A' * 2) буйругу экранга эмнени чыгарат?", "options": ["A * 2", "A 2", "AA", "Ката кетет"], "answer": "AA"},
    {"q": "Тизменин аягына элемент кошуучу метод кайсы?", "options": ["add()", "append()", "push()", "insert()"], "answer": "append()"},
    {"q": "print('A', 'B', sep='-') эмнени чыгарат?", "options": ["A B", "A,B", "A-B", "AB"], "answer": "A-B"},
    {"q": "input() аркылуу кирген маалымат демейки боюнча кайсы типте болот?", "options": ["str", "int", "float", "list"], "answer": "str"},
    {"q": "len([1, 2, 3]) функциясы кандай маани берет?", "options": ["1", "2", "3", "0"], "answer": "3"},
    {"q": "Pythonдо 17 % 5 туюнтмасынын калдыгы канча?", "options": ["3", "2", "1", "5"], "answer": "2"},
    {"q": "Шарттуу операторду (эгерде) ачуучу ачкыч сөз кайсы?", "options": ["if", "else", "for", "while"], "answer": "if"},
    {"q": "Барабарлыкты текшерүүчү операторду көрсөтүңүз?", "options": ["=", "===", "is", "=="], "answer": "=="},
    
    {"q": "Pythonдо логикалык 'ЖАНА' оператору кайсы?", "options": ["&&", "and", "AND", "not"], "answer": "and"},
    {"q": "Pythonдо логикалык 'ЖЕ' оператору кайсы сөз?", "options": ["||", "or", "OR", "xor"], "answer": "or"},
    {"q": "Кайсы маалымат тиби өзгөрүлбөйт (immutable)?", "options": ["list", "dict", "set", "tuple"], "answer": "tuple"},
    {"q": "Сапты бүтүн санга айландыруучу функция?", "options": ["str()", "int()", "float()", "num()"], "answer": "int()"},
    {"q": "Коддогу бир саптуу комментарий кайсы символ менен башталат?", "options": ["//", "/*", "#", "--"], "answer": "#"},
    {"q": "for i in range(3): циклы канча жолу айланат?", "options": ["2 жолу", "3 жолу", "4 жолу", "Чексиз"], "answer": "3 жолу"},
    {"q": "range(3) функциясы кайсы сандарды берет?", "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"], "answer": "0, 1, 2"},
    {"q": "Төмөнкүлөрдүн кайсынысы сөздүк (dictionary) болуп саналат?", "options": ["{1, 2}", "[1, 2]", "(1, 2)", "{'a': 1}"], "answer": "{'a': 1}"},
    {"q": "Сөздүктөн ачкычтарды алуучу метод кайсы?", "options": ["keys()", "values()", "items()", "get()"], "answer": "keys()"},
    {"q": "Жеке функция түзүү үчүн кайсы ачкыч сөз колдонулат?", "options": ["function", "fun", "def", "define"], "answer": "def"},
    
    {"q": "Функциядан маани кайтаруучу ачкыч сөз?", "options": ["give", "return", "back", "exit"], "answer": "return"},
    {"q": "Python тили биринчи жолу кайсы жылы чыккан?", "options": ["1991", "2000", "1985", "1995"], "answer": "1991"},
    {"q": "Python тилинин автору ким?", "options": ["Гвидо ван Россум", "Джеймс Гослинг", "Деннис Ритчи", "Линус Торвальдс"], "answer": "Гвидо ван Россум"},
    {"q": "Тизмедеги элементти индекси менен өчүрүүчү оператор?", "options": ["remove", "del", "clear", "pop_index"], "answer": "del"},
    {"q": "Тизменин эң акыркы элементинин индекси канча?", "options": ["0", "1", "-1", "last"], "answer": "-1"},
    {"q": "Шарттуу оператордогу 'же андай эмес болсо' сөзү кандай кыскартылат?", "options": ["elseif", "elif", "elsif", "else_if"], "answer": "elif"},
    {"q": "while циклы качан ишин токтотот?", "options": ["True болгондо", "False болгондо", "Биринчи айланууда", "Эч качан"], "answer": "False болгондо"},
    {"q": "Циклди дароо токтотуп чыгуучу оператор кайсы?", "options": ["continue", "stop", "break", "exit"], "answer": "break"},
    {"q": "Циклдин учурдагы кадамын өткөрүп жиберүүчү оператор?", "options": ["pass", "break", "skip", "continue"], "answer": "continue"},
    {"q": "Каталарды кармоо (иштетүү) үчүн кайсы блок колдонулат?", "options": ["try / except", "do / catch", "error / fix", "if / error"], "answer": "try / except"}
]

# 6. КИРҮҮ ЖАНА КАТТАЛУУ БЕТИ
if st.session_state["authenticated_user"] is None:
    st.title("🐍 Python Билимди Текшерүү Платформасы")
    tab1, tab2, tab3 = st.tabs(["🔑 Окуучу кирүү", "📝 Катталуу", "👨‍🏫 Мугалим панели"])
    
    with tab1:
        u_name = st.text_input("Логин", key="login_u")
        u_pass = st.text_input("Сыр сөз", type="password", key="login_p")
        if st.button("Кирүү"):
            user = verify_user(u_name, u_pass)
            if user:
                st.session_state["authenticated_user"] = user
                st.session_state["user_role"] = "student"
                st.session_state["stage"] = 1
                st.session_state["answers"] = {}
                st.rerun()
            else:
                st.error("Логин же сыр сөз туура эмес! Алгач 'Катталуу' бөлүмүнөн катталыңыз.")
                
    with tab2:
        r_fio = st.text_input("Аты-жөнүңүз (ФИО)")
        r_clazz = st.selectbox("Классыңыз", ["7-класс", "8-класс", "9-класс", "10-класс", "11-класс", "Студент"])
        r_user = st.text_input("Жаңы логин")
        r_pass = st.text_input("Жаңы сыр сөз", type="password")
        r_avatar = st.file_uploader("Аватар сүрөт жүктөө (WhatsApp сымал)", type=["png", "jpg", "jpeg"])
        
        if st.button("Катталуу"):
            if r_fio and r_user and r_pass:
                avatar_b64 = ""
                if r_avatar is not None:
                    avatar_b64 = base64.b64encode(r_avatar.read()).decode("utf-8")
                if register_user(r_fio, r_clazz, r_user, r_pass, avatar_b64):
