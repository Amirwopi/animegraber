import requests

BASE_URL = "https://aiofilm.com/wp-json/wp/v2/anime"
all_anime = []
page = 1

while True:
    response = requests.get(BASE_URL, params={"per_page": 100, "page": page})
    if response.status_code != 200:
        print(f"خطا در دریافت داده‌ها: {response.status_code}")
        break

    data = response.json()
    if not data:  # اگر داده‌ای برنگشت، پایان حلقه
        break

    all_anime.extend(data)
    page += 1

print(f"تعداد کل انیمه‌ها: {len(all_anime)}")

# ذخیره داده‌ها در فایل JSON
with open("anime_data.json", "w", encoding="utf-8") as file:
    import json
    json.dump(all_anime, file, ensure_ascii=False, indent=4)

print("داده‌ها با موفقیت ذخیره شدند!")
