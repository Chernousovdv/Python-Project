# Python-Project
Typing excercise desktop app

Typing excercise desktop app Текст выбирается случайным образом из файла texts.txt соответсвенно можно загружать свои тексты. Окошко ввода не позволяет вводить неправильные символы, ошибки подсчитываются и подписаны как errors при этом количество ошибок сохраняется в error_log.dat т.е сохраняется при запуске. также присутсвует таймер счётчик набираемых слов и правильных символов в минуту. Присутсвует таймер реализованный с помощью thread. Кнопка reset сбрасывает ошибки, обновляет текст и обнуляет счётчики. Кнопка help открывает окошко с информацией по теме.

Class Window: Основное окно со всеми виджетами и прописаннами классовыми функциями
NewText: Выбор случайного текста из файла с текстами
StartProgramm: Иницилизирует старт работы тренажёра, запускает Thread с таймером
is_valid: Проверяет, является ли вводимый пользователем символ валидным, т.е. совпадает ли он с тепершней буквой текста. Также проверяет, не ввёлся ли весь текст, и вызывает функцию NewText если это так. Если значение неверно, изменяет счётчик ошибок.

OpenHelp: функция создающая объект типа Help, который является окном с базовой информацией по скоростному набору текста
Help: объект, который является окном с базовой информацией по скоростному набору текста
Reset: Функция, обнуляющая статистику, а именно текст, таймер, количесвто ошибок, и скорость набора текста
Init: Иницилизирущая класс функция в которой создаются и размещаются все виджета окна.
