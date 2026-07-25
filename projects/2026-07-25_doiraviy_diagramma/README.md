# Interactive Pie Chart Visualization

## Loyiha nomi: Interaktiv Doiraviy Diagramma Vizualizatsiyasi

## Tavsif:
Ushbu loyiha bitta HTML faylda to'liq ishlaydigan interaktiv doiraviy diagramma (pie chart) vizualizatsiyasini taqdim etadi. HTML Canvas API yordamida ma'lumotlar dinamik ravishda chiziladi va foydalanuvchiga sichqonchani diagramma ustiga olib borganida ma'lumotlar haqida qisqacha ma'lumot (tooltip) ko'rsatiladi. Foydalanuvchilar o'z ma'lumotlarini JSON formatida kiritib, diagrammani yangilashlari mumkin. Loyiha zamonaviy va toza dizaynga ega bo'lib, standart HTML, CSS va JavaScript yordamida yaratilgan.

## Qanday ishga tushirish mumkin:
1. `pie_chart_visualization.html` faylini kompyuteringizga yuklab oling.
2. Faylni istalgan zamonaviy veb-brauzerda (Chrome, Firefox, Safari, Edge va h.k.) oching.
   Masalan, fayl explorerda `pie_chart_visualization.html` faylini ikki marta bosing.

Loyihani ishga tushirish uchun hech qanday server yoki qo'shimcha konfiguratsiya talab qilinmaydi.

## Xususiyatlar:
*   **Dinamik Doiraviy Diagramma:** HTML Canvas yordamida ma'lumotlarni vizualizatsiya qiluvchi to'liq ishlaydigan doiraviy diagramma.
*   **Moslashtiriladigan Ma'lumotlar:** Foydalanuvchilar o'z ma'lumotlarini JSON formatida kiritish orqali diagrammani o'zgartira oladilar. Ma'lumotlar `[{"label": "Category", "value": 123}, ...]` formatida bo'lishi kerak.
*   **Interaktiv Tooltip-lar:** Sichqoncha diagramma segmentlari ustiga olib borilganda, segment nomi, qiymati va foizini ko'rsatuvchi interaktiv tooltip-lar paydo bo'ladi.
*   **Zamonaviy va Toza Dizayn:** Estetik jihatdan yoqimli ranglar palitrasi va toza, professional interfeysga ega.
*   **Legend (Afsona):** Diagrammadagi har bir segment uchun rangli ko'rsatkich va etiketkalarni o'z ichiga olgan afsona.
*   **Yagona HTML Fayl:** Barcha HTML, CSS va JavaScript kodlari bitta faylda joylashgan bo'lib, uni ishga tushirish va bo'lishishni juda oson qiladi.
*   **Barcha Standartlar:** Faqat standart veb-texnologiyalar (HTML, CSS, JavaScript) va Canvas API-dan foydalanilgan.
*   **Mobil Qurilmalarga Mos (Responsive):** Diagramma va sahifa turli ekran o'lchamlariga moslashadi.