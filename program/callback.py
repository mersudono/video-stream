# Copyright (C) 2021 By VeezMusicProject

from driver.queues import QUEUE
from pyrogram import Client, filters
from program.utils.inline import menu_markup
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.answer("home start")
    await query.edit_message_text(
        f"""✨ **سلام {message.from_user.mention()} جان !**\n
※ من [{BOT_NAME}](https://t.me/{BOT_USERNAME}) **بهت کمک میکنم تا آهنگ و ویدیوهای دلخواهتو تو ویس چت پخش کنی!**
※ **برای استفاده از من حتما دکمه‌های▪❓راهنمای پایه و 📚دستورات▪رو با یه کلیک بازکن و بخون!**
🇮🇷 **Persianized Version**
🇬🇧 English Version @SickStbot
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ افزودن ربات",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("💛 حمایت", url=f"https://t.me/{OWNER_NAME}")],
                [
                    InlineKeyboardButton("📚 دستورات", callback_data="cbcmds"),
                    InlineKeyboardButton("❓ راهنمای پایه", callback_data="cbhowtouse"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 گروه پشتیبانی", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 کانال رسمی", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.answer("user guide")
    await query.edit_message_text(
        f"""❓ چطور از ربات استفاده کنی؟ , راهنمای پایینو بخون!

1.) ابتدا ربات را به گروه خود اضافه کنید.
2.) سپس، ربات را به عنوان مدیر ترفیع کنید و همه مجوزها را به جز ادمین ناشناس به آن بدهید.
3.) پس از ارتقاء ربات، در گروه دستور /reload را تایپ کنید تا داده های مدیران به روز شود (پس از اضافه کردن مدیر جدید با دستور /reload قابلیت استفاده از ربات را به او بدهید).
4.) یوزربات @{ASSISTANT_NAME} را به گروه خود اضافه کنید یا از دستور /userbotjoin استفاده کنید | اگر مراحل قبل را به درستی انجام دهید بعد از ( /play . . . ریپلی/نام ترَک) یوزربات خود به خود به گروه اضافه میشود!
4.) قبل از شروع استریم ویس چت را باز کنید.

※ و تمام، همه چی با موفقیت پیش رفت!✓

💡 **اگه بازم مشکلی داری میتونی اونو تو گروه پشتیبانی رفع کنی**: @{GROUP_SUPPORT}.""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 بازگشت", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.answer("commands menu")
    await query.edit_message_text(
        f"""✨ **Hello [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**

» با کلیک روی دکمه های زیر راهنمای دلخواهتو بخون!

» ⌊دستورات پایه شامل کارهای مرتبط با بخش استریم میشود⌉
⚡ __قدرت گرفته توسط {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("❗ دستورات ادمین", callback_data="cbadmin"),
                    InlineKeyboardButton("❗ دستورات سودو", callback_data="cbsudo"),
                ],[
                    InlineKeyboardButton("❗ دستورات پایه", callback_data="cbbasic")
                ],[
                    InlineKeyboardButton("🔙 بازگشت", callback_data="cbstart")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.answer("دستورات پایه")
    await query.edit_message_text(
        f"""🏮 لیست دستورات پایه ربات:

» /play (اسم/لینک/ریپلی) - پخش -آهنگ- در ویس چت
» /vplay (اسم/لینک/ریپلی) - پخش -ویدیو- در ویس چت
» /playlist - دریافت پلی لیست گروه
» /video (هرچیزی) - دانلود ویدیو از یوتیوب
» /song (هرچیزی) - دانلود آهنگ از یوتیوب
» /lyric (هرچیزی) - دریافت متن آهنگ
» /search (هرچیزی) - جستجو لینک یوتیوب

» /ping - دریافت وضعیت پینگ ربات
» /uptime - دریافت وضعیت uptime ربات
» /alive - دریافت وضعیت alive ربات (صرفا در گروه)

⚡️ __قدرت گرفته توسط {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 برگشت", callback_data="cbstart")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.answer("دستورات ادمین")
    await query.edit_message_text(
        f"""🏮 لیست دستورات ادمین (گروه):

» /pause - مکث یک ترَک
» /resume - ادامه یک ترَک
» /skip - تغییر|اسکیپ به ترَک بعدی
» /stop - استریم را متوقف کنید
» /vmute - یوزربات را در ویسچت میوت کنید
» /vunmute - میوت بودن یوزربات را در ویسچت لغو کنید
» /volume `1-200` - تغییر حجم صدای آهنگ در استریم (یوزربات باید ادمین باشد)
» /reload - تازه سازی ربات و اطلاعات ادمین های گروه
» /userbotjoin - دعوت یوربات به گروه
» /userbotleave - خروج یوزربات از گروه

⚡️ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 برگشت", callback_data="cbstart")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.answer("دستورات سودو ها")
    await query.edit_message_text(
        f"""🏮 لیست دستورات سودو ها:

» /gban (`username` یا `user id`) - ||مسدود کردن کلی افراد||
» /ungban (`username` یا `user id`) - ||حذف مسدود کلی افراد||
» /speedtest -||اجرای speedtest سرور ربات||
» /sysinfo - ||نمایش اطلاعات سیستم||
» /update - ||بروزرسانی ربات به آخرین نسخه||
» /restart - || ریستارت ربات||

⚡ __Powered by ||Python Pyrogram|| {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 برگشت", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 فقط ادمین های با توانایی دسترسی به ویسچت قادر به استفاده از این دکمه هستند!", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.message.from_user.id
    buttons = menu_markup(user_id)
    chat = query.message.chat.title
    if chat_id in QUEUE:
          await query.edit_message_text(
              f"⚙️ **Settings of** {chat}\n\n⏸ : توقف پخش\n▶️ : ادامه پخش\n🔇 : میوت کردن یوزربات\n🔊 : آنمیوت کردن یوزربات\n⏹ : پایان پخش",
              reply_markup=InlineKeyboardMarkup(buttons),
          )
    else:
        await query.answer("❌ الان چیزی در حال پخش نیست", show_alert=True)


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 فقط ادمین های با توانایی دسترسی به ویسچت قادر به استفاده از این دکمه هستند!", show_alert=True)
    await query.message.delete()
