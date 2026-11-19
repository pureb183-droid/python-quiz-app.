import streamlit as st
import pandas as pd
import os
import base64
import time
from datetime import datetime

# 1. Веб-сайттын жөндөөлөрү
st.set_page_config(page_title="Python Тест & Аналитика", page_icon="🐍", layout="wide")

# 2. База файлдары
USERS_DB = "users_database.csv"
DB_FILE = "quiz_database.csv"
QUESTIONS_DB = "questions_database.csv"

# 3. Базаларды инициализациялоо
if not os.path.exists(USERS_DB):
    pd.DataFrame(columns=["fio", "clazz", "username", "password", "avatar_bytes"]).to_csv(USERS_DB, index=False)

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["ФИО", "Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли", "Этап_1", "Этап_2", "Этап_3"]).to_csv(DB_FILE, index=False)

DEFAULT_QUESTIONS = [
    # 1-этап (Башталгыч)
    {"stage": 1, "q": "Pythonдо кайсы өзгөрмөнүн аты ката жазылган?", "opt1": "my_var", "opt2": "_age", "opt3": "userAge", "opt4": "1st_place", "answer": "1st_place"},
    {"stage": 1, "q": "Pythonдо 5 / 2 туюнтмасы кандай типти кайтарат?", "opt1": "int", "opt2": "float", "opt3": "str", "opt4": "bool", "answer": "float"},
    {"stage": 1, "q": "print('A' * 2) буйругу экранга эмнени чыгарат?", "opt1": "A * 2", "opt2": "A 2", "opt3": "AA", "opt4": "Ката кетет", "answer": "AA"},
    {"stage": 1, "q": "input() аркылуу кирген маалымат демейки боюнча кайсы типте?", "opt1": "str", "opt2": "int", "opt3": "float", "opt4": "list", "answer": "str"},
    {"stage": 1, "q": "Коддогу бир саптуу комментарий кайсы символ менен башталат?", "opt1": "//", "opt2": "/*", "opt3": "#", "opt4": "--", "answer": "#"},
    # 2-этап (Орто)
    {"stage": 2, "q": "Тизменин аягына элемент кошуучу метод кайсы?", "opt1": "add()", "opt2": "append()", "opt3": "push()", "opt4": "insert()", "answer": "append()"},
    {"stage": 2, "q": "Шарттуу операторду (эгерде) ачуучу ачкыч сөз кайсы?", "opt1": "if", "opt2": "else", "opt3": "for", "opt4": "while", "answer": "if"},
    {"stage": 2, "q": "Барабарлыкты текшерүүчү операторду көрсөтүңүз?", "opt1": "=", "opt2": "===", "opt3": "is", "opt4": "==", "answer": "=="},
    {"stage": 2, "q": "for i in range(3): циклы канча жолу айланат?", "opt1": "2 жолу", "opt2": "3 жолу", "opt3": "4 жолу", "opt4": "Чексиз", "answer": "3 жолу"},
    {"stage": 2, "q": "Тизменин эң акыркы элементинин индекси канча?", "opt1": "0", "opt2": "1", "opt3": "-1", "opt4": "last", "answer": "-1"},
    # 3-этап (Татаал)
    {"stage": 3, "q": "Кайсы маалымат тиби өзгөрүлбөйт (immutable)?", "opt1": "list", "opt2": "dict", "opt3": "set", "opt4": "tuple", "answer": "tuple"},
    {"stage": 3, "q": "Сөздүктөн ачкычтарды алуучу метод кайсы?", "opt1": "keys()", "opt2": "values()", "opt3": "items()", "opt4": "get()", "answer": "keys()"},
    {"stage": 3, "q": "Жеке функция түзүү үчүн кайсы ачкыч сөз колдонулат?", "opt1": "function", "opt2": "fun", "opt3": "def", "opt4": "define", "answer": "def"},
    {"stage": 3, "q": "Циклди дароо токтотуп чыгуучу оператор кайсы?", "opt1": "continue", "opt2": "stop", "opt3": "break", "opt4": "exit", "answer": "break"},
    {"stage": 3, "q": "Каталарды кармоо үчүн кайсы блок колдонулат?", "opt1": "try / except", "opt2": "do / catch", "opt3": "error / fix", "opt4": "if / error", "answer": "try / except"},
]

if not os.path.exists(QUESTIONS_DB):
    pd.DataFrame(DEFAULT_QUESTIONS).to_csv(QUESTIONS_DB, index=False)

# 4. Жардамчы функциялар
def get_avatar_html(fio, avatar_b64, size=48):
    avatar_str = str(avatar_b64).strip()
    if avatar_str and avatar_str != "nan" and avatar_str != "None":
        return f'<img src="data:image/png;base64,{avatar_str}" style="width:{size}px;height:{size}px;border-radius:50%;object-fit:cover;border:2px solid #25D366;">'
    initials = "".join([w[0].upper() for w in str(fio).split()[:2]]) if fio else "?"
    return f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:#128C7E;color:white;display:inline-flex;align-items:center;justify-content:center;font-weight:bold;font-size:{int(size*0.4)}px;border:2px solid #25D366;">{initials}</div>'

def load_users():
    return pd.read_csv(USERS_DB)

