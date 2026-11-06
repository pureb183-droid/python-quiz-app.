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
    {"q": "range(3) функциясы кайсы сандарды берет?", "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"], "answer": "0, 1, 2"},
    {"q": "Төмөнкүлөрдүн кайсынысы сөздүк (dictionary) болуп саналат?", "options": ["{1, 2}", "list", "(1, 2)", "{'a': 1}"], "answer": "{'a': 1}"},
    {"q": "Сөздүктөн ачкычтарды алуучу метод кайсы?", "options": ["keys()", "values()", "items()", "get()"], "answer": "keys()"},
    {"q": "Жеке функция түзүү үчүн кайсы ачкыч сөз колдонулат?", "options": ["function", "fun", "def", "define"], "answer": "def"},
    {"q": "Функциядан маани кайтаруучу ачкыч сөз?", "options": ["give", "return", "back", "exit"], "answer": "return"},
    {"q": "Python тили биринчи жолу кайсы жылы чыккан?", "options": ["1991", "2000", "1985", "1995"], "answer": "1991"},
    {"q": "Python тилинин автору ким?", "options": ["Гвидо ван Россум", "Джеймс Гослинг", "Деннис Ритчи", "Линус Торвальдс"], "answer": "Гвидо ван Россум"},
    {"q": "Тизмедеги элементти индекси менен өчүрүүчү оператор?", "options": ["remove", "del", "clear", "pop_index"], "answer": "del"},
    {"q": "Тизменин эң акыркы элементинин индекси канча?", "options": ["0", "1", "-1", "last"], "answer": "-1"},
    {"q": "Шарттуу оператордегу 'же андай эмес болсо' сөзү кандай кыскартылат?", "options": ["elseif", "elif", "elsif", "else_if"], "answer": "elif"},
    {"q": "while циклы качан ишин токтотот?", "options": ["True болгондо", "False болгондо", "Биринчи айланууда", "Эч качан"], "answer": "False болгондо"},
    {"q": "Циклди дароо токтотуп чыгуучу оператор кайсы?", "options": ["continue", "stop", "break", "exit"], "answer": "break"},
    {"q": "Циклдин кийинки айлануусуна дароо өткөрүүчү сөз?", "options": ["break", "continue", "pass", "next"], "answer": "continue"},
    {"q": "Эч кандай аракет аткарбаган бош оператор?", "options": ["None", "null", "pass", "void"], "answer": "pass"},
    {"q": "Төмөнкүлөрдүн кайсынысы топтом (set) болуп саналат?", "options": ["{1, 2, 3}", "list", "(1, 2, 3)", "set(1)"], "answer": "{1, 2, 3}"},
    {"q": "Топтомдордо (set) кайталануучу бирдей элементтер болобу?", "options": ["Ооба", "Жок", "Кээде гана", "Атайын шарт менен"], "answer": "Жок"},
    {"q": "Pythonдо файлды ачуучу камтылган функция?", "options": ["read()", "file()", "open()", "load()"], "answer": "open()"},
    {"q": "Файлга маалымат жазуу үчүн кайсы режим (mode) тандалат?", "options": ["'r'", "'w'", "'x'", "'a'"], "answer": "'w'"},
    {"q": "Каталар менен иштөө үчүн кайсы блоктор колдонулат?", "options": ["try-except", "if-else", "do-while", "catch-throw"], "answer": "try-except"},
    {"q": "Санды нөлгө бөлгөндө кандай ката келип чыгат?", "options": ["ValueError", "TypeError", "ZeroDivisionError", "IndexError"], "answer": "ZeroDivisionError"},
    {"q": "Сандын даражасын (кубатын) эсептөөчү оператор?", "options": ["^", "*", "**", "//"], "answer": "**"},
    {"q": "2 ** 3 туюнтмасынын жыйынтыгы канча болот?", "options": ["6", "8", "9", "5"], "answer": "8"},
    {"q": "Даяр китепканаларды кошуу үчүн кайсы сөз колдонулат?", "options": ["include", "require", "import", "using"], "answer": "import"},
    {"q": "Саптын бардык тамгаларын чоңойтуучу метод?", "options": ["upper()", "lower()", "capitalize()", "title()"], "answer": "upper()"},
    {"q": "Саптын башындагы жана аягындагы боштуктарды тазалоочу метод?", "options": ["clean()", "strip()", "replace()", "split()"], "answer": "strip()"},
    {"q": "Сапты белгилүү бир бөлгүч менен тизмеге бөлүүчү метод?", "options": ["join()", "split()", "divide()", "slice()"], "answer": "split()"},
    {"q": "Математикалык функцияларды камтыган стандарттык модуль?", "options": ["math", "random", "os", "sys"], "answer": "math"},
    {"q": "Кокустук (туш келди) сандар менен иштөөчү модуль?", "options": ["math", "random", "generate", "os"], "answer": "random"},
    {"q": "Объекттин маалымат тибин билүүчү функция кайсы?", "options": ["type()", "id()", "isinstance()", "typeof()"], "answer": "type()"},
    {"q": "Объекттин уникалдуу номердик кодун (ID) алуучу функция?", "options": ["type()", "id()", "hex()", "hash()"], "answer": "id()"},
    {"q": "Глобалдык өзгөрмөнү функция ичинде өзгөртүүчү сөз?", "options": ["global", "local", "public", "static"], "answer": "global"},
    {"q": "Pythonдо функция өзүн-өзү чакырса, бул процесс кандай аталат?", "options": ["Цикл", "Итерация", "Рекурсия", "Инкапсуляция"], "answer": "Рекурсия"},
    {"q": "Тизмени тескери тартипте жайгаштыруучу метод?", "options": ["sort()", "reverse()", "invert()", "flip()"], "answer": "reverse()"},
    {"q": "Тизмеде жок индексти чакырганда кандай ката чыгат?", "options": ["KeyError", "IndexError", "ValueError", "NameError"], "answer": "IndexError"}
]

