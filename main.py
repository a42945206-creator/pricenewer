from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
PHONE = "+7 978 474 52 38"   # ← замени на свой номер
BANK = "Т-Банк"             # ← замени на свой банк
ADMIN_ID = 88952617         # ← твой ID, уже вписан

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- ТЕКСТЫ УСЛУГ ----------
TEXTS = {
    "menu": (
        "Способ оплаты – любой кроме приёма на карты других стран кроме РФ\n\n"
        "Выбери категорию:"
    ),
    "krajnee": (
        "Крайнее\n\n"
        "Удаление вашей информации из источников – 1600₽\n"
        "Услуги деффа (защиты) – 1500₽ / навсегда"
    ),
    "rassled": (
        "Расследования\n\n"
        "Информационное досье — сбор данных.\n"
        "Оперативное досье — сбор + анализ данных.\n"
        "Разведывательное досье — сбор + анализ + разведка.\n\n"
        "Цены:\n"
        "• Информационное досье: 700₽\n"
        "• Оперативное досье: 1400₽\n"
        "• Разведывательное досье: 1600₽"
    ),
    "obuchenie": (
        "Обучение\n\n"
        "Наставничество — менторство. Я за ручку пройду с вами по "
        "основным точкам интереса в разведке: OSINT, сбор данных, "
        "анализ и проверка объективности данных, систематизация, "
        "инструменты, методички, сборка дистрибутива под разведку и азы "
        "терминала, GEOINT, HUMINT, социальная инженерия и другие "
        "интересующие вас темы.\n\n"
        "Личный Архив — приватный форум проекта. Обучение в закрытом "
        "комьюнити + практика. В категориях архива вы найдете: софт, "
        "веб-инструменты, методички, отчёты, досье, инструкции, "
        "литературу, базы данных и словари, категорию для проведения "
        "расследований, а также деловые предложения от участников "
        "группы.\n\n"
        "Цены:\n"
        "• Наставничество (менторство): 4500₽/мес.\n"
        "• Личный Архив: 500₽/мес., 2200₽/навсегда"
    ),
    "dosug": (
        "Досуг\n\n"
        "Префикс — плашка над вашим никнеймом в выбранной вами группе.\n\n"
        "Цена: 50₽"
    ),
    "numbers_intro": (
        "Физические номера\n\n"
        "Разница в цене за создание аккаунта и смену номера "
        "обусловлена SMS fee в Telegram. Вне зависимости от того, "
        "опцию вы выберете, в конечном итоге вы получите номер "
        "полностью в ваше распоряжение: бесплатные повторные коды под "
        "любые сервисы, бесплатное восстановление сессий, консультации "
        "и обратная связь, гарантия на пол года."
    ),
    "numbers_list": (
        "🇺🇸 США +1 (спам блок) — 60₽\n"
        "🇺🇸 США +1 — 80₽\n"
        "🇺🇸 США отлега (6-8 лет) — 450₽\n"
        "🇮🇳 Индия +91 — 115₽\n"
        "🇧🇩 Бангладеш +880 — 115₽\n"
        "🇪🇨 Эквадор +593 — 130₽\n"
        "🇺🇿 Узбекистан +998 — 140₽\n"
        "🇵🇱 Польша +48 — 190₽\n"
        "🇬🇧 Великобритания +44 — 190₽\n"
        "🇲🇽 Мексика +52 — 200₽\n"
        "🇮🇷 Иран +98 — 205₽\n"
        "🇩🇪 Германия +49 — 215₽\n"
        "🇫🇷 Франция +33 — 230₽\n"
        "🇰🇿 Казахстан +77 — 235₽\n"
        "🇪🇪 Эстония +372 — 245₽\n"
        "🇳🇱 Нидерланды +31 — 265₽\n"
        "🇪🇸 Испания +34 — 265₽\n"
        "🇯🇵 Япония +81 — 280₽\n"
        "🇲🇷 Мавритания +222 — 315₽\n"
        "🇺🇦 Украина +380 — 390₽\n"
        "🇨🇿 Чехия +420 — 390₽\n"
        "🇱🇻 Латвия +371 — 445₽\n"
        "🏷️ аккаунт «FAKE» — 290₽"
    ),
    "admin_panel": (
        "👑 Админ-панель\n\n"
        "Здесь ты можешь посмотреть статистику заказов."
    ),
}

# ---------- КЛАВИАТУРЫ ----------
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Крайнее", callback_data="krajnee")],
        [InlineKeyboardButton(text="Расследования", callback_data="rassled")],
        [InlineKeyboardButton(text="Обучение", callback_data="obuchenie")],
        [InlineKeyboardButton(text="Досуг", callback_data="dosug")],
        [InlineKeyboardButton(text="Физические номера", callback_data="numbers_intro")],
    ])

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 Оплата переводом", callback_data="pay_manual")],
        [InlineKeyboardButton(text="◀ В меню", callback_data="back_menu")],
    ])

def numbers_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Показать список номеров", callback_data="numbers_list")],
        [InlineKeyboardButton(text="💸 Оплата переводом", callback_data="pay_manual")],
        [InlineKeyboardButton(text="◀ Назад", callback_data="back_menu")],
    ])

def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="◀ В меню", callback_data="back_menu")],
    ])

# ---------- ПОЛЬЗОВАТЕЛЬСКИЕ ХЭНДЛЕРЫ ----------
@dp.message(Command("start"))
@dp.message(Command("buy"))
async def cmd_start(message: types.Message):
    await message.answer(TEXTS["menu"], reply_markup=main_menu_kb())

@dp.callback_query(F.data.in_({"krajnee", "rassled", "obuchenie", "dosug"}))
async def show_service(callback: CallbackQuery):
    await callback.message.edit_text(TEXTS[callback.data], reply_markup=back_kb())
    await callback.answer()

@dp.callback_query(F.data == "numbers_intro")
async def show_numbers_intro(callback: CallbackQuery):
    await callback.message.edit_text(TEXTS["numbers_intro"], reply_markup=numbers_kb())
    await callback.answer()

@dp.callback_query(F.data == "numbers_list")
async def show_numbers_list(callback: CallbackQuery):
    await callback.message.edit_text(TEXTS["numbers_list"], reply_markup=back_kb())
    await callback.answer()

@dp.callback_query(F.data == "back_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(TEXTS["menu"], reply_markup=main_menu_kb())
    await callback.answer()

@dp.callback_query(F.data == "pay_manual")
async def pay_manual(callback: CallbackQuery):
    await callback.message.answer(
        f"💸 Оплата переводом\n\n"
        f"Номер: {PHONE}\n"
        f"Банк: {BANK}\n\n"
        f"После перевода напиши сюда, какую услугу ты купил — я выдам её."
    )
    await callback.answer()

# ---------- АДМИН-ПАНЕЛЬ ----------
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У тебя нет доступа.")
        return
    await message.answer(TEXTS["admin_panel"], reply_markup=admin_kb())

@dp.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Нет доступа.", show_alert=True)
        return
    await callback.message.answer("📊 Статистика пока пуста — заказов ещё не было.")
    await callback.answer()

# ---------- УВЕДОМЛЕНИЕ О ЗАКАЗЕ ----------
@dp.message(Command("order"))
async def order(message: types.Message):
    # Пользователь пишет /order и указывает услугу
    # Например: /order Информационное досье
    await message.answer(
        "Напиши, какую услугу ты купил, в формате:\n"
        "`/order Название услуги`\n\n"
        "Например: `/order Информационное досье`"
    )

@dp.message(F.text.startswith("/order "))
async def process_order(message: types.Message):
    service = message.text.replace("/order ", "").strip()
    user = message.from_user

    # Уведомление админу
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🔔 НОВЫЙ ЗАКАЗ\n\n"
            f"👤 Юзернейм: @{user.username or 'нет'}\n"
            f"🆔 ID: {user.id}\n"
            f"🛒 Услуга: {service}\n\n"
            f"Проверь поступление средств и выдай услугу."
        )
    )

    await message.answer(
        "✅ Твой заказ отправлен. После подтверждения оплаты я выдам услугу."
    )

# ---------- ЗАПУСК ----------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
