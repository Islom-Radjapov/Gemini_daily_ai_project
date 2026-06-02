"""
🤖 Kundalik AI Loyiha Generatori
=================================
Gemini API orqali har kuni kichik to'liq loyiha yaratadi.
Har safar tasodifiy turdagi loyiha tanlanadi.
"""
import os
import re
import json
import random
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from google import genai
# ============================================================
# Sozlamalar
# ============================================================
MODEL_NAME = "gemini-2.5-flash"
# Loyiha turlari ro'yxati
# Tarix faylining joylashuvi
HISTORY_FILE = Path(__file__).parent.parent / "projects" / "history.json"
PROJECT_TYPES = [
    {
        "type": "web_page",
        "name": "HTML/CSS/JS Web Sahifa",
        "description": "Bitta HTML faylda to'liq ishlaydigan interaktiv web sahifa. CSS va JavaScript inline bo'lsin.",
        "tags": ["html", "css", "javascript", "web"],
        "examples": [
            "Portfolio sahifa", "Landing page", "Mahsulot tanishtirish sahifasi",
            "Blog sahifa", "Restoran menyusi", "Ob-havo ko'rsatish sahifasi",
            "Countdown timer sahifa", "Parallax scroll sahifa",
            "Fotosuratlar galereyasi", "Interaktiv xarita sahifasi",
            "Muzika pleyer interfeysi", "Ijtimoiy tarmoq profil sahifasi",
            "Onlayn rezume/CV sahifa", "Kitob do'koni sahifasi",
            "Film afisha sahifasi",
        ]
    },
    {
        "type": "python_cli",
        "name": "Python CLI Dastur",
        "description": "Terminal/konsolda ishlaydigan Python dastur. Faqat standart kutubxonalardan foydalansin.",
        "tags": ["python", "cli", "terminal"],
        "examples": [
            "Parol generatori", "Fayl tashkilotchisi", "To-do ro'yxat",
            "Matn statistikasi", "Valyuta konvertori", "Tasodifiy iqtibos generatori",
            "Katalog daraxtini chizuvchi", "Oddiy shifrlash dasturi",
            "Markdown dan HTML ga konvertor", "Kontakt daftarchasi",
            "Hangman o'yini (terminal)", "Sudoku yechuvchi",
            "Pomodoro taymer", "Matn shablonlar generatori",
            "Oddiy chat bot (terminal)",
        ]
    },
    {
        "type": "js_game",
        "name": "JavaScript Canvas O'yini",
        "description": "HTML5 Canvas yordamida ishlaydigan oddiy o'yin. Bitta HTML faylda to'liq ishlashi kerak.",
        "tags": ["javascript", "canvas", "game", "html"],
        "examples": [
            "Snake o'yini", "Pong o'yini", "Flappy Bird kloni",
            "Asteroid o'yini", "Breakout o'yini", "Memory card o'yini",
            "Tetris kloni", "Space shooter", "Maze o'yini",
            "Whack-a-mole o'yini", "2048 o'yini", "Tic-tac-toe o'yini",
            "Platformer o'yini", "Color match o'yini",
            "Typing speed o'yini",
        ]
    },
    {
        "type": "calculator",
        "name": "Kalkulyator / Konvertor",
        "description": "Bitta HTML faylda ishlaydigan chiroyli kalkulyator yoki konvertor. CSS va JS inline bo'lsin.",
        "tags": ["html", "css", "javascript", "tool"],
        "examples": [
            "Ilmiy kalkulyator", "BMI kalkulyatori", "Yosh hisoblagich",
            "Foiz kalkulyatori", "Valyuta konvertori", "Uzunlik konvertori",
            "Vaqt zonasi konvertori", "Rang konvertori (HEX/RGB/HSL)",
            "Kredit kalkulyatori", "Ip subnet kalkulyatori",
            "Temperatura konvertori", "Tezlik konvertori",
            "Masofa kalkulyatori", "Kaloriya kalkulyatori",
            "Chegirma kalkulyatori",
        ]
    },
    {
        "type": "data_viz",
        "name": "Ma'lumot Vizualizatsiya",
        "description": "HTML Canvas yoki SVG yordamida ma'lumotlarni vizualizatsiya qiluvchi sahifa. Bitta HTML faylda to'liq ishlashi kerak.",
        "tags": ["html", "javascript", "svg", "canvas", "data"],
        "examples": [
            "Doiraviy diagramma", "Ustunli diagramma", "Chiziqli grafik",
            "Bubble chart", "Dunyoning aholisi statistikasi",
            "Soat vizualizatsiyasi", "Audio vizualizer",
            "Sorting algoritm vizualizatsiyasi", "Fraktal generatori",
            "Daraxt vizualizatsiyasi", "Radar chart",
            "Heatmap vizualizatsiya", "Sankey diagramma",
            "Gauge chart", "Treemap vizualizatsiya",
        ]
    },
    {
        "type": "css_animation",
        "name": "CSS Animatsiya",
        "description": "Faqat CSS animatsiyalar bilan ishlaydigan chiroyli sahifa. Minimal JavaScript ishlatilsin.",
        "tags": ["html", "css", "animation"],
        "examples": [
            "Loading spinner kolleksiyasi", "CSS art (hayvon, gullar)",
            "Animatsiyali gradient fon", "3D kub animatsiyasi",
            "Yulduzli osmon animatsiyasi", "Yomg'ir animatsiyasi",
            "Neon matn effekti", "Animatsiyali tugmalar kolleksiyasi",
            "CSS particle effekti", "Animatsiyali soat",
            "Hover effektlar kolleksiyasi", "CSS wave animatsiya",
            "Glitch text effekti", "Morphing shakllar",
            "Animatsiyali progress bar",
        ]
    },
    {
        "type": "quiz_app",
        "name": "Viktorina / Quiz",
        "description": "Interaktiv viktorina yoki test dasturi. HTML/CSS/JS bitta faylda. Kamida 10 ta savol bo'lsin.",
        "tags": ["html", "css", "javascript", "quiz"],
        "examples": [
            "Dasturlash viktorinasi", "Geografiya testi",
            "Matematika viktorinasi", "Tarix viktorinasi",
            "Fan va texnologiya testi", "Til bilish testi",
            "Mantiqiy savolar", "Bayroqlarni top o'yini",
            "Poytaxtlarni top", "Umumiy bilim testi",
            "Emoji viktorinasi", "Musiqa viktorinasi",
            "Kosmik viktorina", "Sport viktorinasi",
            "Hayvonlar viktorinasi",
        ]
    },
    {
        "type": "python_api",
        "name": "Python API / Utility",
        "description": "Foydali Python utility yoki ma'lumot qayta ishlash skripti. Faqat standart kutubxonalar.",
        "tags": ["python", "utility", "api"],
        "examples": [
            "JSON formatlovchi va validatori", "CSV dan HTML jadvalga konvertor",
            "Log fayl analizatori", "Oddiy HTTP server",
            "Fayl dublikatlarini topuvchi", "QR kod generatori (ASCII)",
            "Cron ifodalarini tushuntiruvchi", "Git log statistikasi",
            "Regex tester", "Oddiy unit test framework",
            "YAML parser", "INI config boshqaruvchi",
            "Port scanner", "URL qisqartiruvchi",
            "Matn diff vositasi",
        ]
    },
    {
        "type": "interactive_art",
        "name": "Interaktiv San'at",
        "description": "Sichqoncha yoki klaviatura bilan boshqariladigan interaktiv san'at asari. Bitta HTML faylda.",
        "tags": ["html", "javascript", "canvas", "art"],
        "examples": [
            "Particle system", "Generative art", "Mandelbrot to'plami",
            "Sichqoncha izlovchi particles", "Rangli to'lqinlar",
            "Kaleidoskop", "Fireworks simulyatsiyasi",
            "Lava lampa effekti", "Suyuqlik simulyatsiyasi",
            "Rangli dumaloqlar fizikasi", "Perlin noise landshaft",
            "Spirograph chizuvchi", "Raindrop ripple effekti",
            "Neon chizish doskasi", "Galaxy simulyatsiyasi",
        ]
    },
    {
        "type": "dashboard",
        "name": "Dashboard / Panel",
        "description": "Ma'lumotlar paneli — chiroyli dizayndagi dashboard. Bitta HTML faylda. Soxta ma'lumotlar bilan.",
        "tags": ["html", "css", "javascript", "dashboard"],
        "examples": [
            "Analitika dashboard", "Moliya dashboard",
            "Ob-havo dashboard", "Fitness tracker panel",
            "Loyiha boshqaruv paneli", "Server monitoring panel",
            "Ijtimoiy tarmoq statistikasi", "Savdo dashboard",
            "Energiya iste'moli paneli", "Talabalar baholash paneli",
            "Kripto valyuta tracker", "COVID statistika paneli",
            "HR dashboard", "IoT qurilmalar paneli",
            "Marketing analitika paneli",
        ]
    },
]
# ============================================================
# Tarix (History) tizimi — takroriy loyihalarni oldini olish
# ============================================================
def load_history():
    """Avval yaratilgan loyihalar tarixini yuklash."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"generated": []}
    return {"generated": []}
def save_history(history):
    """Tarixni faylga saqlash."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
