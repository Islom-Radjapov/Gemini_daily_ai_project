# Interactive Kaleidoscope

## Loyiha nomi va tavsifi

**Interactive Kaleidoscope** bu HTML Canvas API yordamida yaratilgan interaktiv san'at asari. U foydalanuvchiga sichqoncha yoki klaviatura orqali dinamik, simmetrik naqshlar yaratish imkonini beradi. Har bir chiziq yoki shakl kaleydoskopning markaziy nuqtasi atrofida ko'p marta aks etib, doimiy o'zgaruvchan vizual tajribani taqdim etadi.

## Qanday ishga tushirish mumkinligi

Loyiha bitta HTML faylidan iborat bo'lib, uni ishga tushirish juda oddiy:

1.  Ushbu loyiha faylini ( `interactive_kaleidoscope.html`) kompyuteringizga yuklab oling.
2.  Faylni veb-brauzeringizda (Chrome, Firefox, Edge va hokazo) oching. Buning uchun faylni ikki marta bosish yoki brauzerga sudrab olib borish kifoya.

Loyihani ishga tushirish uchun hech qanday qo'shimcha veb-server yoki kutubxonalar talab qilinmaydi.

## Xususiyatlar ro'yxati

*   **To'liq ekran rejimi:** Kaleydoskop brauzer oynasini to'liq egallaydi va oyna o'lchami o'zgarganda avtomatik ravishda moslashadi (responsive design).
*   **Sichqoncha bilan chizish:** Sichqonchani surish orqali dinamik, rang-barang naqshlar yarating. Cho'tka hajmi chizish tezligiga qarab o'zgaradi.
*   **Sichqoncha bilan boshqarish:**
    *   **Sichqonchani surish:** Naqshlarni chizish.
    *   **Chap tugmani bosish:** Yangi chizishni boshlaydi va cho'tkaning rangini o'zgartiradi.
*   **Klaviatura bilan boshqarish:**
    *   **Arrow Keys (Yo'nalish tugmalari):** Chizish cho'tkasini canvas bo'ylab harakatlantiradi.
    *   **Spacebar (Probel):** Chizish rejimini yoqish/o'chirish (agar yoqilgan bo'lsa, chizishni boshlaydi; o'chirilgan bo'lsa, to'xtatadi) va shu bilan birga cho'tkaning rangini o'zgartiradi.
    *   **R tugmasi:** Canvas'ni tozalaydi va barcha chizmalarni o'chirib tashlaydi.
    *   **P tugmasi:** Animatsiyani to'xtatish/davom ettirish.
    *   **I tugmasi:** Ekranda ko'rsatilgan qo'llanmalarni ko'rsatish/yashirish.
*   **Dinamik ranglar:** Har bir yangi chizish yangi rang bilan boshlanadi, bu ranglar avtomatik ravishda HSL rang modelida aylantiriladi.
*   **Professional ko'rinish:** Minimalistik dizayn, silliq animatsiyalar va interaktiv elementlar orqali foydalanuvchiga yoqimli tajriba taqdim etiladi.