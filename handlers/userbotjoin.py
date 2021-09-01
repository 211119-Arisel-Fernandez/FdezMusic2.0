import asyncio
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from helpers.filters import command
from helpers.decorators import authorized_users_only, errors
from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, SUDO_USERS


@Client.on_message(command(["userbotjoin", f"userbotjoin@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Hazme como administrador primero!</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: Estoy aquí para reproducir música en el chat de voz.")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>Asistente ya en tu chat</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n User {user.first_name} couldn't join your group due to heavy join requests for userbot! Make sure user is not banned in group."
            "\n\nOr manually add Asisstant to your Group and try again</b>",
        )
        return
    await message.reply_text(
        "<b>userbot se unió a tu chat</b>",
    )


@Client.on_message(command(["userbotleave", f"userbotleave@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
@authorized_users_only
async def rem(client, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>¡El usuario no pudo abandonar su grupo! Pueden ser esperas de inundación."
            "\n\nO expulsarme manualmente de tu grupo</b>",
        )
        return
    
@Client.on_message(command(["userbotleaveall", f"userbotleaveall@{BOT_USERNAME}"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("Asistente Abandonando todos los chats")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Asistente saliendo... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"Asistente saliendo... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")


@Client.on_message(command(["userbotjoinchannel", "ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("¿Está el chat incluso vinculado? ?")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Promocioname como administrador de grupo primero!</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: me uní aquí como lo solicitaste")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>Asistente ya en tu canal</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n User {user.first_name} couldn't join your channel due to heavy join requests for userbot! Make sure user is not banned in channel."
            f"\n\nOr manually add @{ASSISTANT_NAME} to your Group and try again</b>",
        )
        return
    await message.reply_text(
        "<b>userbot se unió a tu canal</b>",
    )