def get_all_examples():
    """Barcha loyiha misollarining to'liq ro'yxatini olish."""
    all_examples = []
    for pt in PROJECT_TYPES:
        for ex in pt["examples"]:
            all_examples.append(f"{pt['type']}::{ex}")
    return all_examples
def choose_unique_project(history):
    """Avval yaratilmagan loyihani tanlash.
    
    Agar barcha misollar tugab qolsa, tarixni tozalab boshidan boshlaydi.
    """
    generated_set = set(history.get("generated", []))
    all_examples = get_all_examples()
    
    # Hali yaratilmagan misollarni topish
    remaining = [ex for ex in all_examples if ex not in generated_set]
    
    if not remaining:
        # Barcha misollar yaratilgan — tarixni tozalash va boshidan boshlash
        print("\n🔄 Barcha loyiha misollar yaratilgan! Tarix tozalanmoqda...")
        print(f"   Jami yaratilgan: {len(generated_set)} ta loyiha")
        history["generated"] = []
        save_history(history)
        remaining = all_examples
    
    # Qolgan misollardan tasodifiy tanlash
    chosen = random.choice(remaining)
    type_key, example_name = chosen.split("::", 1)
    
    # Tanlangan turni topish
    project_type = None
    for pt in PROJECT_TYPES:
        if pt["type"] == type_key:
            project_type = pt
            break
    
    print(f"\n📊 Tarix statistikasi:")
    print(f"   Yaratilgan: {len(generated_set)} ta")
    print(f"   Qolgan:     {len(remaining)} ta")
    print(f"   Jami:       {len(all_examples)} ta")
    
    return project_type, example_name, chosen
