# Weather Forecast Dashboard

## Loyiha Nomi va Tavsifi

Bu kichik, bitta HTML faylda joylashgan, to'liq ishlaydigan ob-havo ma'lumotlarini ko'rsatish sahifasidir. Foydalanuvchi shaharni kiritib, ushbu shahar uchun joriy ob-havo ma'lumotlarini (harorat, holat, namlik, shamol tezligi) ko'rishi mumkin. Sahifa zamonaviy va minimalistik dizaynga ega bo'lib, OpenWeatherMap API orqali ma'lumotlarni oladi.

## Qanday Ishga Tushirish Mumkin

1.  **`index.html` faylini saqlang:** Yuqoridagi `index.html` kodini yangi faylga nusxalash va uni `index.html` nomi bilan saqlang.
2.  **OpenWeatherMap API Kalitini Oling:**
    *   [OpenWeatherMap](https://openweathermap.org/api) veb-saytiga ro'yxatdan o'ting.
    *   Hisobingizda "API keys" bo'limiga o'ting va bepul API kalitini oling.
3.  **API Kalitini Kodga Qo'ying:**
    *   `index.html` faylini matn muharriri (masalan, VS Code, Sublime Text, Notepad++) bilan oching.
    *   JavaScript kodining boshida `const API_KEY = "YOUR_API_KEY";` qatorini toping.
    *   `"YOUR_API_KEY"` o'rniga o'zingizning OpenWeatherMap API kalitingizni kiriting.
4.  **Faylni Brauzerda Ochish:** `index.html` faylini istalgan veb-brauzerda (Chrome, Firefox, Edge va hokazo) shunchaki ikki marta bosish orqali oching.

Shundan so'ng, sahifa avtomatik ravishda standart shahar ("Tashkent") uchun ob-havoni ko'rsatadi va siz istalgan boshqa shaharni qidirishingiz mumkin.

## Xususiyatlar Ro'yxati

*   **Shaharni Qidirish:** Foydalanuvchi istalgan shahar nomini kiritib, uning ob-havo ma'lumotlarini qidirishi mumkin.
*   **Joriy Ob-havo Ma'lumotlari:** Shahar nomi, harorat (Selsiyda), ob-havo holati (bulutli, quyoshli va h.k.), namlik va shamol tezligi ko'rsatiladi.
*   **Ob-havo Belgisi:** Joriy ob-havo holatini aks ettiruvchi dinamik belgi (ikonka).
*   **Xatolarni Boshqarish:** Agar shahar topilmasa yoki API so'rovida xatolik yuzaga kelsa, foydalanuvchiga qulay xabar ko'rsatiladi.
*   **Zamonaviy Dizayn:** CSS yordamida chiroyli, minimalistik va foydalanuvchi uchun qulay interfeys yaratilgan.
*   **Bitta Fayl:** Barcha HTML, CSS va JavaScript kodlari bitta `index.html` faylida joylashgan bo'lib, uni osonlik bilan ishga tushirish mumkin.
*   **Default Shahr:** Sahifa yuklanganda avtomatik ravishda default shahar (Tashkent) ob-havosini ko'rsatadi.