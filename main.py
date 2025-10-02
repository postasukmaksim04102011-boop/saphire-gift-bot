from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, ConversationHandler, filters
import os

# Состояния для диалогов
ENTER_CARD, ENTER_AMOUNT, ENTER_TON_AMOUNT, ENTER_STARS_AMOUNT, ENTER_DESCRIPTION = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎁 Создать сделку", callback_data="create_deal")],
        [InlineKeyboardButton("👥 Реферальная система", callback_data="referral_system")],
        [InlineKeyboardButton("🌐 Язык", callback_data="change_language")],
        [InlineKeyboardButton("🆘 Поддержка", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "💎 **Saphire Gift**\n\n"
        "Добро пожаловать в проект SAPHIRE – ваш надежный P2P-гарант 😊\n\n"
        "Совершайте сделки на NFT подарки легко и безопасно!\n\n"
        "📌 **Что мы предлагаем:**\n\n"
        "• Автоматический вывод средств и проведение сделок\n"
        "• Реферальная программа с бонусами\n"
        "• Безопасные сделки с полной гаранчией\n"
        "• Передача товаров и услуг через менеджера: @SaphireGift\n\n"
        "Выберите нужный раздел ниже 👍\n\n"
        "---\n"
        "**Реквизиты**"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "create_deal":
        payment_keyboard = [
            [InlineKeyboardButton("💎 TON", callback_data="payment_ton")],
            [InlineKeyboardButton("💳 Карта", callback_data="payment_card")],
            [InlineKeyboardButton("⭐ Звезды", callback_data="payment_stars")],
            [InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_main")]
        ]
        payment_reply_markup = InlineKeyboardMarkup(payment_keyboard)
        
        await query.message.edit_text(
            "💎 **Saphire Gift**\n\n"
            "Выберите метод получения оплаты:",
            reply_markup=payment_reply_markup,
            parse_mode='Markdown'
        )

    elif query.data == "payment_ton":
        await query.message.edit_text(
            "💎 **Saphire Gift**\n\n"
            "---\n"
            "Введите сумму в TON:\n\n"
            "Пример: 10.5",
            parse_mode='Markdown'
        )
        return ENTER_TON_AMOUNT

    elif query.data == "payment_card":
        currency_keyboard = [
            [InlineKeyboardButton("₽ Рубли", callback_data="currency_rub")],
            [InlineKeyboardButton("₴ Гривны", callback_data="currency_uah")],
            [InlineKeyboardButton("🔙 Назад", callback_data="create_deal")]
        ]
        currency_reply_markup = InlineKeyboardMarkup(currency_keyboard)
        
        await query.message.edit_text(
            "💎 **Saphire Gift**\n\n"
            "Выберите валюту:",
            reply_markup=currency_reply_markup,
            parse_mode='Markdown'
        )

    elif query.data == "currency_rub":
        context.user_data['currency'] = 'RUB'
        await query.message.edit_text(
            "💳 **Привязка карты**\n\n"
            "Введите номер банковской карты:\n\n"
            "Пример: 1234 5678 9012 3456",
            parse_mode='Markdown'
        )
        return ENTER_CARD

    elif query.data == "currency_uah":
        context.user_data['currency'] = 'UAH'
        await query.message.edit_text(
            "💳 **Привязка карты**\n\n"
            "Введите номер банковской карты:\n\n"
            "Пример: 1234 5678 9012 3456",
            parse_mode='Markdown'
        )
        return ENTER_CARD

    elif query.data == "payment_stars":
        await query.message.edit_text(
            "💎 **Saphire Gift**\n\n"
            "---\n"
            "Введите количество Звёзд:\n\n"
            "Пример: 1000",
            parse_mode='Markdown'
        )
        return ENTER_STARS_AMOUNT

    elif query.data == "change_language":
        language_keyboard = [
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="language_ru")],
            [InlineKeyboardButton("🇺🇸 English", callback_data="language_en")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
        ]
        language_reply_markup = InlineKeyboardMarkup(language_keyboard)
        
        await query.message.edit_text(
            "💎 **Saphire Gift**\n\n"
            "Выберите язык интерфейса:",
            reply_markup=language_reply_markup,
            parse_mode='Markdown'
        )

    elif query.data == "language_ru":
        await query.message.edit_text("✅ Язык изменен на Русский")

    elif query.data == "language_en":
        await query.message.edit_text("✅ Language changed to English")

    elif query.data == "referral_system":
        await query.message.edit_text("👥 **Реферальная система**\n\nПриглашайте друзей и получайте бонусы!\n\nВаша реферальная ссылка: https://t.me/SaphireGiftBot?start=ref123")

    elif query.data == "support":
        await query.message.edit_text("🆘 **Поддержка**\n\nПо всем вопросам обращайтесь:\n@SaphireGift")

    elif query.data == "back_to_main":
        await start(update, context)

# Обработчики сообщений
async def handle_card_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card_number = update.message.text
    context.user_data['card_number'] = card_number
    
    currency = context.user_data.get('currency', 'RUB')
    currency_name = 'рублях' if currency == 'RUB' else 'гривнах'
    
    await update.message.reply_text(
        f"💳 **Карта привязана:** {card_number}\n\n"
        f"💎 **Saphire Gift**\n\n"
        f"Введите сумму в {currency_name}:",
        parse_mode='Markdown'
    )
    
    return ENTER_AMOUNT

async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.text
    card_number = context.user_data.get('card_number', 'Не указана')
    currency = context.user_data.get('currency', 'RUB')
    
    currency_symbol = '₽' if currency == 'RUB' else '₴'
    currency_name = 'руб.' if currency == 'RUB' else 'грн.'
    
    await update.message.reply_text(
        f"✅ **Сделка создана!**\n\n"
        f"**Метод оплаты:** Банковская карта\n"
        f"**Валюта:** {currency_name}\n"
        f"**Карта:** {card_number}\n"
        f"**Сумма:** {amount} {currency_symbol}\n\n"
        f"Ожидайте подтверждения от покупателя.",
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END

async def handle_ton_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.text
    
    await update.message.reply_text(
        f"✅ **Сделка создана!**\n\n"
        f"**Метод оплаты:** TON\n"
        f"**Сумма:** {amount} TON\n\n"
        f"Ожидайте подтверждения от покупателя.",
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END

async def handle_stars_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stars_amount = update.message.text
    context.user_data['stars_amount'] = stars_amount
    
    await update.message.reply_text(
        f"💎 **Saphire Gift**\n\n"
        f"Количество Звёзд: {stars_amount}\n\n"
        f"---\n"
        f"Опишите, на что сделка:\n\n"
        f"Пример: https://t.me/nft/PlushPepe-555",
        parse_mode='Markdown'
    )
    
    return ENTER_DESCRIPTION

async def handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    description = update.message.text
    stars_amount = context.user_data.get('stars_amount', 'Не указано')
    
    await update.message.reply_text(
        f"✅ **Сделка создана!**\n\n"
        f"**Метод оплаты:** Звёзды\n"
        f"**Количество Звёзд:** {stars_amount}\n"
        f"**Описание:** {description}\n\n"
        f"Сделка отправлена на модерацию.",
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Создание сделки отменено.")
    return ConversationHandler.END

def main():
    # Токен бота
    TOKEN = os.getenv('TELEGRAM_TOKEN') or "8215407859:AAGFlmK7VGW5eDZMKYbPoo-t8raLOXmNNAI"

    # Создание приложения
    app = Application.builder().token(TOKEN).build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # ConversationHandler для диалогов
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={
            ENTER_CARD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_card_number)],
            ENTER_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount)],
            ENTER_TON_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ton_amount)],
            ENTER_STARS_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_stars_amount)],
            ENTER_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)

    # Проверяем, запущено ли на Render
    if os.getenv("RENDER"):
        # Webhook для продакшена
        port = int(os.environ.get("PORT", 10000))
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,
            webhook_url=f"https://your-bot-name.onrender.com/{TOKEN}",
            drop_pending_updates=True
        )
        print("🤖 Бот запущен на Render через Webhook!")
    else:
        # Polling для разработки
        app.run_polling(drop_pending_updates=True)
        print("🤖 Бот запущен локально через Polling!")

if __name__ == "__main__":

    main()