# ============================================================
# Gemini bilan ishlash
# ============================================================
def get_gemini_client():
    """Gemini API klientini yaratish."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ XATO: GEMINI_API_KEY topilmadi!")
        print("GitHub repo Settings > Secrets > Actions bo'limiga qo'shing.")
        sys.exit(1)
    
    return genai.Client(api_key=api_key)
def generate_project_with_gemini(client, project_type_info, example):
    """Gemini orqali loyiha kodini generatsiya qilish."""
    
    prompt = f"""Sen tajribali dasturchi yordamchisan. Menga kichik lekin TO'LIQ ishlaydigan loyiha yarat.
## Loyiha turi: {project_type_info["name"]}
## Aniq loyiha: {example}
## Tavsif: {project_type_info["description"]}
## Muhim qoidalar:
1. Loyiha TO'LIQ ishlaydigan bo'lishi SHART. Hech qanday placeholder yoki TODO qoldirma.
2. Kod sifatli, chiroyli va professional bo'lsin.
3. Har bir faylni quyidagi formatda ber:
```filename:fayl_nomi.ext
fayl tarkibi shu yerda
```
4. Albatta README.md fayl ham ber, unda:
   - Loyiha nomi va tavsifi
   - Qanday ishga tushirish mumkinligi
   - Xususiyatlar ro'yxati
