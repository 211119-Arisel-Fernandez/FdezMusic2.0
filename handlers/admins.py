
import traceback
import asyncio
from asyncio import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery, ChatPermissions

from cache.admins import admins
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only, errors
from handlers.play import cb_admin_check
from helpers.filters import command, other_filters
from callsmusic import callsmusic
from callsmusic.queues import queues
from config import LOG_CHANNEL, OWNER_ID, BOT_USERNAME, COMMAND_PREFIXES
from helpers.database import db, dcmdb, Database
from helpers.dbtools import handle_user_status, delcmd_is_on, delcmd_on, delcmd_off
from helpers.helper_functions.admin_check import admin_check
from helpers.helper_functions.extract_user import extract_user
from helpers.helper_functions.string_handling import extract_time


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

# Back Button
BACK_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("¡volver!", callback_data="cbback")]])

@Client.on_message(filters.text & ~filters.private)
async def delcmd(_, message: Message):
    if await delcmd_is_on(message.chat.id) and message.text.startswith("/") or message.text.startswith("!"):
        await message.delete()
    await message.continue_propagation()


@Client.on_message(filters.command("reload"))
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text("✅ ¡Bot ** recargado correctamente!**\n✅ **¡La lista de administradores ** ha sido ** actualizada!**")


# Control Menu Of Player
@Client.on_message(command(["control", f"control@{BOT_USERNAME}", "p"]))
@errors
@authorized_users_only
async def controlset(_, message: Message):
    await message.reply_text(
        "** 💡 ¡menú de control del reproductor de música abierto! **\n\n**💭 puede controlar el reproductor de música con solo presionar uno de los botones de abajo**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⏸ pausa", callback_data="cbpause"
                    ),
                    InlineKeyboardButton(
                        "▶️ reanudar", callback_data="cbresume"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⏩ saltar", callback_data="cbskip"
                    ),
                    InlineKeyboardButton(
                        "⏹ fin", callback_data="cbend"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⛔ anti cmd", callback_data="cbdelcmds"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🛄 herramientas de grupo", callback_data="cbgtools"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Cerrar", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❗¡nada en streaming!")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ música en pausa!")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❗¡nada está en pausa!")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸¡Música reanudada!")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ nada en streaming!")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏹ la transmisión terminó!")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ nada en streaming!")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"⫸ Saltarse: **{skip[0]}**\nReproduciendo ahora: **{qeue[0][0]}**")


@Client.on_message(command("auth") & other_filters)
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        await message.reply("❗ ¡Responde al mensaje para autorizar al usuario!")
        return
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply("🟢 Usuario autorizado.\n\nde ahora en adelante, ese usuario puede usar los comandos de administrador.")
    else:
        await message.reply("✅ Usuario ya autorizado!")


@Client.on_message(command("deauth") & other_filters)
@authorized_users_only
async def deautenticate(client, message):
    global admins
    if not message.reply_to_message:
        await message.reply("❗ Responder al mensaje para desautorizar al usuario!")
        return
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply("🔴 usuario desautorizado.\n\na partir de ahora, el usuario no puede usar los comandos de administrador.")
    else:
        await message.reply("✅ usuario ya desautorizado!")


# this is a anti cmd feature
@Client.on_message(command(["delcmd", f"delcmd@{BOT_USERNAME}"]) & ~filters.private)
@authorized_users_only
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("lea el mensaje /help para saber cómo usar este comando")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            await message.reply_text("✅ Ya activado!")
            return
        else:
            await delcmd_on(chat_id)
            await message.reply_text(
                "🟢 activado con éxito"
            )
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("🔴 Deshabilitado exitosamente")
    else:
        await message.reply_text(
            "lea el mensaje /help para saber cómo usar este comando"
        )


# music player callbacks (control by buttons feature)

