import streamlit as st
import pandas as pd
import os
import io
import html
from datetime import datetime

# Негизги жөндөөлөр
st.set_page_config(page_title="Python тести & Аналитика", layout="wide")

# Сайтты толугу менен 3D жана кооз түстөр менен жасалгалоо (CSS)
st.markdown("""
<style>
    /* Негизги фон */
    .main { background-color: #f0f2f6; }
    
    /* 3D Көлөмдүү Карточкалар (Неоморфизм) */
    .card-3d {
        background: #ffffff;
        border-radius: 16px;
        padding: 25px;
        margin: 10px 0px;
        box-shadow: 6px 6px 8px #c5c9d1, -6px -6px 12px #ffffff;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .card-title { color: #5a67d8; font-size: 16px; font-weight: bold; margin-bottom: 5px; }
    .card-value { color: #2d3748; font-size: 32px; font-weight: 900; }
    
    /* Кооз Кнопкалар */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border-radius: 12px; padding: 12px 28px;
        font-weight: bold; border: none;
        box-shadow: 3px 3px 8px #b8b8b8, -3px -3px 8px #ffffff;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 5px 5px 12px #9c9c9c, -5px -5px 12px #ffffff;
    }
    
    /* Сертификаттын дизайны */
    .cert-box {
        border: 12px double #4a5568; padding: 45px; text-align: center;
        background: #ffffff; border-radius: 20px;
        box-shadow: 10px 10px 25px rgba(0,0,0,0.1);
        max-width: 750px; margin: 30px auto;
    }
    .stage-header {
        background: linear-gradient(90deg, #ebf8ff 0%, #bee3f8 100%);
        padding: 15px; border-radius: 10px;
        color: #2b6cb0; font-weight: bold; margin-bottom: 25px;
        border-left: 5px solid #3182ce;
    }
</style>
""", unsafe_allow_html=True)

# Базаны түзүү
DB_FILE = "quiz_database.csv"
if not os.path.exists(DB_FILE):
    columns_list = ["ФИО", "Класс", "Убактысы", "Туура жооп", "Процент (%)", "Деңгээли", "Учурдагы_Этап", "Жооптор"]
    pd.DataFrame(columns=columns_list).to_csv(DB_FILE, index=False)

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
# Сайттын башкы бети
st.title("🐍 Python Тести жана Аналитика")

st.subheader("Тестке кош келиңиз!")

st.write("Бул платформа аркылуу Python билимиңизди текшере аласыз.")

st.success("Сайт ийгиликтүү иштеп жатат!")
# Окуучунун маалыматтары жана тест
st.divider()
st.header("📝 Python билимин текшерүү")

with st.form("python_test"):

    fio = st.text_input("Окуучунун аты-жөнү:")
    clazz = st.text_input("Классы:")

    st.subheader("50 суроолук тест")

    user_answers = []

    for i, question in enumerate(QUESTIONS):
        st.markdown(f"**{i + 1}. {question['q']}**")

        options = [x for x in question["options"] if x.strip()]

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

    if not fio.strip() or not clazz.strip():
        st.error("Аты-жөнүңүздү жана классыңызды жазыңыз!")

    else:
        score = 0

        for i, question in enumerate(QUESTIONS):
            if user_answers[i] == question["answer"]:
                score += 1

        total = len(QUESTIONS)
        percent = round(score / total * 100, 2)

        level = get_level(percent)

        current_time = datetime.now().strftime(
            "%d.%m.%Y %H:%M"
        )

        answers_text = str(user_answers)

        save_to_db(
            fio,
            clazz,
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
# ==================================
# МУГАЛИМ ПАНЕЛИ
# ==================================

with st.expander("🔐 МУГАЛИМ ПАНЕЛИ"):

    password = st.text_input(
        "Мугалимдин сырсөзү:",
        type="password",
        key="teacher_password"
    )

    if password == "nazira2026":

        st.success("Мугалим панели ачылды!")

        df = load_db()

        if not df.empty:

            st.subheader("📊 Окуучулардын жыйынтыгы")

            classes = sorted(
                df["Класс"].dropna().astype(str).unique()
            )

            selected_class = st.selectbox(
                "Классты тандаңыз:",
                ["Бардык класстар"] + classes
            )

            if selected_class == "Бардык класстар":
                result = df.copy()
            else:
                result = df[
                    df["Класс"].astype(str) == selected_class
                ].copy()

            result = result.sort_values(
                by=["Класс", "ФИО"]
            )

            col1, col2, col3 = st.columns(3)

            col1.metric("Окуучулар", len(result))

            col2.metric(
                "Орточо пайыз",
                f"{result['Процент (%)'].mean():.1f}%"
            )

            col3.metric(
                "Мыкты деңгээл",
                len(result[
                    result["Деңгээли"].str.contains(
                        "Advanced", na=False
                    )
                ])
            )

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

            # EXCEL ЖҮКТӨӨ

            buffer = io.BytesIO()

            with pd.ExcelWriter(
                buffer,
                engine="openpyxl"
            ) as writer:

                result.to_excel(
                    writer,
                    index=False,
                    sheet_name="Жыйынтыктар"
                )

            st.download_button(
                "📥 Excel жүктөп алуу",
                data=buffer.getvalue(),
                file_name="Okuu_jyyyntygy.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.divider()

            # СЕРТИФИКАТ

            st.subheader("🏆 Сертификат берүү")

            names = result["ФИО"].dropna().unique().tolist()

            if names:

                name = st.selectbox(
                    "Окуучуну тандаңыз:",
                    names
                )

                student = result[
                    result["ФИО"] == name
                ].iloc[0]

                fio_cert = html.escape(str(student["ФИО"]))
                class_cert = html.escape(str(student["Класс"]))
                percent_cert = html.escape(str(student["Процент (%)"]))
                level_cert = html.escape(str(student["Деңгээли"]))

                cert = f"""
                <html>
                <head>
                <meta charset="UTF-8">
                <style>
                body {{
                    font-family: Arial;
                    text-align: center;
                    background: #f0f2f6;
                    padding: 30px;
                }}
                .cert {{
                    background: white;
                    border: 10px double #667eea;
                    padding: 45px;
                    max-width: 800px;
                    margin: auto;
                }}
                h1 {{ color: #667eea; }}
                h2 {{ color: #333; }}
                .score {{
                    font-size: 40px;
                    color: #764ba2;
                    font-weight: bold;
                }}
                </style>
                </head>
                <body>
                <div class="cert">
                    <h1>🏆 СЕРТИФИКАТ</h1>
                    <h2>PYTHON БИЛИМИН ТЕКШЕРҮҮ</h2>
                    <p>Бул сертификат</p>
                    <h2>{fio_cert}</h2>
                    <p>{class_cert} классынын окуучусуна берилет.</p>
                    <p>Тесттин жыйынтыгы:</p>
                    <div class="score">{percent_cert}%</div>
                    <p>Деңгээли: {level_cert}</p>
                    <br><br>
                    <p>Бейшеналиева Назира Асановна</p>
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

    elif password:
        st.error("Сырсөз туура эмес!")

# Платформанын автору
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
    <h2>Бейшеналиева Назира Асановна</h2>
    <p>Python</p>
    <p>© 2026 Бардык укуктар корголгон</p>
</div>
""", unsafe_allow_html=True)