def get_level(percentage):
    if percentage >= 85:
        return "Мыкты (Advanced)"
    elif percentage >= 65:
        return "Жакшы (Intermediate)"
    else:
        return "Канааттандырарлык (Beginner)"

# 6. Sidebar Навигациясы
st.sidebar.title("📌 Меню")

if st.session_state["authenticated_user"] is None:
    page_choice = st.sidebar.radio("Навигация", ["Кирүү / Катталуу", "Мугалим порталы"])
    if page_choice == "Кирүү / Катталуу":
        st.session_state["current_page"] = "login"
    else:
        st.session_state["current_page"] = "teacher_login"
else:
    st.sidebar.write(f"👤 **Колдонуучу:** {st.session_state['authenticated_user']['fio']}")
    page_choice = st.sidebar.radio("Навигация", ["Жеке кабинет жана Тест", "Чыгуу"])
    if page_choice == "Чыгуу":
        st.session_state["authenticated_user"] = None
        st.session_state["user_role"] = None
        st.session_state["current_page"] = "login"
        st.rerun()

# 7. Барактарды көрсөтүү логикасы
if st.session_state["current_page"] == "login":
    st.header("🔑 Окуучулардын порталы")
    tab1, tab2 = st.tabs(["Кирүү", "Катталуу"])
    
    with tab1:
        with st.form("login_form"):
            login_user = st.text_input("Логин (Колдонуучу аты):")
            login_pass = st.text_input("Сырсөз:", type="password")
            btn_login = st.form_submit_button("Кабинетке кирүү")
            if btn_login:
                user_data = verify_user(login_user, login_pass)
                if user_data:
                    st.session_state["authenticated_user"] = user_data
                    st.session_state["user_role"] = "student"
                    st.session_state["current_page"] = "student_dashboard"
                    st.success("Ийгиликтүү кирдиңиз!")
                    st.rerun()
                else:
                    st.error("Логин же сырсөз туура эмес!")

    with tab2:
        with st.form("reg_form"):
            reg_fio = st.text_input("Толук аты-жөнү (ФИО):")
            reg_clazz = st.text_input("Классы (мисалы: 9-А):")
            reg_user = st.text_input("Жаңы логин ойлоп табыңыз:")
            reg_pass = st.text_input("Жаңы сырсөз түзүңүз:", type="password")
            avatar_file = st.file_uploader("Аватарка үчүн сүрөт жүктөңүз:", type=["png", "jpg", "jpeg"])
            btn_reg = st.form_submit_button("Катталуу")
            
            if btn_reg:
                avatar_b64 = ""
                if avatar_file:
                    avatar_b64 = base64.b64encode(avatar_file.read()).decode('utf-8')
                if reg_fio and reg_clazz and reg_user and reg_pass:
                    if register_user(reg_fio, reg_clazz, reg_user, reg_pass, avatar_b64):
                        st.success("Катталуу ийгиликтүү өттү! Эми Кирүү өтмөгүнөн кириңиз.")
                    else:
                        st.error("Бул логин ээленген!")
                else:
                    st.warning("Бардык талааларды толтуруңуз!")