@Client.on_callback_query(filters.regex("cbpause"))
@cb_admin_check
async def cbpause(_, query: CallbackQuery):
    chat_id = get_chat_id(query.message.chat)
    if (
        query.message.chat.id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[query.message.chat.id] == "paused"
            ):
        await query.edit_message_text("❗️ nada esta reproduciendo", reply_markup=BACK_BUTTON)
    else:
        callsmusic.pytgcalls.pause_stream(query.message.chat.id)
        await query.edit_message_text("▶️ la música está en pausa", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbresume"))
@cb_admin_check
async def cbresume(_, query: CallbackQuery):
    chat_id = get_chat_id(query.message.chat)
    if (
        query.message.chat.id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[query.message.chat.id] == "resumed"
            ):
        await query.edit_message_text("❗️ nada está en pausa", reply_markup=BACK_BUTTON)
    else:
        callsmusic.pytgcalls.resume_stream(query.message.chat.id)
        await query.edit_message_text("⏸ se reanuda la música", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbend"))
@cb_admin_check
async def cbend(_, query: CallbackQuery):
    chat_id = get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text("❗️ nada esta reproduciendo", reply_markup=BACK_BUTTON)
    else:
        try:
            queues.clear(query.message.chat.id)
        except QueueEmpty:
            pass
        
        callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        await query.edit_message_text("✅ Se borró la cola de música y se abandonó correctamente el chat de voz.", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbskip"))
@cb_admin_check
async def cbskip(_, query: CallbackQuery):
    global que
    chat_id = get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text("❗️ nada esta reproduciendo", reply_markup=BACK_BUTTON)
    else:
        queues.task_done(query.message.chat.id)
        
        if queues.is_empty(query.message.chat.id):
            callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                query.message.chat.id, queues.get(query.message.chat.id)["file"]
            )
            
    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await query.edit_message_text(f"⏭ música omitida\n\n» Saltarse: **{skip[0]}**\n» Reproduciendo ahora: **{qeue[0][0]}**", reply_markup=BACK_BUTTON)

# (C) FdezMusic2.0

# ban & unban function

@Client.on_message(filters.command("b", COMMAND_PREFIXES))
@authorized_users_only
async def ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.kick_member(
            user_id=user_id
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ prohibido con éxito "
                f"{user_first_name}"
                " de este grupo !"
            )
        else:
            await message.reply_text(
                "✅ prohibido "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a>"
                " de este grupo !"
            )


@Client.on_message(filters.command("tb", COMMAND_PREFIXES))
@authorized_users_only
async def temp_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    if not len(message.command) > 1:
        return

    user_id, user_first_name = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "el tipo de tiempo especificado no es válido."
                "use m, h o d, formato de hora: {}"
            ).format(
                message.command[1][-1]
            )
        )
        return

    try:
        await message.chat.kick_member(
            user_id=user_id,
            until_date=until_date_val
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ prohibido temporalmente "
                f"{user_first_name}"
                f" ,prohibido para {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "✅ prohibido temporalmente"
                f"<a href='tg://user?id={user_id}'>"
                "from this group !"
                "</a>"
                f" ,prohibido para {message.command[1]}!"
            )

@Client.on_message(filters.command(["ub", "um"], COMMAND_PREFIXES))
@authorized_users_only
async def un_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.unban_member(
            user_id=user_id
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ Ok aceptado, usuario "
                f"{user_first_name} pueden"
                " unirse a este grupo de nuevo!"
            )
        else:
            await message.reply_text(
                "✅ ok ahora "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a> no es"
                " restringido de nuevo!"
            )

@Client.on_message(filters.command("m", COMMAND_PREFIXES))
async def mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            )
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "✅ okay"
                f"{user_first_name}"
                " silenciado con éxito!"
            )
        else:
            await message.reply_text(
                "✅ okay"
                f"<a href='tg://user?id={user_id}'>"
                "ahora es"
                "</a>"
                "apagado!"
            )


@Client.on_message(filters.command("tm", COMMAND_PREFIXES))
async def temp_mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    if not len(message.command) > 1:
        return

    user_id, user_first_name = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "El tipo de hora especificado no es válido. "
                "use m, h o d, formato de hora: {}"
            ).format(
                message.command[1][-1]
            )
        )
        return

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            ),
            until_date=until_date_val
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Silenciado por un tiempo!"
                f"{user_first_name}"
                f" Silenciado por {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "Silenciado por un tiempo!"
                f"<a href='tg://user?id={user_id}'>"
                "es"
                "</a>"
                " nuevo "
                f" silenciado, para {message.command[1]}!"
            )
