import os
import random
from time import sleep
from pyrogram import filters
from bot import LOG, app, advance_config, chats_data, from_chats, to_chats, \
                remove_strings, replace_string, sudo_users
from bot.helper.utils import get_formatted_chat

@app.on_message(filters.chat(from_chats) & filters.incoming)
def work(client, message):
    caption = None
    msg = None
    try:
      for chat in to_chats:
        #unklar
        if caption:
          message.copy(chat, caption=caption)
        elif msg:
          app.send_message(chat, msg)
        else:
          message.copy(chat)
    except Exception as e:
      LOG.error(e)

#/forward command
@app.on_message(filters.user(sudo_users) & filters.command(["fwd", "forward"]), group=1)
def forward(app, message):
    if len(message.command) > 1:
      chat_id = get_formatted_chat(message.command[1], app)
      if chat_id:
        try:
          offset_id = 0
          limit = 0
          if len(message.command) > 2:
            limit = int(message.command[2])
          if len(message.command) > 3:
            offset_id = int(message.command[3])
          for msg in app.iter_history(chat_id, limit=limit, offset_id=offset_id):
            msg.copy(message.chat.id)
            sleep(random.randint(1, 10))
        except Exception as e:
          message.reply_text(f"```{e}```")
      else:
        reply = message.reply_text("```Invalid Chat Identifier. Give me a chat id, username or message link.```")
        sleep(5)
        reply.delete()
    else:
      reply = message.reply_text("```Invalid Command ! Use /fwd {ChatID} {limit} {FirstMessageID}```")
      sleep(20)
      reply.delete()

app.run()
