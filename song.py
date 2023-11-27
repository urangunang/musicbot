import os

import requests
import yt_dlp
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch

from AnonXMusic import app, LOGGER


@app.on_message(filters.command(["song", "vsong", "video", "music"]))
async def song(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    m = await message.reply_text("ðŸ”Ž")

    query = "".join(" " + str(i) for i in message.command[1:])
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=5).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as ex:
        LOGGER.error(ex)
        return await m.edit_text(
            f"Ò“á´€ÉªÊŸá´‡á´… á´›á´ Ò“á´‡á´›á´„Êœ á´›Ê€á´€á´„á´‹ Ò“Ê€á´á´ Êá´›-á´…ÊŸ.\n\n**Ê€á´‡á´€sá´É´ :** `{ex}`"
        )

    await m.edit_text("Â» á´…á´á´¡É´ÊŸá´á´€á´…ÉªÉ´É¢ sá´É´É¢,\n\ná´˜ÊŸá´‡á´€sá´‡ á´¡á´€Éªá´›...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"â˜ï¸ á´›Éªá´›ÊŸá´‡ : {title[:23]} \nâ±ï¸ á´…á´œÊ€á´€á´›Éªá´É´ : `{duration}`\nðŸ¥€ á´œá´˜ÊŸá´á´€á´…á´‡á´… Ê™Ê : {app.mention}"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        try:
            visit_butt = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Êá´á´œá´›á´œÊ™á´‡",
                            url=link,
                        )
                    ]
                ]
            )
            await app.send_audio(
                chat_id=message.from_user.id,
                audio=audio_file,
                caption=rep,
                thumb=thumb_name,
                title=title,
                duration=dur,
                reply_markup=visit_butt,
            )
            if message.chat.type != ChatType.PRIVATE:
                await message.reply_text(
                    "á´˜ÊŸá´‡á´€sá´‡ á´„Êœá´‡á´„á´‹ Êá´á´œÊ€ á´˜á´, sá´‡É´á´› á´›Êœá´‡ Ê€á´‡Ç«á´œá´‡sá´›á´‡á´… sá´É´É¢ á´›Êœá´‡Ê€á´‡."
                )
        except:
            start_butt = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="á´„ÊŸÉªá´„á´‹ Êœá´‡Ê€á´‡",
                            url=f"https://t.me/{app.username}?start",
                        )
                    ]
                ]
            )
            return await m.edit_text(
                text="á´„ÊŸÉªá´„á´‹ á´É´ á´›Êœá´‡ Ê™á´œá´›á´›á´É´ Ê™á´‡ÊŸá´á´¡ á´€É´á´… sá´›á´€Ê€á´› á´á´‡ Ò“á´Ê€ á´…á´á´¡É´ÊŸá´á´€á´…ÉªÉ´É¢ sá´É´É¢s.",
                reply_markup=start_butt,
            )
        await m.delete()
    except:
        return await m.edit_text("Ò“á´€ÉªÊŸá´‡á´… á´›á´ á´œá´˜ÊŸá´á´€á´… á´€á´œá´…Éªá´ á´É´ á´›á´‡ÊŸá´‡É¢Ê€á´€á´ sá´‡Ê€á´ á´‡Ê€s.")

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as ex:
        LOGGER.error(ex)
