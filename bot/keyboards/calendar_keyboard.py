import calendar
from contextlib import suppress
from datetime import datetime, timedelta

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

NOW = datetime.now()


def create_callback(action, year, month, day):
    """ Create the callback data associated to each button"""
    return f"{action}_{year}_{month}_{day}"


async def create_calendar(
        action: str = "MONTH",
        year: int = datetime.now().year,
        month: int = datetime.now().month
) -> InlineKeyboardMarkup:
    day_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    month_names = ['Декабрь', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                   'Август', 'Сентябрь', 'Октябрь', 'Ноябрь']
    ignore = create_callback("IGNORE", year, month, 0)
    # First row - Month and Year
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{year} год",
                callback_data=ignore
            ),
            InlineKeyboardButton(
                text=f"{month_names[month % 12]}",
                callback_data=ignore
            )
        ],
        [
            InlineKeyboardButton(
                text=day,
                callback_data=ignore
            ) for day in day_names
        ]
    ]

    # Second row - Week Days
    for week in calendar.monthcalendar(year, month):
        row = []
        for day in week:
            if day == 0:
                row.append(
                    InlineKeyboardButton(
                        text=" ",
                        callback_data=ignore
                    )
                )
            else:
                row.append(
                    InlineKeyboardButton(
                        text=f" {day} ",
                        callback_data=create_callback("DAY", year, month, day)
                    )
                )
        keyboard.append(row)

    # Last row - Buttons
    keyboard.append([
        InlineKeyboardButton(
            text="<",
            callback_data=create_callback("PREV-MONTH", year, month, 1)
        ),
        InlineKeyboardButton(
            text=" ",
            callback_data=ignore
        ),
        InlineKeyboardButton(
            text=">",
            callback_data=create_callback("NEXT-MONTH", year, month, 1)
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)


async def calendar_selection(callback):
    ret_data = (False, None)
    (action, year, month, day) = callback.data.split("_")
    current_date = datetime(int(year), int(month), 1)

    with suppress(TelegramBadRequest):
        if action == "IGNORE":
            pass
        elif action == "DAY":
            # await callback.message.edit_text(text=callback.message.text)
            ret_data = True, datetime(int(year), int(month), int(day))
        elif action == "PREV-MONTH":
            prev_month = (current_date - timedelta(days=2)).replace(day=1)
            markup = await create_calendar("MONTH", prev_month.year, prev_month.month)
            await callback.message.edit_text(
                text=callback.message.text,
                reply_markup=markup
            )
        elif action == "NEXT-MONTH":
            next_month = (current_date + timedelta(days=32)).replace(day=1)
            markup = await create_calendar("MONTH", next_month.year, next_month.month)
            await callback.message.edit_text(
                text=callback.message.text,
                reply_markup=markup
            )
        else:
            await callback.message.edit_text(
                callback_query_id=callback.id,
                text="Something went wrong!"
            )

    return ret_data
