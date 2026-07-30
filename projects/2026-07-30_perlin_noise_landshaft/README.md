# Perlin Noise Landscape: Interactive Art

## Loyiha nomi va tavsifi
**Perlin Noise Landscape** – bu interaktiv, generativ san'at asari bo'lib, dinamik Perlin shovqiniga asoslangan landshaftni tasvirlaydi. Bu landshaft doimiy ravishda harakatlanadi va o'zgaradi, bu esa "parvoz" yoki "sayohat" tuyg'usini beradi. Foydalanuvchilar klaviatura yordamida landshaft bo'ylab harakatlanishlari va uning tafsilotlarini (masshtabini) o'zgartirishlari mumkin, bu esa har safar noyob va jozibali vizual tajriba yaratadi.

## Qanday ishga tushirish mumkinligi
Loyihani ishga tushirish juda oddiy:
1.  `index.html` faylini saqlang.
2.  Ushbu faylni istalgan zamonaviy veb-brauzerda (Chrome, Firefox, Edge, Safari va boshqalar) oching.
3.  Landshaft darhol jonlanishni boshlaydi.

## Xususiyatlar ro'yxati
*   **Dinamik Perlin Shovqini Generatsiyasi**: Landshaft real vaqtda 3D Perlin shovqin funksiyasidan foydalanib yaratiladi va doimiy ravishda rivojlanadi.
*   **Silliq Animatsiya**: `requestAnimationFrame` yordamida optimallashtirilgan animatsiya silliq va uzluksiz vizual tajribani ta'minlaydi.
*   **Klaviatura Boshqaruvi**:
    *   **W / S (yoki Yuqoriga / Pastga o'qlar)**: Landshaft bo'ylab oldinga va orqaga harakatlanish.
    *   **A / D (yoki Chapga / O'ngga o'qlar)**: Landshaft bo'ylab chapga va o'ngga harakatlanish.
    *   **+ / - (yoki '=' / '_')**: Landshaft masshtabini sozlash (yaqinlashtirish/uzoqlashtirish). Bu shovqinning chastotasini o'zgartirib, mayda detallarni yoki kengroq shakllarni ko'rsatadi.
*   **Rangli Landshaft Renderlash**: Balandlik va chuqurlik asosida boy rang gradyenti qo'llanilib, okean chuqurliklaridan tortib, qirg'oq bo'yi qumlariga, yam-yashil o'tloqlarga va qorli cho'qqilarga qadar turli xil relef turlari tasvirlanadi. Chuqurlikka qarab ranglar qorayadi, bu esa perspektiva effektini kuchaytiradi.
*   **Bitta HTML Fayl**: Barcha HTML, CSS va JavaScript kodlari bitta `index.html` faylida birlashtirilgan bo'lib, hech qanday tashqi kutubxona yoki fayllar talab qilinmaydi.
*   **Moslashuvchan Dizayn**: Landshaft brauzer oynasining o'lchamiga avtomatik ravishda moslashadi, bu esa har qanday ekran o'lchamida to'liq ekranni qamrab oluvchi tajribani ta'minlaydi.