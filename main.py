import logging
import requests
import urllib.parse
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = '8701827418:AAGVmb-5Bq8Ma20zP4NjTR7O_w6Uaf3GGJo'
HF_TOKEN = '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'

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def get_product_name(image_data):
    response = requests.post(API_URL, headers=headers, data=image_data)
    if response.status_code == 200:
        result = response.json()
        return result[0]['generated_text']
    return None

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    if message.caption:
        product_name = message.caption
    else:
        photo = await message.photo[-1].download(make_dirs=False)
        with open(photo.name, "rb") as f:
            img_bytes = f.read()
        product_name = get_product_name(img_bytes)

    if product_name:
        query = urllib.parse.quote(product_name)
        pdd_link = f"https://mobile.yangkeduo.com/search_result.html?search_key={query}"
        s1688_link = f"https://s.1688.com/youyuan/index.htm?tab=imageSearch&keywords={query}"
        kaspi_link = f"https://kaspi.kz/shop/search/?text={query}"

        response_text = (
            f"✅ {product_name}\n\n"
            f"🇨🇳 [Pinduoduo]({pdd_link})\n"
            f"🇨🇳 [1688]({s1688_link})\n"
            f"🇰🇿 [Kaspi.kz]({kaspi_link})"
        )
        await message.answer(response_text, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
  
