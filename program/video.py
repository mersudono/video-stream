# Copyright (C) 2021 By Veez Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import re
import asyncio

from config import BOT_USERNAME, IMG_1, IMG_2, IMG_5
from program.utils.inline import stream_markup
from driver.design.thumbnail import thumb
from driver.design.chatname import CHAT_TITLE
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/maxresdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text(
            "شما یک ادمین __ناشناس__ هستید! \n\n«برای استفاده باید تیک **ارسال ناشناس** پنل مدیریت شما غیرفعال شود"
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡برای استفاده ، من باید یک **مدیر** با دسترسی های زیر باشم: \n\n❌__حذف پیام__\n»❌__دعوت کاربران__\n»❌ __مدیریت ویسچت__\n\n بعد از دادن دسترسی ها ، از /reload استفاده کن!"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "💡 برای استفاده، **دسترسی**(های)زیر رو به من بده:"
            + "\n\n» ❌ __مدیریت ویدیوچت__ \n\n بعد از دادن دسترسی ، از /reload استفاده کن!"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "💡 برای استفاده، **دسترسی**(های)زیر رو به من بده:"
            + "\n\n» ❌ __حذف پیام__ \n\n بعد از دادن دسترسی ، از /reload استفاده کن!"
        )
        return
    if not a.can_invite_users:
        await m.reply_text(
            "💡 برای استفاده، **دسترسی**(های)زیر رو به من بده:"
            + "\n\n» ❌__دعوت کاربران__ \n\n بعد از دادن دسترسی ، از /reload استفاده کن!"
        )
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot) 
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
    except UserNotParticipant:
        try:
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **یوزربات اضافه نشد**\n\n**rep**: `{e}`"
            )

    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥 **دانلود Video...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __only 720, 480, 360 allowed__ \n💡 **حالا! استریم ویدیو روی 720p است!**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                    duration = replied.video.duration
                elif replied.document:
                    songname = replied.document.file_name[:70]
                    duration = replied.document.duration
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                title = songname
                userid = m.from_user.id
                thumbnail = f"{IMG_5}"
                image = await thumb(thumbnail, title, userid, ctitle)
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=image,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **ترَک به صف اضافه شد »** `{pos}`\n\n🗂 **Name:** [{songname}]({link}) | `video`\n⏱️ **Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                )
            else:
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                title = songname
                userid = m.from_user.id
                thumbnail = f"{IMG_5}"
                image = await thumb(thumbnail, title, userid, ctitle)
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await loser.edit("🔄 **اضافه شدن به ویدیوچت...**")
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=image,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"🗂 **نام:** [{songname}]({link}) | `video`\n💭 **گروه:** `{chat_id}`\n🧸 **از طرف:** {requester}",
                )
        else:
            if len(m.command) < 2:
                await m.reply(
                    "»  روی یه **قایل ویدویی** ریپلای کن یا **یچیزی رو سرچ کن**"
                )
            else:
                loser = await c.send_message(chat_id, "🔍 **جستجو...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **نتیجه ای پیدا نشد.**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    ctitle = await CHAT_TITLE(gcname)
                    image = await thumb(thumbnail, title, userid, ctitle)
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await loser.edit(f"❌ yt-dl مشکلات یافت شده\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"💡 **ترَک به صف اضافه شد »** `{pos}`\n\n🗂 **Name:** [{songname}]({url}) | `music`\n**⏱ Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                            )
                        else:
                            try:
                                await loser.edit("🔄 **اضافه شدن به ویدیوچت...**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                buttons = stream_markup(user_id)
                                await m.reply_photo(
                                    photo=image,
                                    reply_markup=InlineKeyboardMarkup(buttons),
                                    caption=f"🗂 **نام:** [{songname}]({url}) | `video`\n**⏱ زمان:** `{duration}`\n🧸 **از طرف:** {requester}",
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 خطا: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» reply to an روی یه **فایل ویدیویی** ریپلی کن یا **یچیزی رو سرچ کن**"
            )
        else:
            loser = await c.send_message(chat_id, "🔍 **جستجو...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **نتیجه ای پیدا نشد.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await thumb(thumbnail, title, userid, ctitle)
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ yt-dl مشکلات یافت شده\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        buttons = stream_markup(user_id)
                        await m.reply_photo(
                            photo=image,
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"💡 **ترَک به صف اضافه شد »** `{pos}`\n\n🗂 **نام:** [{songname}]({url}) | `video`\n**⏱ زمان:** `{duration}`\n🧸 **از طرف:** {requester}",
                        )
                    else:
                        try:
                            await loser.edit("🔄 **اضافه شدن به ویدیوچت...**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"🗂 **نام:** [{songname}]({url}) | `music`\n**⏱ زمان:** `{duration}`\n🧸 **از طرف:** {requester}",
                            )
                        except Exception as ep:
                            await loser.delete()
                            await m.reply_text(f"🚫 خطا: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vstream(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text(
            "شما یک ادمین __ناشناس__ هستید! \n\n«برای استفاده باید تیک **ارسال ناشناس** پنل مدیریت شما غیرفعال شود"
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡برای استفاده ، من باید یک **مدیر** با دسترسی های زیر باشم: \n\n❌__حذف پیام__\n»❌__دعوت کاربران__\n»❌ __مدیریت ویسچت__\n\n بعد از دادن دسترسی ها ، از /reload استفاده کن!"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "💡 برای استفاده، **دسترسی**(های)زیر رو به من بده:"
            + "\n\n» ❌ __مدیریت ویسچت__ \n\n بعد از دادن دسترسی ، از /reload استفاده کن!"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "💡 برای استفاده، **دسترسی**(های)زیر رو به من بده:"
            + "\n\n» ❌ __حذف پیام__ \n\n بعد از دادن دسترسی ، از /reload استفاده کن!"
        )
        return
    if not a.can_invite_users:
        await m.reply_text(
            "💡 برای استفاده، **دسترسی**(های)زیر رو به من بده:"
            + "\n\n» ❌__دعوت کاربران__ \n\n بعد از دادن دسترسی ، از /reload استفاده کن! "
        )
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
    except UserNotParticipant:
        try:
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **یوزربات اضافه نشد**\n\n**rep**: `{e}`"
            )

    if len(m.command) < 2:
        await m.reply("» give me a live-link/m3u8 url/youtube link to stream.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await c.send_message(chat_id, "🔄 **processing stream...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» __only 720, 480, 360 allowed__ \n💡 **now streaming video in 720p**"
                )
            loser = await c.send_message(chat_id, "🔄 **processing stream...**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"❌ yt-dl issues detected\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n💭 **Chat:** `{chat_id}`\n🧸 **Request by:** {requester}",
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await loser.edit("🔄 **Joining vc...**")
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    buttons = stream_markup(user_id)
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=f"💡 **[Video Live]({link}) stream started.**\n\n💭 **Chat:** `{chat_id}`\n🧸 **Request by:** {requester}",
                    )
                except Exception as ep:
                    await loser.delete()
                    await m.reply_text(f"🚫 error: `{ep}`")