elif st.session_state["current_page"] == "student_dashboard" and st.session_state["authenticated_user"]:
    user_info = st.session_state["authenticated_user"]
    
    col_av, col_info = st.columns([1, 3])
    with col_av:
        if user_info.get("avatar_bytes") and isinstance(user_info["avatar_bytes"], str):
            st.markdown(f'<img src="data:image/png;base64,{user_info["avatar_bytes"]}" style="width:130px; height:130px; border-radius:50%; object-fit:cover; border: 3px solid #667eea;">', unsafe_allow_html=True)
        else:
            st.markdown('<div style="width:120px; height:120px; border-radius:50%; background:#cbd5e0; display:flex; align-items:center; justify-content:center; font-size:40px;">👤</div>', unsafe_allow_html=True)
    
    with col_info:
        st.markdown(f"### 📘 Кеңешбек Мырзабеков атындагы ЖББМ **{user_info['fio']}**")
        st.write(f"**Классы:** {user_info['clazz']}")
        st.write(f"**Статусу:** Активдүү окуучу")

    st.divider()
    st.header("📝 Python билимин текшерүү")

    with st.form("python_test"):
        st.subheader("50 суроолук тест")
        user_answers = []

        for i, question in enumerate(QUESTIONS):
            st.markdown(f"**{i + 1}. {question['q']}**")
            options = [x for x in question["options"] if str(x).strip()]
            answer = st.radio(
                f"Жоопту тандаңыз:",
                options,
                index=None,
                key=f"question_{i}",
                label_visibility="collapsed"
            )
            user_answers.append(answer)

        submitted = st.form_submit_button("ТЕСТТИ ЖӨНӨТҮҮ")

    if submitted:
        score = 0
        for i, question in enumerate(QUESTIONS):
            if user_answers[i] == question["answer"]:
                score += 1

        total = len(QUESTIONS)
        percent = round(score / total * 100, 2)
        level = get_level(percent)
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        answers_text = str(user_answers)

        save_to_db(
            user_info["fio"],
            user_info["clazz"],
            current_time,
            f"{score}/{total}",
            percent,
            level,
            "1-этап",
            answers_text
        )

        st.success("Тест ийгиликтүү аяктады!")
        st.subheader("🏆 Сиздин жыйынтыгыңыз")

        col1, col2, col3 = st.columns(3)
        col1.metric("Туура жооп", f"{score}/{total}")
        col2.metric("Пайыз", f"{percent}%")
        col3.metric("Деңгээли", level)

        st.progress(percent / 100)

        if percent >= 85:
            st.balloons()
            st.success("Мыкты! Сиз Python тилин жакшы билесиз!")
        elif percent >= 65:
            st.info("Жакшы! Дагы да машыгыңыз!")
        else:
            st.warning("Көбүрөөк даярданыңыз!")

