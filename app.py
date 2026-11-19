import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# 1. Барактын жөндөөлөрү
st.set_page_config(page_title="Python Тест", page_icon="🐍", layout="wide")

# 2. Эс тутумду (Session State) даярдоо
if "user" not in st.session_state:
    st.session_state["user"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
if "stage" not in st.session_state:
    st.session_state["stage"] = 1
if "answers" not in st.session_state:
    st.session_state["answers"] = {}

# 3. Дизайн (CSS)
st.markdown("""
<style>
    .main { background-color: #f4f6f9; }
    .card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08); text-align: center; margin-bottom: 15px;
    }
    .student-item {
        display: flex; align-items: center; background: white;
        padding: 12px 18px; border-radius: 12px; margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .avatar {
        width: 50px; height: 50px; border-radius: 50%;
        object-fit: cover; margin-right: 15px; border: 2px solid #25D366;
    }
    .cert {
        border: 10px double #4a5568; padding: 30px; text-align: center;
        background: white; border-radius: 15px; max-width: 700px; margin: 20px auto;
    }
</style>
""", unsafe_allow_html=True)

# 4. Маалымат базасы (CSV)
USERS_FILE = "users.csv"
RESULTS_FILE = "results.csv"

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["fio", "clazz", "username", "password", "avatar"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(RESULTS_FILE):
    pd.DataFrame(columns=["ФИО", "Username", "Класс", "Убактысы", "Упай", "Процент", "Деңгээли"]).to_csv(RESULTS_FILE, index=False)

def get_users():
    try:
        return pd.read_csv(USERS_FILE)
    except Exception:
        return pd.DataFrame(columns=["fio", "clazz", "username", "password", "avatar"])

def get_results():
    try:
        return pd.read_csv(RESULTS_FILE)
    except Exception:
        return pd.DataFrame(columns=["ФИО", "Username", "Класс", "Убактысы", "Упай", "Процент", "Деңгээли"])

# 5. Суроолор (30 суроо = 3 этап x 10 суроо)
QUESTIONS = [
    {"q": "Pythonдо кайсы өзгөрмөнүн аты ката жазылган?", "options": ["my_var", "_age", "userAge", "1st_place"], "answer": "1st_place"},
    {"q": "Pythonдо 5 / 2 туюнтмасы кандай типти кайтарат?", "options": ["int", "float", "str", "bool"], "answer": "float"},
    {"q": "print('A' * 2) буйругу экранга эмнени чыгарат?", "options": ["A * 2", "A 2", "AA", "Ката кетет"], "answer": "AA"},
    {"q": "Тизменин аягына элемент кошуучу метод кайсы?", "options": ["add()", "append()", "push()", "insert()"], "answer": "append()"},
    {"q": "print('A', 'B', sep='-') эмнени чыгарат?", "options": ["A B", "A,B", "A-B", "AB"], "answer": "A-B"},
    {"q": "input() аркылуу кирген маалымат кайсы типте болот?", "options": ["str", "int", "float", "list"], "answer": "str"},
    {"q": "len('ABC') функциясы кандай маани берет?", "options": ["1", "2", "3", "0"], "answer": "3"},
    {"q": "Pythonдо 17 % 5 туюнтмасынын калдыгы канча?", "options": ["3", "2", "1", "5"], "answer": "2"},
    {"q": "Шарттуу операторду ачуучу ачкыч сөз кайсы?", "options": ["if", "else", "for", "while"], "answer": "if"},
    {"q": "Барабарлыкты текшерүүчү операторду көрсөтүңүз?", "options": ["=", "===", "is", "=="], "answer": "=="},

    {"q": "Pythonдо логикалык 'ЖАНА' оператору кайсы?", "options": ["&&", "and", "AND", "not"], "answer": "and"},
    {"q": "Pythonдо логикалык 'ЖЕ' оператору кайсы?", "options": ["||", "or", "OR", "xor"], "answer": "or"},
    {"q": "Кайсы маалымат тиби өзгөрүлбөйт (immutable)?", "options": ["list", "dict", "set", "tuple"], "answer": "tuple"},
    {"q": "Сапты бүтүн санга айландыруучу функция?", "options": ["str()", "int()", "float()", "num()"], "answer": "int()"},
    {"q": "Бир саптуу комментарий кайсы символ менен башталат?", "options": ["//", "/*", "#", "--"], "answer": "#"},
    {"q": "for i in range(3): циклы канча жолу айланат?", "options": ["2 жолу", "3 жолу", "4 жолу", "Чексиз"], "answer": "3 жолу"},
    {"q": "range(3) функциясы кайсы сандарды берет?", "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"], "answer": "0, 1, 2"},
    {"q": "Кайсынысы сөздүк (dictionary) болуп саналат?", "options": ["{1, 2}", "list(1, 2)", "(1, 2)", "{'a': 1}"], "answer": "{'a': 1}"},
    {"q": "Сөздүктөн ачкычтарды алуучу метод кайсы?", "options": ["keys()", "values()", "items()", "get()"], "answer": "keys()"},
    {"q": "Функция түзүү үчүн кайсы ачкыч сөз колдонулат?", "options": ["function", "fun", "def", "define"], "answer": "def"},

    {"q": "Функциядан маани кайтаруучу ачкыч сөз?", "options": ["give", "return", "back", "exit"], "answer": "return"},
    {"q": "Python тили кайсы жылы чыккан?", "options": ["1991", "2000", "1985", "1995"], "answer": "1991"},
    {"q": "Python тилинин автору ким?", "options": ["Гвидо ван Россум", "Джеймс Гослинг", "Деннис Ритчи", "Линус Торвальдс"], "answer": "Гвидо ван Россум"},
    {"q": "Тизмедеги элементти индекси менен өчүрүүчү оператор?", "options": ["remove", "del", "clear", "pop_index"], "answer": "del"},
    {"q": "Тизменин эң акыркы элементинин индекси канча?", "options": ["0", "1", "-1", "last"], "answer": "-1"},
    {"q": "'Же андай эмес болсо' сөзү кандай кыскартылат?", "options": ["elseif", "elif", "elsif", "else_if"], "answer": "elif"},
    {"q": "while циклы качан ишин токтотот?", "options": ["True болгондо", "False болгондо", "Биринчи айланууда", "Эч качан"], "answer": "False болгондо"},
    {"q": "Циклди дароо токтотуп чыгуучу оператор кайсы?", "options": ["continue", "stop", "break", "exit"], "answer": "break"},
    {"q": "Циклдин учурдагы кадамын өткөрүп жиберүүчү оператор?", "options": ["pass", "break", "skip", "continue"], "answer": "continue"},
    {"q": "Каталарды кармоо үчүн кайсы блок колдонулат?", "options": ["try / except", "do / catch", "error / fix", "if / error"], "answer": "try / except"}
]

# ==========================================
# АБАЛ 1: КИРҮҮ ЖАНА КАТТАЛУУ БАРАГЫ
# ==========================================
if st.session_state["role"] is None:
    st.title("🐍 Python Онлайн Тест Платформасы")
    t1, t2, t3 = st.tabs(["🔑 Окуучу кирүү", "📝 Катталуу", "👨‍🏫 Мугалим панели"])

    with t1:
        login_u = st.text_input("Логин")
        login_p = st.text_input("Сыр сөз", type="password")
        if st.button("Кирүү"):
            df_u = get_users()
            found = df_u[(df_u["username"].astype(str) == str(login_u).strip()) & (df_u["password"].astype(str) == str(login_p).strip())]
            user_dict = next(iter(found.to_dict(orient="records")), None)
            if user_dict is not None:
                st.session_state["user"] = user_dict
                st.session_state["role"] = "student"
                st.session_state["stage"] = 1
                st.session_state["answers"] = {}
                st.rerun()
            else:
                st.error("Логин же сыр сөз туура эмес! Алгач 'Катталуу' бөлүмүнөн катталыңыз.")

    with t2:
        r_fio = st.text_input("Аты-жөнүңүз (ФИО)")
        r_clazz = st.selectbox("Классыңыз", ["7-класс", "8-класс", "9-класс", "10-класс", "11-класс", "Студент"])
        r_user = st.text_input("Жаңы логин түзүңүз")
        r_pass = st.text_input("Сыр сөз түзүңүз", type="password")
        r_img = st.file_uploader("Аватар сүрөт (WhatsApp сымал)", type=["png", "jpg", "jpeg"])
        if st.button("Катталуу"):
            if r_fio and r_user and r_pass:
                df_u = get_users()
                if str(r_user).strip() in df_u["username"].astype(str).values:
                    st.warning("Бул логин мурун алынган, башка логин жазыңыз.")
                else:
                    img_b64 = base64.b64encode(r_img.read()).decode("utf-8") if r_img else ""
                    new_row = pd.DataFrame([{"fio": r_fio.strip(), "clazz": r_clazz, "username": r_user.strip(), "password": r_pass.strip(), "avatar": img_b64}])
                    pd.concat([df_u, new_row], ignore_index=True).to_csv(USERS_FILE, index=False)
                    st.success("Каттоо ийгиликтүү өттү! Эми 'Окуучу кирүү' бөлүмүнө өтүп кириңиз.")
            else:
                st.warning("Бардык талааларды толтуруңуз!")

    with t3:
        admin_p = st.text_input("Мугалимдин сыр сөзү (admin123)", type="password")
        if st.button("Мугалим панелине кирүү"):
            if admin_p == "admin123":
                st.session_state["role"] = "admin"
                st.rerun()
            else:
                st.error("Сыр сөз туура эмес!")

# ==========================================
# АБАЛ 2: ОКУУЧУНУН 3 ЭТАПТУУ ТЕСТ БАРАГЫ
# ==========================================
elif st.session_state["role"] == "student":
    user = st.session_state["user"]

    with st.sidebar:
        av = str(user.get("avatar", ""))
        if av and av != "nan" and len(av) > 20:
            st.markdown(f'<img src="data:image/png;base64,{av}" style="width:85px;height:85px;border-radius:50%;object-fit:cover;border:3px solid #25D366;">', unsafe_allow_html=True)
        st.subheader(f"👤 {user.get('fio', '')}")
        st.write(f"📚 Класс: **{user.get('clazz', '')}**")
        if st.button("🚪 Чыгуу"):
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.rerun()

    st.title("📝 Python боюнча 3 этаптуу тест")
    stage = st.session_state["stage"]

    if stage <= 3:
        start = (stage - 1) * 10
        end = stage * 10
        st.info(f"🚀 **{stage}-этап** (Суроолор: {start + 1} — {end})")

        with st.form(f"form_stage_{stage}"):
            for i in range(start, end):
                q_item = QUESTIONS[i]
                st.markdown(f"**{i + 1}. {q_item['q']}**")
                ans = st.radio("Жоопту тандаңыз:", q_item["options"], key=f"radio_{i}", index=None)
                st.session_state["answers"][i] = ans
