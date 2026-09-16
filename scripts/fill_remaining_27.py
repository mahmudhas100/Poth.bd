import sqlite3

MANUAL_MAP = {
    'নারায়ণগঞ্জ লিংক রোড': 'Narayanganj Link Road',
    'মোহাম্মদপুর শিয়া মসজিদ': 'Mohammadpur Shia Masjid',
    'মতিঝিল (শাপলা চত্বর)': 'Motijheel (Shapla Chattar)',
    'মোহাম্মদপুর (আসাদ এভিনিউ)': 'Mohammadpur (Asad Avenue)',
    'মোঃপুর (জাপান গার্ডেন সিটি)': 'Mohammadpur (Japan Garden City)',
    'নাঃগঞ্জ লিংক রোড': 'Narayanganj Link Road',
    'পল্লবী (মিরপুর-১২)': 'Pallabi (Mirpur-12)',
    'মিরপুর-১১ ৩/২': 'Mirpur-11 3/2',
    'মানিকমিয়া এভিনিউ': 'Manik Mia Avenue',
    'আমুলিয়া স্টাফ কোয়ার্টার': 'Amulia Staff Quarter',
    'মানিক মিয়া': 'Manik Mia',
    'গাজীপুর চৌঃ': 'Gazipur Chowrasta',
    'রাজেন্দ্রপুর চৌঃ': 'Rajendrapur Chowrasta',
    'মহাশালী আমতলী': 'Mohakhali Amtoli',
    'ইসিবি চতুর': 'ECB Chattar',
    'মোঃপুর টাউন হল': 'Mohammadpur Town Hall',
    'কুড়িল ফ্লাইওভার': 'Kuril Flyover',
    'বাড্ডা লিংক রোড/মধ্য বাড্ডা': 'Badda Link Road/Moddho Badda',
    'আসাদ গেইট': 'Asad Gate',
    'কালশী মোড়': 'Kalshi More',
    'মোঃ জিল্লুর রহমান ফ্লাইওভার': 'Zillur Rahman Flyover',
    'কলেজ গেইট': 'College Gate',
    'মোহাম্মদপুর (বসিলা রোড)': 'Mohammadpur (Bosila Road)',
    'মোহাম্মদপুর বাস স্ট্যান্ড': 'Mohammadpur Bus Stand',
    'মতিঝিল (নটরডেম কলেজ)': 'Motijheel (Notre Dame College)',
    'ডেমরা স্টাফ কোয়ার্টার': 'Demra Staff Quarter',
    'মেরাদিয়া বাজার': 'Meradia Bazar'
}

def fill_remaining_27():
    conn = sqlite3.connect('backend/data/busvara.db')
    c = conn.cursor()
    
    updated = 0
    for bn, en in MANUAL_MAP.items():
        c.execute("UPDATE stops SET name_en = ? WHERE name_bn = ?", (en, bn))
        updated += c.rowcount
        
    conn.commit()
    conn.close()
    
    print(f"Successfully applied {updated} manual updates for the final 27 gaps.")

if __name__ == "__main__":
    fill_remaining_27()
