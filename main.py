from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
import asyncio
import os

# ======== ЗАМЕНИ ЭТИ ТРИ СТРОКИ ========
BOT_TOKEN = os.getenv("BOT_TOKEN", "ТОКЕН_БОТА")
PHONE = "+7 978 474 52 38"
BANK = "Т-Банк"
# =======================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- ТЕКСТЫ ----------
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
        "🇺🇸 США +1 (спам блок) — 60₽ / 40 звезд\n"
        "🇺🇸 США +1 — 80₽ / 53 звезд\n"
        "🇺🇸 США отлега (6-8 лет) — 450₽\n"
        "🇮🇳 Индия +91 — 115₽ / 53 звезд\n"
        "🇧🇩 Бангладеш +880 — 115₽ / 77 звезд\n"
        "🇪🇨 Эквадор +593 — 130₽ / 87 звезд\n"
        "🇺🇿 Узбекистан +998 — 140₽ / 93 звезд\n"
        "🇵🇱 Польша +48 — 190₽ / 127 звезд\n"
        "🇬🇧 Великобритания +44 — 190₽ / 127 звезд\n"
        "🇲🇽 Мексика +52 — 200₽ / 133 звезд\n"
        "🇮🇷 Иран +98 — 205₽ / 137 звезд\n"
        "🇩🇪 Германия +49 — 215₽ / 143 звезд\n"
        "🇫🇷 Франция +33 — 230₽ / 153 звезд\n"
        "🇰🇿 Казахстан +77 — 235₽ / 157 звезд\n"
        "🇪🇪 Эстония +372 — 245₽ / 163 звезд\n"
        "🇳🇱 Нидерланды +31 — 265₽ / 177 звезд\n"
        "🇪🇸 Испания +34 — 265₽ / 177 звезд\n"
        "🇯🇵 Япония +81 — 280₽ / 187 звезд\n"
        "🇲🇷 Мавритания +222 — 315₽ / 210 звезд\n"
        "🇺🇦 Украина +380 — 390₽ / 260 звезд\n"
        "🇨🇿 Чехия +420 — 390₽ / 260 звезд\n"
        "🇱🇻 Латвия +371 — 445₽ / 297 звезд\n"
        "🏷️ аккаунт «FAKE» — 290₽ / 193 звезд"
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
        [InlineKeyboardButton(text="⭐ Оплатить звёздами", callback_data="pay_stars")],
        [InlineKeyboardButton(text="💸 Оплата переводом", callback_data="pay_manual")],
        [InlineKeyboardButton(text="◀ В меню", callback_data="back_menu")],
    ])

def numbers_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Показать список номеров", callback_data="numbers_list")],
        [InlineKeyboardButton(text="⭐ Оплатить звёздами", callback_data="pay_stars")],
        [InlineKeyboardButton(text="💸 Оплата переводом", callback_data="pay_manual")],
        [InlineKeyboardButton(text="◀ Назад", callback_data="back_menu")],
    ])

# ---------- ХЭНДЛЕРЫ ----------
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
        f"💸 Оплата переводом\n\nНомер: {PHONE}\nБанк: {BANK}\n\n"
        f"После перевода пришли чек сюда — я подтвержу заказ."
    )
    await callback.answer()

@dp.callback_query(F.data == "pay_stars")
async def pay_stars(callback: CallbackQuery):
    await callback.message.answer(
        "⭐ Оплата звёздами пока в разработке.\n"
        "Пока используй кнопку «Оплата переводом»."
    )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
