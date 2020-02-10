import asyncio
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from google_images_download import google_images_download
from userbot import (CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, TG_GLOBAL_ALBUM_LIMIT, LOGS, bot)
from userbot.events import register


@register(outgoing=True, pattern="^.gimg(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    response = google_images_download.googleimagesdownload()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    arguments = {
        "keywords": input_str,
        "limit": TG_GLOBAL_ALBUM_LIMIT,
        "format": "jpg",
        "delay": 1,
        "safe_search": True,
        "output_directory": TEMP_DOWNLOAD_DIRECTORY
    }
    paths = response.download(arguments)
    LOGS.info(paths)
    lst = paths[0].get(input_str)
    await bot.send_file(
        event.chat_id,
        lst,
        caption=input_str,
        reply_to=event.message.id,
        progress_callback=progress
    )
    logger.info(lst)
    for each_file in lst:
        os.remove(each_file)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("searched Google for {} in {} seconds.".format(input_str, ms), link_preview=False)
    await asyncio.sleep(5)
    await event.delete()

def progress(current, total):
    LOGS.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))

CMD_HELP.update({
    'gimage':
    '.gimg <search_query>\
        \nUsage: Does an image search on Google and shows 6 images.'
})