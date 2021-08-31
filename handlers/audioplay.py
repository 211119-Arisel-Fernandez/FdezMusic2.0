

from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues

import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT, UPDATES_CHANNEL, AUD_IMG, QUE_IMG, GROUP_SUPPORT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from strings import string as tgl

@Client.on_message(command("stream") & other_filters)
@errors
async def stream(_, client, message):

    lel = await message.reply_text(tgl("process_one"))
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Grupo",
                        url=f"https://t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton(
                        text="Canal",
                        url=f"https://t.me/{UPDATES_CHANNEL}")
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Vídeos de más de {DURATION_LIMIT} minuto (s) no se permite reproducir!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text(tgl("where_file"))

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo=f"{QUE_IMG}",
        reply_markup=keyboard,
        caption=f"#la canción solicitada se agregó a la ** cola ** en la posición {position}!\n\n⚡by {bn}")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"{AUD_IMG}",
        reply_markup=keyboard,
        caption=f"💡 **ahora reproduciendo ** una canción solicitada por {costumer} !\n\n⚡by {bn}"
        )
        return await lel.delete()