5. Agar HTML loyiha bo'lsa, barcha CSS va JavaScript bitta HTML faylda bo'lsin (inline).
6. Agar Python loyiha bo'lsa, faqat standart kutubxonalardan foydalan.
7. Dizayn chiroyli, zamonaviy va professional bo'lsin.
8. Izohlar (comments) ingliz tilida bo'lsin.
9. Kodni to'liq yoz, hech narsani qisqartirma.
## Fayl nomlari qoidalari:
- Bo'shliqlar o'rniga pastki chiziq (_) ishlat
- Faqat kichik harflar
- Loyiha nomi bilan bog'liq bo'lsin
Hozir {example} loyihasini to'liq yarat!"""
    print(f"🤖 Gemini dan '{example}' loyihasini so'ramoqdaman...")
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        
        if response.text:
            print(f"✅ Gemini javob berdi! ({len(response.text)} belgi)")
            return response.text, example
        else:
            print("❌ Gemini bo'sh javob qaytardi.")
            return None, example
            
    except Exception as e:
        print(f"❌ Gemini xatosi: {e}")
        return None, example
# ============================================================
# Fayllarni ajratib olish
# ============================================================
def extract_files(response_text):
    """Gemini javobidan fayllarni ajratib olish.
    
    Quyidagi formatlarni qo'llab-quvvatlaydi:
    1. ```filename:fayl_nomi.ext  ...  ```
    2. ```language\n// fayl_nomi.ext  ...  ```
    3. **fayl_nomi.ext**  ```  ...  ```
    """
    files = {}
    
    # 1-format: ```filename:fayl_nomi.ext
    pattern1 = r'```filename:([^\n]+)\n(.*?)```'
    matches1 = re.findall(pattern1, response_text, re.DOTALL)
    for filename, content in matches1:
        filename = filename.strip()
        files[filename] = content.strip()
    
    # 2-format: ```ext\n yoki ``` bilan boshlanib, fayl nomi oldingi qatorda
    if not files:
        # Har xil formatlarni sinab ko'rish
        pattern2 = r'[`*]{1,3}([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)[`*]{0,3}\s*\n\s*```[a-zA-Z]*\n(.*?)```'
        matches2 = re.findall(pattern2, response_text, re.DOTALL)
        for filename, content in matches2:
            filename = filename.strip().strip('`').strip('*')
            files[filename] = content.strip()
    
    # 3-format: ### fayl_nomi.ext yoki #### fayl_nomi.ext
    if not files:
        pattern3 = r'#{2,4}\s+`?([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)`?\s*\n+\s*```[a-zA-Z]*\n(.*?)```'
        matches3 = re.findall(pattern3, response_text, re.DOTALL)
        for filename, content in matches3:
            filename = filename.strip().strip('`')
            files[filename] = content.strip()
    
    # 4-format: oddiy ``` bloklari — kamida bitta fayl bo'lsa
    if not files:
        code_blocks = re.findall(r'```([a-zA-Z]*)\n(.*?)```', response_text, re.DOTALL)
        for i, (lang, content) in enumerate(code_blocks):
            content = content.strip()
            if not content:
                continue
            
            # Tilga qarab fayl nomini aniqlash
            if lang in ('html', 'htm'):
                filename = 'index.html'
            elif lang in ('python', 'py'):
                filename = 'main.py'
            elif lang in ('javascript', 'js'):
                filename = 'script.js'
            elif lang in ('css',):
                filename = 'style.css'
            elif lang in ('json',):
                filename = 'data.json'
            elif lang in ('markdown', 'md'):
                filename = 'README.md'
            else:
                # Kontentga qarab aniqlash
                if '<!DOCTYPE' in content or '<html' in content:
                    filename = 'index.html'
                elif 'def ' in content or 'import ' in content:
                    filename = 'main.py'
                elif 'function ' in content or 'const ' in content:
                    filename = 'script.js'
                else:
                    filename = f'file_{i+1}.txt'
            
            # Dublikat nomlarni oldini olish
            if filename in files:
                base, ext = os.path.splitext(filename)
                filename = f"{base}_{i+1}{ext}"
            
            files[filename] = content
    
    return files
