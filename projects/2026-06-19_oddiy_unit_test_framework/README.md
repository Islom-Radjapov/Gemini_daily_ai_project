# PyMiniTest: Oddiy Unit Test Framework

## Loyiha nomi: PyMiniTest

## Tavsif
`PyMiniTest` bu Python uchun mo'ljallangan, juda oddiy va to'liq ishlaydigan unit test framework. U faqat Python standart kutubxonalari yordamida yaratilgan bo'lib, loyihangizda kichik, tezkor va asosiy testlarni yozish va ishga tushirish uchun mo'ljallangan. U `unittest` moduli kabi murakkab funksionalliklarga ega emas, ammo asosiy assert metodlari, testni aniqlash (discovery) va natijalarni hisobot qilish imkoniyatini beradi.

## Qanday ishga tushirish mumkin?

1.  **Loyiha fayllarini saqlash**: Barcha loyiha fayllarini (ya'ni, `micro_test.py`, `test_example.py`, `main_runner.py` va `README.md`) bitta papkaga saqlang.

2.  **Test fayllarini yaratish**:
    *   Testlaringizni `test_` prefiksi bilan boshlanadigan Python fayllarida yozing (masalan, `test_my_app.py`, `test_data_processing.py`).
    *   Har bir test klassi `micro_test.TestCase` dan meros olishi kerak.
    *   Test metodlaringizni `test_` prefiksi bilan boshlang (masalan, `test_my_function_works`, `test_edge_cases`).
    *   Quyidagi misol faylini ko'rib chiqing: `test_example.py`. Unda `setup` va `teardown` metodlaridan foydalanish, shuningdek, turli assert metodlari va kutilmagan xatolarni qanday tekshirish ko'rsatilgan.

3.  **Testlarni ishga tushirish**:
    *   Terminalni loyiha fayllari joylashgan papkaga o'ting.
    *   `main_runner.py` skriptini ishga tushiring: