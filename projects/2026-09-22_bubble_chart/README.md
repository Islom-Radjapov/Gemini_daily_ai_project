# Interactive Bubble Chart Visualization

## Loyiha nomi va tavsifi

**Loyihaning nomi:** Interactive Bubble Chart Visualization

**Tavsif:** Ushbu loyiha bitta HTML faylida to'liq ishlaydigan, HTML Canvas yordamida ma'lumotlarni vizualizatsiya qiluvchi interaktiv Bubble Chart yaratishga qaratilgan. Loyiha turli mamlakatlar bo'yicha uydirma ma'lumotlarni (yalpi ichki mahsulot (GDP), umr ko'rish davomiyligi (Life Expectancy) va aholi soni (Population)) pufak (bubble) shaklida tasvirlaydi. Har bir pufakning o'lchami aholi sonini, gorizontal holati GDPni, vertikal holati esa umr ko'rish davomiyligini ifodalaydi. Foydalanuvchi sichqoncha bilan pufaklar ustiga olib borganida, pufakning batafsil ma'lumotlarini ko'rsatuvchi tooltip paydo bo'ladi.

## Qanday ishga tushirish mumkinligi

1.  **Faylni saqlash:** `bubble_chart.html` nomli fayl yaratib, berilgan kodni unga joylashtiring.
2.  **Brauzerda ochish:** Faylni veb-brauzerda ikki marta bosish orqali oching. (Masalan, Chrome, Firefox, Safari).
3.  **Vizualizatsiyani ko'rish:** Sahifa yuklangach, ma'lumotlar vizualizatsiyasi avtomatik ravishda chiziladi.
4.  **Interaktivlik:** Har bir pufak (bubble) ustiga sichqonchani olib borib, o'sha pufakning batafsil ma'lumotlarini ko'rishingiz mumkin.

Hech qanday server yoki qo'shimcha kutubxonalar talab qilinmaydi, chunki barcha kod HTML, CSS va JavaScript birgina fayl ichida joylashgan.

## Xususiyatlar ro'yxati

*   **To'liq bir faylda:** Barcha HTML, CSS va JavaScript kodlari bitta `bubble_chart.html` faylida birlashtirilgan.
*   **HTML Canvas asosida:** Ma'lumotlarni chizish uchun zamonaviy HTML Canvas API'sidan foydalanilgan.
*   **Bubble Chart:** Uch o'lchovli ma'lumotlarni (X, Y, Size) vizualizatsiya qiladi.
    *   X-o'qi: GDP per Capita (example data)
    *   Y-o'qi: Life Expectancy (example data)
    *   Pufak hajmi: Population (example data)
*   **Interaktiv Tooltip:** Sichqoncha pufak ustiga olib borilganda, pufakning nomi va barcha ma'lumotlarini ko'rsatuvchi tooltip paydo bo'ladi.
*   **Dinamik o'lchov:** Ma'lumotlarning minimal va maksimal qiymatlariga qarab avtomatik ravishda o'lchamlarni hisoblash.
*   **Chiroyli dizayn:** Toza, zamonaviy va professional ko'rinishga ega bo'lib, o'qlar, sarlavhalar va pufaklar uchun aniq ranglar ishlatilgan.
*   **Inglizcha izohlar:** Kod tushunarli bo'lishi uchun izohlar ingliz tilida yozilgan.
*   **Sifatli kod:** Xalqaro dasturlash standartlariga muvofiq yozilgan, o'qishga qulay va yaxshi tuzilishga ega.