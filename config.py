TOKEN = 'OTcyNDA3NjE2MjUwNzIwMzE2.GN7sW3.7LF5a0wIb_6vHT3jLovSB2NWxSJCmDMRbcI8dg'
MONGO_TOKEN = 'mongodb+srv://Iscra:blackwolf999@cluster0.noqz5gz.mongodb.net/?retryWrites=true&w=majority'

COMMANDS = {
    'note': ' [name]: [text] введите название и текст чтобы создать заметку',
    'what': ' [name] введите название заметки чтобы обратиться к ней',
    'notated': ' (nn) выводит имена заметок',
    'formula': ' (f) [formula] расчитывает математическое выражение',
    'rroll': ' (r, p, к) [1d1] введите кол-во кубов и их значение чтобы сделать, бросок [1d1_1] '
             ' задаст минимальное пороговое значение, m положительный модификатор к броску каждого куба'
             ' mm для отрицательного модификатора, модификатор всегда [1d1_1m1, 1d1mm1], [b1d1]'
             ' для активации взрыва кубов, [s1d1] для сортировки результатов',
    'croll': ' (cr, ск) [1d1_1+1d1] рассчитывает результат',
    'del': ' [limit] удаляет limit сообщений с момента ввода команды, команда также будет удалена,'
           ' команда не учитываетв в limit',
    'coin': ' (монетка) бросок монетки со значеним орёл/решка/ребро',
    'say': ' (скажи) [text] создаёт сообщение содержащее [text]',
    'choose': ' (выбрать, выбери) [options] случайно выбирает значение из [option]',
    'timer': ' (t, таймер, т) 1d1h1m1s/1д1ч1м1с спустя введённое время бот сообщит об окончании таймера',
    'dnote': ' (dn) [name] введите название записи которую хотите удалить'


}

phrases = [
    'я на страже',
    'проходи, не задерживайся',
    'и снова здавствуй, милый друг, всё так же бродишь ты вокруг...',
    'из мрака свет, из света мрак, и в ужасе бежит мой враг',
    'струится тьма, сверкает свет, врагам моим спасенья нет',
    'no pasaram!'
]

names = ['Gatekeeper', 'привратник', 'gatekeeper', 'Страж', 'Привратник', '<@&972458797937332247>',
         '<@972407616250720316>', 'привет', 'Hi,', 'Hello', 'hello', 'Привет', 'bot']