# ============================================================
# Loyihani saqlash
# ============================================================
def create_project_directory(files, project_name, project_type_info, example_name):
    """Loyiha fayllarini saqlash."""
    
    # Sana va loyiha nomi bilan papka yaratish
    tz = timezone(timedelta(hours=5))  # GMT+5
    today = datetime.now(tz).strftime("%Y-%m-%d")
    
    # Loyiha nomi uchun xavfsiz nom yaratish
    safe_name = re.sub(r'[^a-zA-Z0-9\s]', '', example_name)
    safe_name = safe_name.strip().replace(' ', '_').lower()
    safe_name = safe_name[:50]  # Juda uzun bo'lmasligi uchun
    
    project_dir_name = f"{today}_{safe_name}"
    
    # projects/ papkasiga saqlash
    script_dir = Path(__file__).parent.parent
    projects_dir = script_dir / "projects" / project_dir_name
    projects_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Loyiha papkasi: {projects_dir}")
    
    saved_files = []
    
    for filename, content in files.items():
        # Xavfsiz fayl nomi
        safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        file_path = projects_dir / safe_filename
        
        # Papka ichidagi papkani yaratish
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        saved_files.append(safe_filename)
        print(f"  ✅ {safe_filename} saqlandi ({len(content)} belgi)")
    
    # Agar README.md yaratilmagan bo'lsa, oddiy README qo'shish
    readme_exists = any('readme' in f.lower() for f in saved_files)
    if not readme_exists:
        readme_content = f"""# {example_name}
> 🤖 Bu loyiha Gemini AI tomonidan avtomatik yaratilgan
## Loyiha turi
{project_type_info["name"]}
## Yaratilgan sana
{today}
## Teglar
{', '.join(f'`{tag}`' for tag in project_type_info["tags"])}
"""
        readme_path = projects_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        saved_files.append("README.md")
        print(f"  ✅ README.md saqlandi (avtomatik)")
    
    return projects_dir, saved_files
# ============================================================
# Asosiy funksiya
# ============================================================
def main():
    """Asosiy ishga tushirish funksiyasi."""
    
    print("=" * 60)
    print("🤖 Kundalik AI Loyiha Generatori")
    print("=" * 60)
    
    tz = timezone(timedelta(hours=5))
    now = datetime.now(tz)
    print(f"📅 Sana: {now.strftime('%Y-%m-%d %H:%M:%S')} (GMT+5)")
    
    # Yakshanba kunini tekshirish (qo'shimcha himoya)
    if now.weekday() == 6:  # 6 = Yakshanba
        print("📅 Bugun yakshanba — dam olish kuni. Loyiha yaratilmaydi.")
        return
    
    # 1. Tarixni yuklash
    history = load_history()
    
    # 2. Takrorlanmaydigan loyihani tanlash
    project_type, example_name, history_key = choose_unique_project(history)
    print(f"\n🎯 Tanlangan tur: {project_type['name']}")
    print(f"📝 Loyiha: {example_name}")
    
    # 3. Gemini klientini yaratish
    client = get_gemini_client()
    
    # 4. Loyiha generatsiya qilish
    response_text, _ = generate_project_with_gemini(client, project_type, example_name)
    
    if not response_text:
        print("❌ Loyiha generatsiya qilib bo'lmadi. Keyingi safar urinib ko'riladi.")
        sys.exit(1)
    
    # 5. Fayllarni ajratib olish
    files = extract_files(response_text)
    
    if not files:
        print("⚠️ Gemini javobidan fayllarni ajratib bo'lmadi.")
        print("📝 Butun javobni bitta fayl sifatida saqlayman...")
        
        # Javobni aniqlash va to'g'ri kengaytma berish
        if '<!DOCTYPE' in response_text or '<html' in response_text:
            files = {"index.html": response_text}
        elif 'def ' in response_text or 'import ' in response_text:
            files = {"main.py": response_text}
        else:
            files = {"project.txt": response_text}
    
    print(f"\n📄 Topilgan fayllar: {len(files)}")
    for fname in files:
        print(f"   - {fname}")
    
    # 6. Fayllarni saqlash
    project_dir, saved_files = create_project_directory(
        files, example_name, project_type, example_name
    )
    
    # 7. Tarixga qo'shish (qayta generatsiya bo'lmasligi uchun)
    history["generated"].append(history_key)
    save_history(history)
    print(f"\n📜 Tarixga yozildi: {history_key}")
    
    print(f"\n{'=' * 60}")
    print(f"✅ Loyiha muvaffaqiyatli yaratildi!")
    print(f"📁 Papka: {project_dir}")
    print(f"📄 Fayllar soni: {len(saved_files)}")
    print(f"🔢 Jami yaratilgan: {len(history['generated'])} ta")
    print(f"{'=' * 60}")
if __name__ == "__main__":
    main()
