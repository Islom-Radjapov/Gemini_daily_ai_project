# Time Zone Converter (Vaqt Zonasi Konvertori)

## Loyiha nomi va tavsifi

**Loyiha nomi:** Time Zone Converter

**Tavsif:** Bu loyiha brauzerda ishlaydigan, foydalanuvchiga bir vaqt zonasidagi ma'lum bir sana va vaqtni boshqa vaqt zonasiga o'tkazish imkonini beruvchi oddiy, ammo to'liq funksional konvertordir. U bitta HTML faylda yaratilgan bo'lib, barcha CSS stil va JavaScript logikasi shu faylning ichida (inline) joylashgan. Loyiha chiroyli va zamonaviy interfeysga ega.

## Qanday ishga tushirish mumkinligi

1.  Yuqoridagi `time_zone_converter.html` fayl tarkibini kompyuteringizda `time_zone_converter.html` nomli faylga saqlang.
2.  Faylni veb-brauzeringizda oching (masalan, Chrome, Firefox, Edge). Shunchaki faylni brauzer oynasiga tortib tashlashingiz yoki fayl joylashgan papkaga borib, uni ikki marta bosishingiz mumkin.

## Xususiyatlar ro'yxati

*   **Sana va vaqt kiritish:** Foydalanuvchi ma'lum bir sanani (kalendar yordamida) va vaqtni (soat va minut) kiritishi mumkin.
*   **Manba va maqsad vaqt zonalarini tanlash:** Keng tarqalgan vaqt zonalari ro'yxatidan manba (source) va maqsad (target) vaqt zonalarini tanlash imkoniyati.
*   **Avtomatik joriy vaqt:** Boshlang'ich sana va vaqt joriy mahalliy sana va vaqtga, manba vaqt zonasi esa foydalanuvchining brauzeri vaqt zonasiga avtomatik ravishda o'rnatiladi.
*   **Tezkor konvertatsiya:** "Convert Time" tugmasini bosish orqali kiritilgan sana va vaqtni manba vaqt zonasidan maqsad vaqt zonasiga tezda o'tkazadi.
*   **To'g'ri vaqt zonasi hisob-kitobi:** Yozgi vaqtga o'tish (Daylight Saving Time) kabi murakkab vaqt zonasi qoidalarini `Intl.DateTimeFormat` yordamida to'g'ri hisobga oladi.
*   **Chiroyli va zamonaviy dizayn:** Toza, minimalistik va foydalanishga qulay interfeys.
*   **Yagona fayl:** Barcha kod (HTML, CSS, JavaScript) bitta `time_zone_converter.html` faylida joylashgan.