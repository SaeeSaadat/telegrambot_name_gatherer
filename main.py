import logging
import os

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler, CallbackQueryHandler
from dotenv import load_dotenv

import handle_list

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Your name is " + update.effective_user.first_name + 'If you want to change it, use /name')


async def name_changer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Your name is " + update.effective_user.first_name + 'If you want to change it, I don\'t care! I haven\'t '
                                                                  'implemented this part yet! XD')


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    response_text = 'کی پایس برای ' + query
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton('پایم', callback_data='opt_in'),
        InlineKeyboardButton('نیستم :(', callback_data='opt_out')
    ]])
    results = [InlineQueryResultArticle(
        id=query,
        title='List for ' + query,
        input_message_content=InputTextMessageContent(response_text),
        reply_markup=keyboard
    )]

    await context.bot.answer_inline_query(update.inline_query.id, results)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    option = query.data
    user = query.from_user.username
    logging.info("\n\n============================")
    logging.info(query)
    logging.info(update.message)
    logging.info(update)
    logging.info(context.chat_data)
    logging.info(context.user_data)
    logging.info(context.chat_data)
    logging.info("============================\n\n")

    current_members = handle_list.get_members(query.chat_instance, query.inline_message_id)
    if option == 'opt_in':
        if user in current_members:
            await context.bot.answer_callback_query(query.id, text="You\'re already in!", show_alert=True)
            return
        else:
            current_members += [user]

    else:
        if user not in current_members:
            await context.bot.answer_callback_query(query.id, text="You\'re not even on the list!", show_alert=True)
            return
        else:
            current_members.remove(user)

    handle_list.update_members(query.chat_instance, query.inline_message_id, current_members)

    message_text = 'لیست پایه‌ها:'
    for i, name in enumerate(current_members):
        message_text += f'\n{i}- {name}'

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton('پایم', callback_data='opt_in'),
        InlineKeyboardButton('نیستم :(', callback_data='opt_out')
    ]])
    await query.edit_message_text(text=message_text, reply_markup=keyboard)


def setup_handlers():
    return [
        CommandHandler('start', start),
        CommandHandler('name', name_changer),
        CallbackQueryHandler(button),
        InlineQueryHandler(inline_query)
    ]


if __name__ == '__main__':
    load_dotenv()
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    for handler in setup_handlers():
        application.add_handler(handler)

    application.run_polling()
