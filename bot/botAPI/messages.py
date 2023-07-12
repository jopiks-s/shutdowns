import gettext
from enum import Enum

from bot.db.user import User
from config import root_path
from . import logger

default_lang = User.language_code.default
langs = ['uk', 'en']
languages = {}
for language in langs:
    languages[language] = gettext.translation('main', f'{root_path}/locales/', languages=[language])


# todo refactor
class Messages(Enum):
    start = """Привіт 🤙, це бот відключень міста Київ, який може надати графік 🗓 та повідомляти ⚠️ про майбутні відключенню у місті відповідно до інформації наданої на офіційному сайті [ДТЕК](https://www.dtek-kem.com.ua/ua/shutdowns)

👀
Для перегляду графіка використовуйте команду /view '_номер групи_', якщо бажаєте переглянути відключення для конкретної групи, або,  /view для перегляду власної.

Щоб отримати інформацію про свої налаштування використайте команду /info

⚙️
Для того, щоб бот почав повідомляти вас про можливі відключення:
1. Зайдіть на сайт [ДТЕК](https://www.dtek-kem.com.ua/ua/shutdowns)
2. Дізнайтесь свою групу увівши адресу та номер дому
3. Використайте команду /setgroup '_номер групи_'

За замовчуванням, повідомлення буде приходити за *15хв* ⏱ до відключення. Ви можете змінити наскільки завчасно повідомлення будуть приходити командою /notification\_advance '_кількість хвилин_'

🚫🚫🚫
Якщо ви більше не бажаєте отримувати нагадування, ви можете  вимкнути повідомлення або зупинити бота.

Список команд для взаємодії з ботом🙃
/start - запуск бота
/view ('_номер групи_') - перегляд графіку відключень за вашою групою або вказаним номером
/setgroup '_номер групи_' - встановлення вашої групи
/notification\_advance '_кількість хвилин_' - встановлення за скільки до відключення вас повідомляти (хв).
/info - перегляд налаштувань"""

    view_success = 'Група {group}'
    view_failure_group = """Щоб подивитися розклад конкретної групи
/view '_номер групи_'.
Ви не встановили номер своєї групи, щоб це зробити 👇"""
    view_failure_param = """/view ('_номер групи_') - перегляд графіку відключень за вашою групою або вказаним номером.
'_Номер групи_' число від 1 до 3.
/view ✅ # _Відобразити за вашою групою_
/view 1 ✅ # _Відобразити 1 групу_
/view 10 🚫"""

    setgroup = """/setgroup '_номер групи_' - встановлення вашої групи.
'_Номер групи_' число від 1 до 3.
/setgroup 1 ✅
/setgroup 10 🚫"""
    setgroup_success = 'Групу успішно змінено! ✅'
    setgroup_failure = 'Не вдалося змінити групу :( 🚫'

    notification_advance = """/notification\_advance '_кількість хвилин_' - встановлення за скільки до відключення вас повідомляти.
'_Кількість хвилин_' - зсув від *0хв* до *1 доби* (_1440хв_).
/notification\_advance 25 ✅ # _За 25хв до відключень_
/notification\_advance 1441 🚫"""
    notification_advance_success = 'Час успішно змінено! ✅'
    notification_advance_failure = 'Не вдалося змінити час повідомлень :( 🚫'

    info_set = 'Група {group}. Повідомлення за {notification_advance}хв до відключення.'
    info_unset = 'Група не встановлена. Щоб це зробити👇'


# todo lock, dude :)
def get_translation(msgs: tuple[Messages] | Messages, language_code: str, **kwargs) -> str:
    if language_code in languages:
        languages[language_code].install()
        logger.debug(f'Installed language: {language_code}')
    else:
        languages[default_lang].install()
        logger.debug(f'Didn`t find language: {language_code}\n'
                     f'Installed default: {default_lang}')

    if isinstance(msgs, tuple):
        text = '\n'.join([_(msg.value) for msg in msgs])
        text = text.format(**kwargs)
    else:
        text = _(msgs.value).format(**kwargs)

    return text
