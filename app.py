import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Баракчанын негизги орнотуулары
st.set_page_config(
    page_title="Python Тести", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Түстөр жана стилдер
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #4CAF50; color: white; border-radius: 8px;
        padding: 10px 24px; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #45a049; }
    .cert-box {
        border: 10px double #2c3e50; padding: 40px; text-align: center;
        background-color: #ffffff; border-radius: 15px;
    }
    .stage-header {
        background-color: #e3f2fd; padding: 12px; border-radius: 8px;
        color: #0d47a1; font-weight: bold; margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Жыйынтыктарды сактай турган CSV файлдык база
DB_FILE = "quiz_database.csv"
if not os.path.exists(DB_FILE):
    columns_list = ["ФИО", "Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли", "Учурдагы_Этап", "Жооптор"]
    df_empty = pd.DataFrame(columns=columns_list)
    df_empty.to_csv(DB_FILE, index=False)

def load_db():
    return pd.read_csv(DB_FILE)

def save_to_db(fio, clazz, time_str, score_str, percent, level, stage, answers_str):
    df = load_db()
    if fio in df["ФИО"].values:
        df.loc[df["ФИО"] == fio, ["Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли", "Учурдагы_Этап", "Жооптор"]] = [clazz, time_str, score_str, percent, level, stage, answers_str]
    else:
        new_row = pd.DataFrame([{
            "ФИО": fio, "Класс": clazz, "Убактысы": time_str,
            "Туура жооп": score_str, "Процент (%)": percent, "Деңгээли": level,
            "Учурдагы_Этап": stage, "Жооптор": answers_str
        }])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# 50 суроонун базасы
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
    {"q": "Төмөнкүлөрдүн кайсынысы сөздүк (dictionary) болуп саналат?", "options": ["{1, 2}", "", "(1, 2)", "{'a': 1}"], "answer": "{'a': 1}"},
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
    
    {"q": "Төмөнкүлөрдүн кайсынысы топтом (set) болуп саналат?", "options": ["{1, 2, 3}", "", "(1, 2, 3)", "set(1)"], "answer": "{1, 2, 3}"},
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
    {"q": "Функция өзүн-өзү чакырса, бул процесс кандай аталат?", "options": ["Цикл", "Итерация", "Рекурсия", "Инкапсуляция"], "answer": "Рекурсия"},
    {"q": "Тизмени тескери тартипте жайгаштыруучу метод?", "options": ["sort()", "reverse()", "invert()", "flip()"], "answer": "reverse()"},
    {"q": "Тизмеде жок индексти чакырганда кандай ката чыгат?", "options": ["KeyError", "IndexError", "ValueError", "NameError"], "answer": "IndexError"}
]

def get_level(percentage):
    if percentage >= 85: return "Мыкты (Advanced)"
    elif percentage >= 65: return "Жакшы (Intermediate)"
    elif percentage >= 40: return "Канааттандырарлык (Beginner)"
    else: return "Төмөн (A1)"

# Башкаруу панели
page = st.sidebar.radio("Панелди тандаңыз:", ["Окуучулар үчүн (Тест)", "Мугалим үчүн (Жыйынтык тактасы)"])

# Глобалдык эстутумду даярдоо
if "user_fio" not in st.session_state:
    st.session_state.user_fio = None
if "user_class" not in st.session_state:
    st.session_state.user_class = None
if "current_stage" not in st.session_state:
    st.session_state.current_stage = 1
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# ----------------- ОКУУЧУНУН ПАНЕЛИ -----------------
if page == "Окуучулар үчүн (Тест)":
    st.title("🎓 Python Программалоо Тили Боюнча Тест системасы")
    
    if st.session_state.user_fio is None:
        st.subheader("📝 Тестке катталуу / Кирүү")
        l_name = st.text_input("Фамилияңыз:").strip()
        f_name = st.text_input("Атыңыз:").strip()
        m_name = st.text_input("Атасынын аты (болсо):").strip()
        student_class = st.text_input("Классыңыз (мисалы: 9-А, 11-Б):").strip()
        
        if st.button("🚀 Тестти баштоо / Улантуу"):
            if l_name and f_name and student_class:
