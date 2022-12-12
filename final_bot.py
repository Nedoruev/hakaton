from datetime import datetime
from aiogram import executor
from variables import *
import functions
import asyncio
import asyncpg
import datetime


date: datetime = datetime.datetime(2022, 12, 11, 23, 0)


async def db2_test():
    await db.set_bind(config.POSTGRES_URI)


@dp.message_handler(commands=['start'])
async def admin_funcs(message: types.Message):
    await message.answer('Вітаю, для реєстрації уведіть /login,'
                         ' переглянути усі дисципліни можна'
                         ' за допомогою /disc')


@dp.message_handler(commands=['set_date', 'add_teacher', 'teachers'])
async def admin_funcs(message: types.Message):
    global date
    admin = await functions.select_by_role('admin')
    admin_id = admin.user_id
    if message.from_user.id == admin_id:
        if '/add_teacher' in message.text:
            text = message.text.replace('/add_teacher ', '')
            token = functions.create_token()
            for i in (' / ', ' /', '/ ', '/'):
                if i in text:
                    text = text.split(i)
                    break
            if len(text) != 3:
                await message.answer('Уведіть /add_teacher "Login" / "Password" / "Discipline"')
            else:
                await functions.add_user(0, token, text[1], text[0], 'teacher', text[2])
                await message.answer(f'Дані для входу: \n'
                                     f'*Токен (нікому не показувати)*:\n'
                                     f'{token}\n'
                                     f'*Логін*:\n'
                                     f'{text[0]}\n'
                                     f'*Пароль (нікому не показувати)*:\n'
                                     f'{text[1]}\n'
                                     f'*Дисципліна*:\n'
                                     f'{text[2]}\n', parse_mode='Markdown')
        elif '/teachers' in message.text:
            t_list = ''
            for user in await functions.select_all_users():
                if user.role == 'teacher':
                    t_list += f'{user.name} - {user.disc}\n'
            await message.answer(t_list)
        elif '/set_date' in message.text:
            text = message.text.replace('/set_date', ' ')
            text = [int(i) for i in text.split()]
            date = datetime.datetime(text[0], text[1], text[2], text[3], text[4])
            await message.answer(f'Встановлена дата закриття набору: *{date}*', parse_mode='Markdown')


@dp.message_handler(text_contains='sup')
async def signup(message: types.Message):
    await message.answer(sup_text)


@dp.message_handler(text_contains='/login')
async def login_students(message: types.Message):
    await message.answer(login_text)


@dp.message_handler(text_contains='/recover')
async def login_students(message: types.Message):
    token = message.text.replace('/recover ', '')
    user = await functions.select_user_by_token(token)
    password = functions.create_passwoed()
    if user.name is not None:
        await functions.change_password(password=password, token=token)
        await message.answer(f'{user.name}, Ваш новий пароль *{password}*', parse_mode='Markdown')


@dp.message_handler(commands=['menu'])
async def main_menu(message: types.Message):
    user = await functions.select_user_by_id(message.from_user.id)
    if user is not None:
        if user.role == 'admin':
            await message.answer('Що потрібно переглянути/відредагувати?', reply_markup=admin_main_menu, parse_mode='Markdown')
        elif user.role == 'teacher':
            await message.answer('Що потрібно переглянути/відредагувати?', reply_markup=teacher_menu, parse_mode='Markdown')
        elif user.role == 'student':
            await message.answer('Що потрібно переглянути?', reply_markup=student_menu, parse_mode='Markdown')
    else:
        await message.answer('Головне меню достопне лише для '
                             '*зареєстрованих* користвучів,'
                             ' натисніть /login для реєстрації', parse_mode='Markdown')


@dp.message_handler(commands=['disc'])
async def discc(message: types.Message):
    text = ''
    for i in await functions.select_all_disc():
        text += f'\n*{i.less_name}*:' \
                f'\n\t\t{await functions.disc_info(i)}\n'
    await message.answer(text, parse_mode='Markdown')


@dp.callback_query_handler(lambda call: 'main_menu' in call.data)
async def admin_2_menu(call):
    text = 'Що потрібно переглянути/відредагувати?'
    user = await functions.select_user_by_id(call.from_user.id)
    await functions.edit_message(call.message, text)
    if user.role == 'admin':
        await call.message.edit_reply_markup(admin_main_menu)


@dp.callback_query_handler(lambda call: 'profile' in call.data)
async def profile(call):
    user = await functions.select_user_by_id(call.from_user.id)
    await call.message.answer(f'*Ім\'я:*\n'
                              f'{user.name}\n'
                              f'*Роль*:\n'
                              f'{user.role}\n'
                              f'*Дисципліни*:\n'
                              f'{user.disc}', parse_mode='Markdown')


@dp.callback_query_handler(lambda call: 'teachers' in call.data)
async def admin_2_menu(call):
    text = ''
    for i in await functions.select_all_users():
        if i.role == 'teacher':
            text += f'*{i.name}* - {i.disc}\n'
    user = await functions.select_user_by_id(call.from_user.id)
    await functions.edit_message(call.message, text)
    if user.role == 'admin':
        await call.message.edit_reply_markup(admin_t_menu)


@dp.callback_query_handler(lambda call: 'c_name' in call.data)
async def c_name(call):
    user = await functions.select_user_by_id(call.from_user.id)
    if user.role == 'admin':
        await call.message.answer(c_name_text)


@dp.callback_query_handler(lambda call: 'c_disc' in call.data)
async def c_disc(call):
    text = '\nоберіть одну з: \n'
    for i in await functions.select_all_disc():
        text += '*' + i.less_name + '*\n'
    user = await functions.select_user_by_id(call.from_user.id)
    if user.role == 'admin':
        await call.message.answer(c_disc_text + text, parse_mode='Markdown')


@dp.callback_query_handler(lambda call: 'disc1' in call.data)
async def admin_3_menu(call):
    text = ''
    for i in await functions.select_all_disc():
        text += f'\n*{i.less_name}*:\n\t\t{await functions.disc_info(i)}\n'
    user = await functions.select_user_by_id(call.from_user.id)
    await functions.edit_message(call.message, text)
    if user.role == 'admin':
        await call.message.edit_reply_markup(admin_d_menu)


@dp.callback_query_handler(lambda call: 'c_d_name' in call.data)
async def c_d_name(call):
    user = await functions.select_user_by_id(call.from_user.id)
    if user.role == 'admin':
        await call.message.answer(c_disc_name_text)


@dp.callback_query_handler(lambda call: 'students' in call.data)
async def disc_students(call):
    user = await functions.select_user_by_id(call.from_user.id)
    if user.role == 'admin':
        await call.message.answer(disc_students_text)


@dp.callback_query_handler(lambda call: 'c_info' in call.data)
async def disc_students(call):
    user = await functions.select_user_by_id(call.from_user.id)
    if user.role == 'admin':
        await call.message.answer(c_disc_info_text)


@dp.callback_query_handler(lambda call: 't_dis' in call.data)
async def disc_students(call):
    user = await functions.select_user_by_id(call.from_user.id)
    if user.role == 'teacher':
        disc = await functions.select_disc(user.disc)
        await call.message.answer(f'Ваша дисципліна: *{user.disc}*\n'
                                  f'Інформація: *{await functions.disc_info(disc)}*', parse_mode='Markdown')


@dp.callback_query_handler(lambda call: 'teacher1' in call.data)
async def t_s(call):
    user = await functions.select_user_by_id(call.from_user.id)
    if user.role == 'teacher':
        disc = await functions.select_disc(user.disc)
        text = f'{len(disc.info.split(" / ")[1].split(","))}/30 \n'
        for j in disc.info.split(' / ')[1].split(','):
            text += j + '\n'
        await call.message.answer(text)


@dp.callback_query_handler(lambda call: 'teacher2' in call.data)
async def disc_students(call):
    user = await functions.select_user_by_id(call.from_user.id)
    if user.role == 'teacher':
        await call.message.answer(c_disc_info_t_text)


@dp.callback_query_handler(lambda call: '123123' in call.data)
async def disc_students1(call):
    user = await functions.select_user_by_id(call.from_user.id)
    if user.role == 'student':
        text = f'Дата завершення реєстрації: *{date}* \n'
        for i in await functions.select_all_disc():
            if user.name in i.info.split(" / ")[1].split(","):
                text += f'\n*ЗАРЕЄСТОВАНИЙ* *{i.less_name} ({len(i.info.split(" / ")[1].split(","))}/30)*: ' \
                        f'\n\t\t{await functions.disc_info(i)}\n'
            else:
                text += f'\n*{i.less_name} ({len(i.info.split(" / ")[1].split(","))}/30)*:' \
                        f'\n\t\t{await functions.disc_info(i)}\n'
        await functions.edit_message(call.message, text)
        await call.message.edit_reply_markup(student_disc_menu)


@dp.callback_query_handler(lambda call: '321321' in call.data)
async def disc_students1(call):
    user = await functions.select_user_by_id(call.from_user.id)
    await functions.edit_message(call.message, 'Що потрібно переглянути?')
    if user.role == 'student':
        await call.message.edit_reply_markup(student_menu)


@dp.callback_query_handler(lambda call: 'register' in call.data)
async def disc_students1(call):
    user = await functions.select_user_by_id(call.from_user.id)
    if datetime.datetime.now() < date:
        if user.role == 'student':
            registered = False
            for i in await functions.select_all_disc():
                if user.name in i.info.split(" / ")[1].split(","):
                    registered = True
                    break
            if not registered:
                await call.message.answer(register_text)
            else:
                await call.message.answer('Ви вже зареєстровані!')
    else:
        await call.message.answer('Занадто пізно для реєстрації.')


@dp.message_handler()
async def least_funcs(message: types.Message):
    if message.reply_to_message is not None:
        if message.reply_to_message.from_user.is_bot:
            text = message.text
            for i in (' / ', ' /', '/ ', '/'):
                if i in text:
                    text = text.split(i)
                    break
            if message.reply_to_message.text == login_text:
                await functions.sign_up(message, text)
            elif message.reply_to_message.text == sup_text:
                await functions.reggistration(message, text)
            f_user = await functions.select_user_by_id(message.from_user.id)
            if f_user is not None:
                f_user = f_user.role
                if f_user == 'admin':
                    await functions.admin_func(message, text)
                elif f_user == 'teacher':
                    await functions.teacher_func(message, text)
                elif f_user == 'student':
                    await functions.studend_func(message, text)
    else:
        await message.reply('Відповідь на повідомлення виглядає так.')


async def on_startup(dp: dp):
    await functions.set_default_commands(dp)
    print('бот запущен')


async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database=config.DATABASE,
    user=config.PGUSER,
    password=config.PGPASSWORD,
    max_inactive_connection_lifetime=100)


loop = asyncio.get_event_loop()
loop.run_until_complete(db2_test())

if __name__ == '__main__':
    try:
        executor.start_polling(dp, on_startup=on_startup)
    except Exception as ex:
        print(ex)
        executor.start_polling(dp, on_startup=on_startup)