elif st.session_state["current_page"] == "teacher_login":
    st.header("🔐 Мугалимдин жеке кабинети")
    
    if st.session_state.get("teacher_logged_in"):
        st.success("Кош келиңиз, Назира Асановна!")
        
        df = load_db()

        if not df.empty:
            st.subheader("📊 Окуучулардын жыйынтыгы")

            classes = sorted(df["Класс"].dropna().astype(str).unique())
            selected_class = st.selectbox("Классты тандаңыз:", ["Бардык класстар"] + classes)

            if selected_class == "Бардык класстар":
                result = df.copy()
            else:
                result = df[df["Класс"].astype(str) == selected_class].copy()

            result = result.sort_values(by=["Класс", "ФИО"])

            col1, col2, col3 = st.columns(3)
            col1.metric("Окуучулар", len(result))
            col2.metric("Орточо пайыз", f"{result['Процент (%)'].mean():.1f}%")
            col3.metric(
                "Мыкты деңгээл",
                len(result[result["Деңгээли"].str.contains("Advanced", na=False)])
            )

            st.dataframe(result, use_container_width=True, hide_index=True)

            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                result.to_excel(writer, index=False, sheet_name="Жыйынтыктар")

            st.download_button(
                "📥 Excel жүктөп алуу",
                data=buffer.getvalue(),
                file_name="Okuu_jyyyntygy.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.divider()

            st.subheader("🏆 Сертификат берүү")

            names = result["ФИО"].dropna().unique().tolist()

            if names:
                name = st.selectbox("Окуучуну тандаңыз:", names)
                student = result[result["ФИО"] == name].iloc[0]

                fio_cert = html.escape(str(student["ФИО"]))
                class_cert = html.escape(str(student["Класс"]))
                percent_cert = html.escape(str(student["Процент (%)"]))
                level_cert = html.escape(str(student["Деңгээли"]))

                cert = f"""
<html>
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
    body {{
        font-family: 'Times New Roman', serif;
        background: #f4f4f4;
        padding: 20px;
    }}
    .cert-container {{
        border: 15px solid #0088cc;
        padding: 10px;
        background: #fff;
        max-width: 900px;
        margin: auto;
        box-shadow: 0 0 20px rgba(0,0,0,0.2);
    }}
    .cert-inner {{
        border: 3px double #0088cc;
        padding: 30px;
        text-align: center;
        position: relative;
        background: radial-gradient(circle, #ffffff 60%, #e6f7ff 100%);
    }}
    .header-title {{
        font-size: 16px;
        font-weight: bold;
        color: #1a365d;
        text-transform: uppercase;
        margin-bottom: 5px;
    }}
    .sub-header {{
        font-size: 14px;
        color: #2b6cb0;
        font-weight: bold;
        margin-bottom: 20px;
    }}
    .cert-main-title {{
        font-size: 48px;
        color: #0056b3;
        font-weight: bold;
        letter-spacing: 4px;
        margin: 15px 0;
    }}
    .student-name {{
        font-size: 32px;
        color: #2c5282;
        font-style: italic;
        border-bottom: 2px solid #2c5282;
        display: inline-block;
        padding: 0 20px 5px 20px;
        margin: 15px 0;
    }}
    .desc {{
        font-size: 16px;
        line-height: 1.6;
        color: #2d3748;
        max-width: 750px;
        margin: 0 auto;
    }}
    .footer-table {{
        width: 100%;
        margin-top: 40px;
        font-size: 14px;
    }}
</style>
</head>
<body>

<div class="cert-container">
    <div class="cert-inner">
        <div class="header-title">КЫРГЫЗ РЕСПУБЛИКАСЫНЫН БИЛИМ БЕРҮҮ ЖАНА ИЛИМ МИНИСТРЛИГИ</div>
        <div class="sub-header">КЕҢЕШБЕК МЫРЗАБЕКОВ АТЫНДАГЫ ЖАЛПЫ БИЛИМ БЕРҮҮ МЕКТЕБИ</div>
        
        <div class="cert-main-title">СЕРТИФИКАТ</div>
        
        <p style="font-size:18px;">Бул сертификат салтанаттуу түрдө берилет:</p>
        <div class="student-name">{fio_cert}</div>
        <p><b>{class_cert}</b> классынын окуучусуна</p>
        
        <div class="desc">
            «Python программалоо тили боюнча билимди текшерүү жана практикалык көндүмдөр» курсун 
            ийгиликтүү аяктагандыгы үчүн. <br>
            Жыйынтык: <b>{percent_cert}%</b> | Деңгээли: <b>{level_cert}</b>
        </div>

        <table class="footer-table">
            <tr>
                <td style="text-align:left; width:35%;">
                    <b>Директор:</b><br>
                    Арыстанбекова М. А.<br><br>
                    <i>Колу: ___________</i>
                </td>
                <td style="text-align:center; width:30%;">
                    <div style="border:1px solid #ccc; padding:5px; display:inline-block;">
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=Certificate-{fio_cert}" width="80" height="80">
                    </div>
                    <br><small>№ 24630</small>
                </td>
                <td style="text-align:right; width:35%;">
                    <b>Текшерүүчү мугалим:</b><br>
                    Бейшеналиева Назира Асановна<br><br>
                    <i>Колу: ___________</i>
                </td>
            </tr>
        </table>
    </div>
</div>

</body>
</html>
"""

                st.download_button(
                    "🏆 Сертификатты жүктөп алуу",
                    data=cert.encode("utf-8"),
                    file_name="Sertifikat.html",
                    mime="text/html"
                )

        else:
            st.info("Азырынча окуучулар тест тапшыра элек.")
            
        st.divider()
        if st.button("🚪 Мугалим кабинетинен чыгуу"):
            st.session_state["teacher_logged_in"] = False
            st.rerun()

    else:
        teacher_pass = st.text_input("Мугалимдин сырсөзүн киргизиңиз:", type="password")
        if st.button("Кабинетке кирүү"):
            if teacher_pass == "nazira202!":
                st.session_state["teacher_logged_in"] = True
                st.rerun()
            else:
                st.error("Сырсөз туура эмес!")

# 8. Автордук футер
st.divider()
st.markdown("""
<div style="
    text-align: center;
    padding: 30px;
    margin-top: 40px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 10px;
    color: white;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
">
    <h3>Автор:</h3>
    <h4>Бейшеналиева Назира Асановна</h4>
    <p>Python</p>
    <p>© 2026 Бардык укуктар корголгон</p>
</div>
""", unsafe_allow_html=True)
