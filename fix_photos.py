#!/usr/bin/env python3
"""
fix_photos.py
Заменяет все Google Maps фото на Unsplash CDN во всех демо-сайтах.
Запуск: python3 fix_photos.py
"""

import os, re

# Unsplash Source — бесплатный CDN, всегда грузится, релевантные фото по запросу
# Формат: https://source.unsplash.com/WIDTHxHEIGHT/?query
# Или через picsum.photos для гарантированной загрузки без блокировок

PHOTOS = {
    # ── BELLAVISTA ──────────────────────────────────────────────────
    "bellavista": [
        # [старый паттерн в URL, новый URL, alt-описание]
        ("AL8-SNGMQxQWjGAT2mb45",
         "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80&fit=crop",
         "Vista panoramica ristorante"),
        ("AL8-SNFLxGWxlH0n1B",
         "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80&fit=crop",
         "Interno ristorante"),
        ("AL8-SNFyuAGRwTLrG4",
         "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&q=80&fit=crop",
         "Atmosfera serale"),
        ("AL8-SNGIgjd7gm",
         "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80&fit=crop",
         "Sala ristorante"),
        ("AL8-SNF4jvzHoH",
         "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80&fit=crop",
         "Piatti del ristorante"),
    ],

    # ── ERSILIO ─────────────────────────────────────────────────────
    "ersilio": [
        ("ANXAkqFIjCez6",
         "https://images.unsplash.com/photo-1428515613728-6b4607e44363?w=800&q=80&fit=crop",
         "Pizzeria da Ersilio"),
        ("ANXAkqGixrECpnbV",
         "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80&fit=crop",
         "Cucina da Ersilio"),
        ("AL8-SNG6nfXNb2Ck",
         "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=800&q=80&fit=crop",
         "Piatti da Ersilio"),
        ("AL8-SNELIihIrkLl",
         "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&q=80&fit=crop",
         "Pizza artigianale"),
        ("ANXAkqHWfq31",
         "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800&q=80&fit=crop",
         "Ambiente rustico"),
    ],

    # ── BISTROT ─────────────────────────────────────────────────────
    "bistrot": [
        ("AL8-SNGmFlJiBeKO",
         "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&q=80&fit=crop",
         "BistrotEnoteca serata"),
        ("AL8-SNFoCxWCOjV",
         "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80&fit=crop",
         "Atmosfera bistrot"),
        ("AL8-SNE-nENKqzY4",
         "https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80&fit=crop",
         "Cibo internazionale"),
        ("AL8-SNGgM-am8mmm",
         "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80&fit=crop",
         "Hugo e Wilma"),
        ("AL8-SNGO690w1US",
         "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80&fit=crop",
         "Serata speciale"),
    ],

    # ── FATTORIA ────────────────────────────────────────────────────
    "fattoria": [
        ("ANXAkqGca2u8kJOT",
         "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80&fit=crop",
         "La Vecchia Fattoria"),
        ("ANXAkqFo_K7-rlob",
         "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=800&q=80&fit=crop",
         "Esterno ristorante"),
        ("AL8-SNGofjAgTQ",
         "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80&fit=crop",
         "Cucina di qualità"),
        ("AL8-SNHKPa0fJac",
         "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800&q=80&fit=crop",
         "Pesce fresco"),
        ("ANXAkqHxHSh4MMgL",
         "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800&q=80&fit=crop",
         "Piatti fattoria"),
    ],

    # ── SERRAGO ─────────────────────────────────────────────────────
    "serrago": [
        ("AL8-SNHsYRdBNgJv",
         "https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80&fit=crop",
         "Serrago cucina"),
        ("AL8-SNFSbzBX9M2",
         "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80&fit=crop",
         "Serrago piatti"),
    ],

    # ── RONDINELLA ──────────────────────────────────────────────────
    "rondinella": [
        ("AL8-SNEUgCAcIT39",
         "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&q=80&fit=crop",
         "La Rondinella farm"),
        ("AL8-SNEm-c3x6oc",
         "https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800&q=80&fit=crop",
         "Cucina fattoria"),
        ("ANXAkqFDZpXLSXmy",
         "https://images.unsplash.com/photo-1502784444187-359ac186c5bb?w=800&q=80&fit=crop",
         "Agriturismo Calabria"),
        ("ANXAkqHNHYu6406",
         "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&q=80&fit=crop",
         "Orto fattoria"),
        ("AL8-SNG90EO7ZLay",
         "https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=800&q=80&fit=crop",
         "Campagna calabrese"),
    ],
}

def fix_file(filepath, replacements):
    if not os.path.exists(filepath):
        print(f"  ⚠️  File non trovato: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    count = 0

    # Sostituisci ogni URL Google Maps con Unsplash
    for pattern, new_url, alt in replacements:
        # Trova tutti i src che contengono il pattern
        regex = r'(src=["\'])https://(?:lh3\.googleusercontent\.com|maps\.googleapis\.com)[^"\']*' + re.escape(pattern) + r'[^"\']*(["\'])'
        new_src = f'\\1{new_url}\\2'
        new_content, n = re.subn(regex, new_src, content)
        if n > 0:
            content = new_content
            count += n
            print(f"    ✓ {alt} ({n}x)")

    # Fallback: sostituisci tutti i restanti URL Google Maps con foto generiche belle
    remaining = len(re.findall(r'https://lh3\.googleusercontent\.com[^\s"\']+', content))
    if remaining > 0:
        print(f"    ⚡ {remaining} foto Google rimanenti → sostituisco con foto tematiche")
        # Sostituisci con foto cibo/ristorante generiche ma belle
        generic_photos = [
            "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80&fit=crop",
            "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80&fit=crop",
            "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80&fit=crop",
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80&fit=crop",
            "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80&fit=crop",
        ]
        i = 0
        def replacer(m):
            nonlocal i
            url = generic_photos[i % len(generic_photos)]
            i += 1
            return url
        content = re.sub(r'https://lh3\.googleusercontent\.com[^\s"\']+', replacer, content)
        count += remaining

    if count > 0 and content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {count} foto sostituite in {filepath}")
        return True
    elif content == original:
        print(f"  ℹ️  Nessuna foto Google trovata in {filepath}")
        return False

def main():
    print("\n🔧 Fix Photos — sostituisco Google Maps con Unsplash CDN\n")

    demos = [
        ("bellavista/index.html", "bellavista"),
        ("ersilio/index.html", "ersilio"),
        ("bistrot/index.html", "bistrot"),
        ("fattoria/index.html", "fattoria"),
        ("serrago/index.html", "serrago"),
        ("rondinella/index.html", "rondinella"),
    ]

    fixed = 0
    for filepath, name in demos:
        print(f"📁 {name}/index.html")
        replacements = PHOTOS.get(name, [])
        if fix_file(filepath, replacements):
            fixed += 1
        print()

    print(f"✅ Fatto! {fixed} file aggiornati.")
    print("\nOra esegui:")
    print("  git add .")
    print('  git commit -m "Fix: sostituito Google Maps foto con Unsplash CDN"')
    print("  git push")
    print()

if __name__ == "__main__":
    main()
