

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import authorized_users_only
from config import BOT_NAME, BOT_USERNAME, OWNER_NAME, GROUP_SUPPORT, UPDATES_CHANNEL, ASSISTANT_NAME
from handlers.play import cb_admin_check


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>✨ **Bienvenido usuario soy {query.message.from_user.mention}** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) le permiten reproducir música en grupos a través de los nuevos chats de voz de Telegram!**

💡 **Descubre todos los comandos del Bot y cómo funcionan haciendo clic en el » 📚Boton Comandos !**

❓ **Para obtener información sobre todas las características de este bot, simplemente escriba /help**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ Agrégame a tu grupo ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "❓ Cómo usarme", callback_data="cbhowtouse")
                ],[
                    InlineKeyboardButton(
                         "📚 Comandos", callback_data="cbcmds"
                    ),
                    InlineKeyboardButton(
                        "💝 Donar", url=f"https://t.me/{OWNER_NAME}")
                ],[
                    InlineKeyboardButton(
                        "👥 Official Group", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Official Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Hola, bienvenido al menú de ayuda!</b>

**en este menú puede abrir varios menús de comando disponibles, en cada menú de comando también hay una breve explicación de cada comando**

⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Basico", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 Avanzado", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Administrador", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Super Administrador", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📙 Dueño", callback_data="cbowner"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📔 Divertido", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏡VOLVER A AYUDAR", callback_data="cbguide"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 aquí están los comandos básicos</b>

🎧 [ GRUPO COMANDOS CHAT VOZ ]

/play (nombre de la canción): reproduce la canción de youtube
/ytp (nombre de la canción): reproduce la canción directamente desde youtube
/stream (responder al audio): reproduce la canción usando un archivo de audio
/playlist - muestra la lista de canciones en la cola
/song (nombre de la canción) - descargar la canción de youtube
/search (nombre del video): búsqueda detallada de videos de youtube
/vsong (nombre del video) - descarga el video de youtube detallado
/lyric - (nombre de la canción) letras scrapper
/vk (nombre de la canción): descarga la canción desde el modo en línea

🎧 [ CANAL COMANDOS CHAT VOZ ]

/cplay transmite música en el chat de voz del canal
/cplayer - muestra la canción en streaming
/cpause - pausa la transmisión de música
/cresume - reanudar la transmisión se pausó
/cskip - salta la transmisión a la siguiente canción
/cend - finaliza la transmisión de música
/admincache - actualiza la caché de administración
/ubjoinc invita al asistente a unirse a tu canal

⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡Volver", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 aquí están los comandos avanzados</b>

/start (en grupo) - ver el estado activo del bot
/reload - recarga el bot y actualiza la lista de administradores
/cache - actualiza la caché de administración
/ping - verifica el estado del bot ping
/uptime verifique el estado del tiempo de actividad del bot

⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡Volver", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 aquí están los comandos de administrador</b>

/player muestra el estado de reproducción de la música
/pause - pausa la transmisión de música
/resume - reanudar la música se pausó
/skip pasa a la siguiente canción
/end - detener la transmisión de música
/userbotjoin - invita al asistente a unirse a tu grupo
/auth - usuario autorizado para usar el bot de música
/deauth - no autorizado para usar el bot de música
/control abre el panel de configuración del reproductor
/delcmd (on | off) - habilitar / deshabilitar la función del cmd
/musicplayer (activar / desactivar): deshabilita / habilita el reproductor de música en tu grupo
/by /tb (prohibición / prohibición temporal): usuario prohibido de forma permanente o temporal en el grupo
/ub - para un usuario no baneado, estás baneado del grupo
/my /tm (silenciar / silenciar temporalmente): silenciar permanentemente o temporalmente al usuario silenciado en el grupo
/um - para dejar de silenciar al usuario, estás silenciado en el grupo

⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡Volver", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 aquí están los comandos super Administrador</b>

/userbotleaveall - ordena al asistente que se vaya de todos los grupos
/gcast envía un mensaje de difusión a través del asistente
/stats - muestra la estadística del bot

⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡Volver", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbowner"))
async def cbowner(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 aquí están los comandos del propietario</b>

/stats - muestra la estadística del bot
/broadcast envía un mensaje de difusión desde el bot
/block (ID de usuario - duración - motivo): bloquea al usuario por usar su bot
/unblock (identificación de usuario - motivo): desbloquea al usuario que bloqueaste por usar tu bot
/blocklist muestra la lista de usuarios bloqueados por usar su bot

📝 nota: todos los comandos propiedad de este bot pueden ser ejecutados por el propietario del bot sin excepciones.

⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡Volver", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbfun"))
async def cbfun(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🏮 aquí están los comandos divertidos</b>

/chika - compruébalo tú mismo
/wibu - compruébalo tú mismo
/asupan - compruébalo tú mismo
/truth - compruébalo tú mismo
/dare - compruébalo tú mismo

⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡Volver", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ CÓMO USAR ESTE BOT:

1.) primero, agrégame a tu grupo.
2.) luego promocionarme como administrador y otorgar todos los permisos excepto administrador anónimo.
3.) agregar @{ASSISTANT_NAME} a su grupo o escriba /userbotjoin para invitarlo.
4.) primero active el chat de voz antes de comenzar a reproducir música.

⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Lista de Comandos", callback_data="cbhelp"
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


@Client.on_callback_query(filters.regex("close"))
@cb_admin_check
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbback"))
@cb_admin_check
async def cbback(_, query: CallbackQuery):
    await query.edit_message_text(
        "**💡 aquí está el menú de control de bot:**",
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
                        "⛔ anti comandos", callback_data="cbdelcmds"
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


@Client.on_callback_query(filters.regex("cbgtools"))
@cb_admin_check
@authorized_users_only
async def cbgtools(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>esta es la información de la función :</b>

💡 **Característica:** esta función contiene funciones que pueden prohibir, silenciar, desbloquear y reactivar usuarios en su grupo.

y también puede establecer un tiempo para la prohibición y silenciar las sanciones para los miembros de su grupo para que puedan ser liberados del castigo en el tiempo especificado.

❔ **uso:**

1️⃣ prohibir y prohibir temporalmente al usuario de su grupo:
    »Escriba` /b nombre de usuario /responder al mensaje` ban de forma permanente
    »Escriba` /tb nombre de usuario /responder al mensaje / duración` prohibir temporalmente al usuario
    »Escriba` /ub username /responder al mensaje` para desbloquear u

2️⃣ Silenciar y silenciar temporalmente al usuario en tu grupo:
   »Escriba` /m nombre de usuario /responder al mensaje` silenciar permanentemente
    »Escriba` /tm nombre de usuario /responder al mensaje /duración` silenciar temporalmente al usuario
    »Escriba` /um nombre de usuario /responder al mensaje` para dejar de silenciar al usuario

📝nota: comandos /b, /tb y /ub es la función para el usuario baneado / no baneado de su grupo, mientras que /m, /tm y /um son comandos para silenciar / activar el sonido de un usuario en su grupo.

⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡Volver", callback_data="cbback"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbdelcmds"))
@cb_admin_check
@authorized_users_only
async def cbdelcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>esta es la información de la función:</b>
        
**💡 Característica:** eliminar todos los comandos enviados por los usuarios para evitar el spam en grupos !

❔ Uso:**

 1️⃣ para activar la función:
     » escriba `/delcmd on`
    
 2️⃣ para desactivar la función:
     » escriba `/delcmd off`
      
⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡Volver", callback_data="cbback"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbhelps(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 Hola, bienvenido al menú de ayuda!</b>

**en este menú puede abrir varios menús de comando disponibles, en cada menú de comando también hay una breve explicación de cada comando**

⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                 [
                    InlineKeyboardButton(
                        "📚 Basico", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 Avanzado", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Administrador", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Super Administrador", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📙 Dueño", callback_data="cbowner"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📔 Divertido", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏡Volver al Menu", callback_data="cbstart"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ CÓMO USAR ESTE BOT:

1.) primero, agrégame a tu grupo.
2.) luego promocionarme como administrador y otorgar todos los permisos excepto administrador anónimo.
3.) agregar @{ASSISTANT_NAME} a su grupo o escriba /userbotjoin para invitarla.
4.) primero active el chat de voz antes de comenzar a reproducir música.

⚡by {BOT_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏡Volver al Menu", callback_data="cbstart"
                    )
                ]
            ]
        )
    )
