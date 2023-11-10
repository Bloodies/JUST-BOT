import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

now = datetime.now()


def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return f"CALENDAR;{action};{year}:{month}:{day}"


def create_calendar(
        year: datetime.year = now.year,
        month: datetime.month = now.month
):
    data_ignore = create_callback_data("IGNORE", year, month, 0)

    builder = InlineKeyboardBuilder()

    # First row - Month and Year
    keyboard = [[InlineKeyboardButton(text=f"{month} {year}", callback_data=data_ignore)]]

    # Second row - Week Days
    row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row.append(InlineKeyboardButton(text=day, callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data=data_ignore))
            else:
                row.append(
                    InlineKeyboardButton(text=str(day), callback_data=create_callback_data("DAY", year, month, day)))
        keyboard.append(row)
    # Last row - Buttons
    row = [InlineKeyboardButton(text="<", callback_data=create_callback_data("PREV-MONTH", year, month, day)),
           InlineKeyboardButton(text=" ", callback_data=data_ignore),
           InlineKeyboardButton(text=">", callback_data=create_callback_data("NEXT-MONTH", year, month, day))]
    keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def process_calendar_selection(update, context):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """
    ret_data = (False, None)
    query = update.callback_query
    print(query)
    print(query.data)
    (_, action, year, month, day) = query.data.split(";")
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        context.bot.answer_callback_query(callback_query_id=query.id)
    elif action == "DAY":
        context.bot.edit_message_text(text=query.message.text,
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id
                                      )
        ret_data = True, datetime.datetime(int(year), int(month), int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        context.bot.edit_message_text(text=query.message.text,
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      reply_markup=create_calendar(int(pre.year), int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        context.bot.edit_message_text(text=query.message.text,
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      reply_markup=create_calendar(int(ne.year), int(ne.month)))
    else:
        context.bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
        # UNKNOWN
    return ret_data
