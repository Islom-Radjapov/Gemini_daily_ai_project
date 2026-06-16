# 🚀 Simple Python HTTP Server

Bu faqat standart Python kutubxonalaridan foydalanib yaratilgan, kichik, to'liq va ishga yaroqli HTTP serveri. U belgilangan katalogdagi statik fayllarni maxsus xato sahifalari va aniq konsol loglari bilan taqdim etish uchun mo'ljallangan.

## ✨ Xususiyatlar (Features)

*   **Statik fayllarni taqdim etish (Static File Serving)**: HTML, CSS, JavaScript, rasmlar va boshqa statik fayllarni belgilangan katalogdan to'g'ridan-to'g'ri taqdim etadi.
*   **Moslashtiriladigan port va katalog (Customizable Port and Directory)**: Serverning tinglash portini va kontent katalogini buyruq qatori argumentlari orqali osonlik bilan sozlash mumkin.
*   **Maxsus xato sahifalari (Custom Error Pages)**: Agar `404.html` (topilmadi) va `403.html` (kirish taqiqlangan) fayllari taqdim etish katalogida mavjud bo'lsa, ularni avtomatik ravishda taqdim etadi. Aks holda, standart xato sahifalaridan foydalanadi.
*   **Batafsil loglash (Detailed Logging)**: Har bir so'rov uchun konsolga aniq va ma'lumotli loglarni, shu jumladan vaqt tamg'asini va statusni taqdim etadi.
*   **Nazoratli o'chirish (Graceful Shutdown)**: `Ctrl+C` tugmasi bosilganda serverni toza to'xtatadi.
*   **Faqat standart kutubxonalar (Standard Library Only)**: Hech qanday tashqi bog'liqlik talab qilinmaydi, bu esa maksimal moslashuvchanlik va foydalanish qulayligini ta'minlaydi.

## 🚀 Qanday ishga tushirish (How to run)

1.  **Loyiha fayllarini saqlash (Save Project Files)**:
    Barcha yuqoridagi fayllarni bitta papkaga saqlang. `web_content` papkasini `server.py` bilan bir darajada (bir xil ota papkada) joylashtiring.