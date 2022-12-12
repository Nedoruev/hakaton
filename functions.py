from asyncpg import UniqueViolationError
from classes import *
from final_bot import date
import random
import uuid


let = (('A', 'E', 'I', 'O', 'U', 'Y', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Z'), ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))


def create_token():
    return str(uuid.uuid4())


def create_passwoed():
    password = ''
    for i in range(9):
        ran = random.randrange(2)
        password += random.choice(let[ran])
    return password


def check_password(password: str):
    b_l = False
    n = False
    if len(password) >= 8:
        for i in password:
            if i in let[0]:
                b_l = True
            if i in let[1]:
                n = True
    if b_l and n:
        return True
    else:
        return False


async def set_default_commands(dp: dp):
    await dp.bot.set_my_commands([
        types.BotCommand('/start', 'Привітання'),
        types.BotCommand('/login', 'Зареєструватися'),
        types.BotCommand('/sup', 'Увійти'),
        types.BotCommand('/menu', 'Головне меню'),
        types.BotCommand('/disc', 'Список дисциплін')
    ])


async def edit_message(message: types.Message, text):
    new_mess = await message.edit_text(text, parse_mode='Markdown')
    return new_mess


async def startup_database(disptcher: dp):
    print('устанавливается связь с базой данных')
    await db.set_bind(config.POSTGRES_URI)


async def db2_test():
    await db.set_bind(config.POSTGRES_URI)


async def studend_func(message, text):
    if register_text in message.reply_to_message.text:
        if datetime.datetime.now() < date:
            user = await select_user_by_id(message.from_user.id)
            disc = await select_disc(text)
            registered = False
            for i in await select_all_disc():
                if user.name in i.info.split(" / ")[1].split(","):
                    registered = True
                    break
            if disc is None:
                await message.answer(f'Такої дисципліни не існує.')
            else:
                if len(disc.info.split(" / ")[1].split(",")) <= 30:
                    if not registered:
                        await add_user_to_disc(disc, user)
                        await message.answer(f'Вас зареєстровано на {text}!')
                    else:
                        await message.answer('Ви вже зареєстровані!')
        else:
            await message.answer('Реєстрація завершена.')


async def teacher_func(message, text):
    f_user = await select_user_by_id(message.from_user.id)
    if c_disc_info_t_text in message.reply_to_message.text:
        disc = await select_disc(f_user.disc)
        await update_disc_info(disc, text)
        await message.answer('Інформація успішно оновлена.')


async def admin_func(message, text):
    user = await select_user(text[0])
    if message.reply_to_message.text == c_name_text:
        if user is None:
            await message.answer(f'Помилка, здається користувача з таким ім\'ям *не існує.*', parse_mode='Markdown')
        else:
            await update_user_name(user, text[1])
            await message.answer(f'{text[0]} тепер {text[1]}.')
    elif c_disc_text in message.reply_to_message.text:
        disc = await select_disc(text[1])
        user = await select_user(text[0])
        if user is None:
            await message.answer(f'Помилка, здається користувача з таким ім\'ям *не існує.*', parse_mode='Markdown')
        else:
            if disc is not None:
                await update_user_disc(user, text[1])
                await message.answer(f'{text[0]} тепер викладає: {text[1]}.')
            else:
                await message.answer('Такої дисципліни *не існує.*', parse_mode='Markdown')
    elif c_disc_name_text in message.reply_to_message.text:
        disc = await select_disc(text[0])
        if disc is None:
            await message.answer('Такої дисципліни *не існує.*', parse_mode='Markdown')
        else:
            if disc is not None:
                await update_disc_name(disc, text[1])
                await message.answer(f'{text[0]} тепер {text[1]}.')
            else:
                await message.answer('Такої дисципліни *не існує.*', parse_mode='Markdown')
    elif disc_students_text in message.reply_to_message.text:
        disc = await select_disc(text)
        if disc is None:
            await message.answer('Такої дисципліни *не існує.*', parse_mode='Markdown')
        else:
            if disc is not None:
                text = f'{len(disc.info.split(" / ")[1].split(","))}/30 \n'
                for j in disc.info.split(' / ')[1].split(','):
                    text += j + '\n'
                await message.answer(text)
            else:
                await message.answer('Такої дисципліни *не існує.*', parse_mode='Markdown')
    elif c_disc_info_text in message.reply_to_message.text:
        disc = await select_disc(text[0])
        if disc is None:
            await message.answer('Такої дисципліни *не існує.*', parse_mode='Markdown')
        else:
            if disc is not None:
                await update_disc_info(disc, text[1])
                await message.answer(f'Інформація *успішно* змінена.', parse_mode='Markdown')
            else:
                await message.answer('Такої дисципліни *не існує.*', parse_mode='Markdown')


async def reggistration(message, text):
    user = await select_user(text[0])
    if user is None:
        await message.answer(f'Помилка, здається користувача з таким ім\'ям *не існує.*\n{login_text}',
                             parse_mode='Markdown')
    else:
        if user.password == text[1]:
            user = await select_user_by_id(message.from_user.id)
            if user is not None:
                await update_user_id(user, 0)
            user = await select_user(text[0])
            await update_user_id(user, message.from_user.id)
            await message.answer(f'Вітаємо, {user.role}, Ви увійшли!')
        else:
            await message.answer('Неправильний пароль. Якщо ви його забули, то напишіть /recover "Token".')


async def sign_up(message, text):
    in_db = False
    token = create_token()
    for user in await select_all_users():
        if text[0] == user.name:
            in_db = True
            await message.answer(login_text)
            break
    if not in_db:
        user = await select_user_by_id(message.from_user.id)
        if user is not None:
            await update_user_id(user, 0)
        if check_password(text[1]):
            await add_user(message.from_user.id, token, text[1], text[0], 'student', 'unselected')
            await message.answer(f'Дані для входу: \n'
                                 f'*Токен (нікому не показувати)*:\n'
                                 f'{token}\n'
                                 f'*Логін*:\n'
                                 f'{text[0]}\n'
                                 f'*Пароль (нікому не показувати)*:\n'
                                 f'{text[1]}\n', parse_mode='Markdown')
        else:
            await message.answer('Ваш пароль: \n'
                                 'можливо *коротший за 8 символів*\n'
                                 'може не містити *великої літери латиницею*\n'
                                 'може не містити *цифри*\n'
                                 'Спробуйте ще раз.', parse_mode='Markdown')


async def no_students_notify():
    if datetime.datetime.now() > date:
        no_students = False
        for i in await select_all_disc():
            if len(i.info.split(" / ")[1].split(",")) < 5:
                no_students = True
                break
        if no_students:
            for i in await select_all_users():
                if i.role == 'student' and i.user_id != 0:
                    await bot.send_message(i.user_id, 'На жаль, на одну, або декілька дисциплін не'
                                                      ' набралося достатньої кількості студентів. '
                                                      'Будь ласка, *переоберіть дисципліну.*', parse_mode='Markdown')


async def create_disc(less_name: str, info: str):
    try:
        disc = Lessons(less_name=less_name, info=info)
        await disc.create()
    except UniqueViolationError:
        print('Дисципліна не додана')


async def add_user(user_id: int, token: str, password: str, name: str, role: str, disc: str):
    try:
        user = User(user_id=user_id, token=token, password=password, name=name, role=role, disc=disc)
        await user.create()
    except UniqueViolationError:
        print('Користувач не доданий')


async def add_disc(less_name: str, info: str):
    try:
        disc = Lessons(less_name=less_name, info=info)
        await disc.create()
    except UniqueViolationError:
        print('Дисципліна не додана')


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_all_disc():
    disc = await Lessons.query.gino.all()
    return disc


async def select_disc(less_name):
    disc = await Lessons.query.where(Lessons.less_name == less_name).gino.first()
    return disc


async def update_disc_name(disc, name):
    await disc.update(less_name=name).apply()


async def select_user_by_id(user_id: int):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def select_user_by_token(token):
    user = await User.query.where(User.token == token).gino.first()
    return user


async def select_user(name):
    user = await User.query.where(User.name == name).gino.first()
    return user


async def select_by_role(role):
    user = await User.query.where(User.role == role).gino.first()
    return user


async def change_password(password: str, token: str):
    user = await select_user_by_token(token)
    await user.update(password=password).apply()


async def update_user_id(user, user_id):
    await user.update(user_id=user_id).apply()


async def update_user_name(user, name):
    await user.update(name=name).apply()


async def update_user_disc(user, disc):
    await user.update(disc=disc).apply()


async def disc_info(disc):
    return disc.info.split(' / ')[0]


async def update_disc_info(disc, info):
    studetns = disc.info.split(' / ')[1]
    new_info = info + ' / ' + studetns
    await disc.update(info=new_info).apply()


async def add_user_to_disc(disc, user):
    info = disc.info
    new_info = info + ',' + user.name
    await disc.update(info=new_info).apply()




