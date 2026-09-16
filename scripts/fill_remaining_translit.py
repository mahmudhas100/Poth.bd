import sqlite3

MANUAL_MAP = {
    'কলেজগেট': 'College Gate',
    'বাংলামটর': 'Banglamotor',
    'আসাদগেট': 'Asad Gate',
    'ভিক্টোরিয়াপার্ক': 'Victoria Park',
    'কামারপাড়া': 'Kamarpara',
    'যাত্রাবাড়ী': 'Jatrabari',
    'সাইন্সল্যাবঃ': 'Science Lab',
    'ঘাটারচর': 'Ghatarchar',
    'মোঃপুর': 'Mohammadpur',
    'ধানমন্ডি-১৫': 'Dhanmondi-15',
    'সাইন্সল্যাব:': 'Science Lab',
    'নন্দনপার্ক': 'Nandan Park',
    'কালশী': 'Kalshi',
    'শেওড়াপাড়া': 'Shewrapara',
    'কাঁচপুরব্রীজ': 'Kanchpur Bridge',
    'আনসারক্যাম্প': 'Ansar Camp',
    'কাওরানবাজার': 'Kawran Bazar',
    'কলেজগেইট': 'College Gate',
    'নিউমার্কেট': 'New Market',
    'মিরপুর(১৪)': 'Mirpur (14)',
    'মিরপুর(১০)': 'Mirpur (10)',
    'মিরপুর(১)': 'Mirpur (1)',
    'এয়ারপোর্ট': 'Airport',
    'রাজাবাড়ী': 'Rajabari',
    'কাপাসিয়া': 'Kapasia',
    'মৎস্যভবন': 'Matsya Bhaban',
    'শনিরআখড়া': 'Shanir Akhra',
    'মেঘনাঘাট': 'Meghna Ghat',
    'আসাদগেইট': 'Asad Gate',
    'কোনাবাড়ী': 'Konabari',
    'সায়েন্সল্যাবঃ': 'Science Lab',
    'সায়েন্সল্যাব': 'Science Lab',
    'পাগলাবাজার': 'Pagla Bazar',
    'সায়দাবাদ': 'Sayedabad'
}

def fill_remaining():
    conn = sqlite3.connect('backend/data/busvara.db')
    c = conn.cursor()
    
    updated = 0
    for bn, en in MANUAL_MAP.items():
        c.execute("UPDATE stops SET name_en = ? WHERE name_bn = ?", (en, bn))
        updated += c.rowcount
        
    conn.commit()
    conn.close()
    
    print(f"Successfully applied {updated} manual updates for remaining gaps.")

if __name__ == "__main__":
    fill_remaining()
