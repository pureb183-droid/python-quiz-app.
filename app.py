import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Баракчанын дизайны жана жөндөөлөрү
st.set_page_config(page_title="Python Базалык Тести", layout="wide", initial_sidebar_state="expanded")

# CSS стилдери - сайтты кооздоо үчүн
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #4CAF50; color: white; border-radius: 8px;
        padding: 10px 24px; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #45a049; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .cert-box {
        border: 10px double #2c3e50; padding: 40px; text-align: center;
        background-color: #ffffff; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    .stage-header {
        background-color: #e3f2fd; padding: 12px; border-radius: 8px;
        color: #0d47a1; font-weight: bold; margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Туруктуу маалымат базасы (CSV файл) түзүү
DB_FILE = "quiz_database.csv"
if not os.path.exists(DB_FILE):
    df_empty = pd.DataFrame(columns=["ФИО", "Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли", "Учурдагы_Этап", "Жооптор"])
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

# 50 суроодон турган база
QUESTIONS = [
    {"q": "Төмөндөгүлөрдүн кайсынысы Pythonдо өзгөрмөнүн аты катары туура эмес?", "options": ["my_var", "_age", "userAge", "1st_place"], "answer": "1st_place"},
    {"q": "Pythonдо 5 / 2 туюнтмасы кандай маалымат тибин кайтарат?", "options": ["int", "float", "str", "bool"], "answer": "float"},
    {"q": "print('Python' * 2) буйругу экранга эмнени чыгарат?", "options": ["Python * 2", "Python 2", "PythonPython", "Ката кетет"], "answer": "PythonPython"},
    {"q": "Тизменин (list) аягына жаңы элемент кошуу үчүн кайсы метод колдонулат?", "options": ["add()", "append()", "push()", "insert_end()"], "answer": "append()"},
    {"q": "print('Hello', 'World', sep='-') буйругу экранга эмнени чыгарат?", "options": ["Hello World", "Hello,World", "Hello-World", "HelloWorld"], "answer": "Hello-World"},
    {"q": "Pythonдо input() функциясы аркылуу киргизилген маалымат демейки боюнча кайсы типте сакталат?", "options": ["str", "int", "float", "list"], "answer": "str"},
    {"q": "len() функциясы кандай маанини кайтарат?", "options": ["3", "40", "4", "10"], "answer": "4"},
    {"q": "Pythonдо 17 % 5 туюнтмасынын натыйжасы эмнеге барабар?", "options": ["3", "2", "3.4", "5"], "answer": "2"},
    {"q": "x = 10; if x > 10: print('A') else: print('B') кодунун жыйынтыгы эмне болот?", "options": ["A", "B", "AB", "Эч нерсе чыкпайт"], "answer": "B"},
    {"q": "Pythonдо эки маанинин барабарлыгын текшерүү үчүн кайсы оператор колдонулат?", "options": ["=", "===", "is equal", "=="], "answer": "=="},
    
    {"q": "Pythonдо логикалык 'ЖАНА' оператору кайсы сөз менен жазылат?", "options": ["&&", "and", "AND", "conj"], "answer": "and"},
    {"q": "Pythonдо логикалык 'ЖЕ' оператору кайсы?", "options": ["||", "or", "OR", "disj"], "answer": "or"},
    {"q": "Төмөнкүлөрдүн кайсынысы өзгөрүлбөс (immutable) маалымат тибине кирет?", "options": ["list", "dict", "set", "tuple"], "answer": "tuple"},
    {"q": "Сапты бүтүн санга айландыруу үчүн кайсы функция колдонулат?", "options": ["str()", "int()", "float()", "to_integer()"], "answer": "int()"},
    {"q": "Коддогу комментарийлер кайсы символ менен башталат?", "options": ["//", "/*", "#", "--"], "answer": "#"},
    {"q": "for i in range(3): циклы канча жолу аткарылат?", "options": ["2 жолу", "3 жолу", "4 жолу", "Чексиз"], "answer": "3 жолу"},
    {"q": "range(3) функциясы кайсы сандардын ырааттуулугун берет?", "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"], "answer": "0, 1, 2"},
    {"q": "Төмөнкүлөрдүн кайсынысы Pythonдо сөздүк (dictionary) болуп саналат?", "options": ["{1, 2}", "", "(1, 2)", "{'a': 1}"], "answer": "{'a': 1}"},
    {"q": "Сөздүктөн (dict) ачкычтардын тизмесин алуу үчүн кайсы метод колдонулат?", "options": ["keys()", "values()", "items()", "get()"], "answer": "keys()"},
    {"q": "Функция түзүү үчүн кайсы ачкыч сөз колдонулат?", "options": ["function", "fun", "def", "define"], "answer": "def"},
    
    {"q": "Функциядан маани кайтаруу үчүн кайсы ачкыч сөз колдонулат?", "options": ["give", "return", "back", "exit"], "answer": "return"},
    {"q": "Python тили кайсы жылы жарык көргөн?", "options": ["1991", "2000", "1985", "1995"], "answer": "1991"},
    {"q": "Python тилинин автору ким?", "options": ["Гвидо ван Россум", "Джеймс Гослинг", "Бьерн Страуструп", "Деннис Ритчи"], "answer": "Гвидо ван Россум"},
    {"q": "Тизмедеги элементти индекси боюнча өчүрүү үчүн кайсы оператор же метод колдонулат?", "options": ["remove()", "del", "clear()", "discard()"], "answer": "del"},
    {"q": "Тизменин эң акыркы элементинин индекси канчага барабар?", "options": ["0", "1", "-1", "len(list)"], "answer": "-1"},
    {"q": "Pythonдо шарттуу оператордун ичиндеги 'эгерде андай эмес болсо' (else if) сөзү кантип кыскартылат?", "options": ["elseif", "elif", "elsif", "else_if"], "answer": "elif"},
    {"q": "while циклы качан токтойт?", "options": ["Шарт True болгондо", "Шарт False болгондо", "Дароо биринчи айланууда", "Эч качан токтобойт"], "answer": "Шарт False болгондо"},
    {"q": "Циклди мөөнөтүнөн мурда токтотуу үчүн кайсы ачкыч сөз колдонулат?", "options": ["continue", "stop", "break", "exit"], "answer": "break"},
    {"q": "Циклдин кийинки айлануусуна (итерациясына) дароо өтүү үчүн эмне колдонулат?", "options": ["break", "continue", "pass", "next"], "answer": "continue"},
    {"q": "Эч кандай аракет аткарбаган бош оператор кайсы?", "options": ["None", "null", "pass", "void"], "answer": "pass"},
    
    {"q": "Төмөнкүлөрдүн кайсынысы топтом (set) болуп саналат?", "options": ["{1, 2, 3}", "", "(1, 2, 3)", "set(1,2)"], "answer": "{1, 2, 3}"},
    {"q": "Топтомдордо (set) кайталануучу элементтер болушу мүмкүнбү?", "options": ["Ооба", "Жок", "Кээде гана", "Атайын жөндөө менен гана"], "answer": "Жок"},
    {"q": "Pythonдо файлды ачуу үчүн кайсы камтылган функция колдонулат?", "options": ["read()", "file()", "open()", "load()"], "answer": "open()"},
    {"q": "Файлга маалымат жазуу үчүн open() функциясында кайсы режим (mode) колдонулат?", "options": ["'r'", "'w'", "'x'", "'rb'"], "answer": "'w'"},
    {"q": "Pythonдо каталар менен иштөө үчүн (Exception handling) кайсы блоктор колдонулат?", "options": ["try-except", "if-else", "do-while", "catch-throw"], "answer": "try-except"},
    {"q": "Нөлгө бөлүү катасы катталганда кайсы өзгөчөлүк (Exception) келип чыгат?", "options": ["ValueError", "TypeError", "ZeroDivisionError", "IndexError"], "answer": "ZeroDivisionError"},
    {"q": "Сандын даражасын эсептөө үчүн кайсы оператор колдонулат?", "options": ["^", "*", "**", "//"], "answer": "**"},
    {"q": "2 ** 3 туюнтмасынын жыйынтыгы канча?", "options": ["6", "8", "9", "5"], "answer": "8"},
    {"q": "Модулдарды жана китепканаларды кошуу үчүн кайсы ачкыч сөз колдонулат?", "options": ["include", "require", "import", "using"], "answer": "import"},
    {"q": "Саптын бардык тамгаларын чоңойтуу үчүн кайсы метод колдонулат?", "options": ["upper()", "lower()", "capitalize()", "title()"], "answer": "upper()"},
    
    {"q": "Саптын башындагы жана аягындагы боштуктарды (пробелдерди) өчүрүүчү метод?", "options": ["clean()", "strip()", "replace()", "split()"], "answer": "strip()"},
    {"q": "Сапты тизмеге бөлүү үчүн кайсы метод колдонулат?", "options": ["join()", "split()", "divide()", "slice()"], "answer": "split()"},
    {"q": "Төмөнкүлөрдүн кайсынысы математикалык функцияларды камтыган стандарттык модуль?", "options": ["math", "random", "os", "sys"], "answer": "math"},
    {"q": "Кокустук сандар менен иштөөчү модуль кандай аталат?", "options": ["math", "random", "generate", "os"], "answer": "random"},
    {"q": "Маалыматтын тибин (класс атын) билүү үчүн кайсы функция колдонулат?", "options": ["type()", "id()", "isinstance()", "typeof()"], "answer": "type()"},
    {"q": "Объекттин уникалдуу идентификаторун алуу үчүн кайсы функция колдонулат?", "options": ["type()", "id()", "hex()", "hash()"], "answer": "id()"},
    {"q": "Глобалдык өзгөрмөнү функциянын ичинде өзгөртүү үчүн кайсы ачкыч сөз колдонулат?", "options": ["global", "local", "public", "static"], "answer": "global"},
    {"q": "Pythonдо функция өзүн-өзү чакырса, бул процесс кандай аталат?", "options": ["Цикл", "Итерация", "Рекурсия", "Инкапсуляция"], "answer": "Рекурсия"},
    {"q": "Тизмени тескери тартипте жайгаштыруу үчүн кайсы метод колдонулат?", "options": ["sort()", "reverse()", "invert()", "flip()"], "answer": "reverse()"},
    {"q": "Индекс табылбай калганда тизмеде кандай ката пайда болот?", "options": ["KeyError", "IndexError", "ValueError", "NameError"], "answer": "IndexError"}
]

def get_level(percentage):
    if percentage >= 85: return "Мыкты (Advanced)"
    elif percentage >= 65: return "Жакшы (Intermediate)"
    elif percentage >= 40: return "Канааттандырарлык (Beginner)"
    else: return "Төмөн (A1)"

# Капталдагы меню
page = st.sidebar.radio("Панелди тандаңыз:", ["Окуучулар үчүн (Тест)", "Мугалим үчүн (Жыйынтык тактасы)"])

# ----------------- ОКУУЧУНУН ПАНЕЛИ -----------------
if page == "Окуучулар үчүн (Тест)":