def register_user(fio, clazz, username, password, avatar_bytes=""):
    df = load_users()
    if str(username) in df["username"].astype(str).values:
        return False
    new_user = pd.DataFrame([{"fio": fio, "clazz": clazz, "username": username, "password": password, "avatar_bytes": avatar_bytes}])
    pd.concat([df, new_user], ignore_index=True).to_csv(USERS_DB, index=False)
    return True

def verify_user(username, password):
    df = load_users()
    match = df[(df["username"].astype(str) == str(username)) & (df["password"].astype(str) == str(password))]
    return match.iloc[0].to_dict() if not match.empty else None

def load_questions():
    return pd.read_csv(QUESTIONS_DB)

def load_db():
    return pd.read_csv(DB_FILE)

def save_to_db(fio, clazz, time_str, score_str, percent, level, s1, s2, s3):
    df = load_db()
    if fio in df["ФИО"].values:
        df.loc[df["ФИО"] == fio, ["Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли", "Этап_1", "Этап_2", "Этап_3"]] = [clazz, time_str, score_str, percent, level, s1, s2, s3]
    else:
        new_row = pd.DataFrame([{"ФИО": fio, "Класс": clazz, "Убактысы": time_str, "Туура жооп": score_str, "Процент (%)": percent, "Деңгээли": level, "Этап_1": s1, "Этап_2": s2, "Этап_3": s3}])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# 5. CSS стилдер
st.markdown("""
<style>
    .main { background-color: #f4f6f9; }
    .card-3d {
        background: #ffffff; border-radius: 16px; padding: 20px; margin: 10px 0px;
        box-shadow: 4px 4px 12px rgba(0,0,0,0.08); text-align: center;
    }
    .card-title { color: #5a67d8; font-size: 15px; font-weight: bold; }
    .card-value { color: #2d3748; font-size: 28px; font-weight: 900; }
    .testpad-box {
        background: #ffffff; border-radius: 18px; padding: 30px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1); border-top: 6px solid #3182ce;
        max-width: 800px; margin: 20px auto;
    }
    .wa-row {
        display: flex; align-items: center; gap: 15px; background: white;
        padding: 12px 18px; border-radius: 12px; margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .timer-badge {
        background: #fff5f5; color: #c53030; border: 2px solid #feb2b2;
        padding: 10px 18px; border-radius: 10px; font-weight: bold; font-size: 18px;
        text-align: center; margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 6. Сессиялык абалдар
for key, val in [("authenticated_user", None), ("user_role", None), ("stage", 1), ("answers", {}), ("start_time", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

TEST_DURATION_SECONDS = 15 * 60  # 15 мүнөт таймер

# ==========================================
# 7. КИРҮҮ ЖАНА КАТТАЛУУ БЕТИ
# ==========================================
if st.session_state["authenticated_user"] is None:
    st.title("🐍 Python Онлайн Тест & Аналитика")
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
                st.session_state["start_time"] = time.time()
                st.rerun()
            else:
                st.error("Логин же сыр сөз туура эмес!")
                
    with tab2:
        r_fio = st.text_input("Аты-жөнүңүз (ФИО)")
        r_clazz = st.selectbox("Классыңыз", ["7-класс", "8-класс", "9-класс", "10-класс", "11-класс", "Студент"])
        r_user = st.text_input("Жаңы логин")
        r_pass = st.text_input("Жаңы сыр сөз", type="password")
        r_avatar = st.file_uploader("Аватар сүрөт жүктөө (WhatsApp сымал)", type=["png", "jpg", "jpeg"])
        
        if st.button("Катталуу"):
            if r_fio and r_user and r_pass:
                avatar_b64 = base64.b64encode(r_avatar.read()).decode("utf-8") if r_avatar else ""
                if register_user(r_fio, r_clazz, r_user, r_pass, avatar_b64):
                    st.success("Ийгиликтүү катталдыңыз! Эми 'Окуучу кирүү' бөлүмүнөн кириңиз.")
                else:
                    st.warning("Бул логин мурун алынган!")
            else:
                st.warning("Бардык негизги талааларды толтуруңуз!")

    with tab3:
        admin_pass = st.text_input("Мугалимдин сыр сөзү (демейки: admin123)", type="password")
        if st.button("Панелге кирүү"):
            if admin_pass == "admin123":
                st.session_state["authenticated_user"] = {"fio": "Мугалим"}
                st.session_state["user_role"] = "admin"
                st.rerun()
            else:
                st.error("Сыр сөз ката!")

# ==========================================
# 8. ОКУУЧУНУН ТЕСТ БЕТИ (3 ЭТАП + ТАЙМЕР + ONLINE TEST PAD ГРАФИКА)
# ==========================================
elif st.session_state["user_role"] == "student":
    user = st.session_state["authenticated_user"]
    q_df = load_questions()
    
    # Калган убакытты эсептөө
    elapsed = int(time.time() - st.session_state["start_time"])
    remaining = max(0, TEST_DURATION_SECONDS - elapsed)
    mins, secs = divmod(remaining, 60)

    with st.sidebar:
        st.markdown(f'<div style="text-align:center;">{get_avatar_html(user["fio"], user.get("avatar_bytes", ""), 90)}</div>', unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center;'>{user['fio']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>📚 {user['clazz']}</p>", unsafe_allow_html=True)
        
