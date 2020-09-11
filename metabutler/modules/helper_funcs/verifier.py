import random
import re

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, ChatPermissions
from telegram.ext import CallbackQueryHandler
from telegram.error import BadRequest

from metabutler import dispatcher
import metabutler.modules.sql.welcome_sql as sql

from metabutler.modules.helper_funcs.alternate import send_message


verify_code = ["🙏", "👈", "👉", "👇", "👆", "❤️", "🅰️", "🅱️", "0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
verify_code_links = {
"🙏": "www.google.com", 
"👈": "www.fb.com",
"👉": "www.youtube.com",

def verify_welcome(update, context, chat_id):
	user_id = update.effective_user.id
	is_clicked = sql.get_chat_userlist(chat_id)
	if user_id not in list(is_clicked):
		send_message(update.effective_message, "You are not in verification mode, if you are muted, you can ask the admin of the group for help")
		return
	elif user_id in list(is_clicked) and is_clicked[user_id] == True:
		send_message(update.effective_message, "You are not in verification mode, if you are muted, you can ask the admin of the group for help")
		return
	verify_code = ["️www.google.com"]
	print(len(verify_code))
	real_btn = random.choice(verify_code)
	verify_code.remove(real_btn)
	verbox = (random.randint(1, 3), random.randint(1, 3))
	buttons = []
	linebox = []
	for x in range(3):
		x += 1
		if verbox[1] == x:
			ver1 = True
		else:
			ver1 = False
		for y in range(3):
			y += 1
			if verbox[0] == y and ver1:
				verify_link = real_btn
				linebox.append(InlineKeyboardButton(text=verify_link, callback_data="verify_me(y|{}|{})".format(user_id, chat_id)))
			else:
				verify_link = random.choice(verify_code)
				linebox.append(InlineKeyboardButton(text=verify_link, callback_data="verify_me(n|{}|{})".format(user_id, chat_id)))
				verify_code.remove(verify_emoji)
		buttons.append(linebox)
		linebox = []
	context.bot.send_photo(user_id, photo=verify_code_links[real_btn], caption="Please select matching link below:", parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(buttons))

def verify_button_pressed(update, context):
	chat = update.effective_chat  # type: Optional[Chat]
	user = update.effective_user  # type: Optional[User]
	query = update.callback_query  # type: Optional[CallbackQuery]
	match = re.match(r"verify_me\((.+?)\)", query.data)
	match = match.group(1).split("|")
	is_ok = match[0]
	user_id = match[1]
	chat_id = match[2]
	message = update.effective_message  # type: Optional[Message]
	print("-> {} was clicked welcome verify button".format(user.id))
	if is_ok == "y":
		if context.bot.getChatMember(chat_id, user_id).status in ('left'):
			query.answer(text="Failed: user left chat")
			return
		try:
			context.bot.restrict_chat_member(chat_id, user_id, permissions=ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
			sql.add_to_userlist(chat_id, user_id, True)
			sql.rm_from_timeout(chat_id, user_id)
		except BadRequest as err:
			if not update.effective_chat.get_member(context.bot.id).can_restrict_members:
				query.answer(text="<a href="http://www.google.com/">inline URL</a>", parse_mode="html")
			else:
				query.answer(text="Error: " + str(err))
			return
		chat_name = context.bot.get_chat(chat_id).title
		context.bot.edit_message_media(chat.id, message_id=query.message.message_id, media=InputMediaPhoto(media="https://telegra.ph/file/32dbdc63c6957b8345a32.jpg", caption="*Success!*\n\nGood work human, you can now chat in: *{}*".format(chat_name), parse_mode="markdown"))
		query.answer(text="Success! You can chat in {} now".format(chat_name), show_alert=True)
	else:
		context.bot.edit_message_media(chat.id, message_id=query.message.message_id, media=InputMediaPhoto(media="https://telegra.ph/file/32dbdc63c6957b8345a32.jpg", caption="Sorry robot, you are clicked wrong button.\n\nTry again by click welcome security button.", parse_mode="markdown"))
		query.answer(text="Failed! You are clicked wrong button", show_alert=True)


verify_callback_handler = CallbackQueryHandler(verify_button_pressed, pattern=r"verify_me")

dispatcher.add_handler(verify_callback_handler)
