import fastf1
import os

# Cache klasörünü oluştur (yoksa hata verebilir)
if not os.path.exists('f1_cache'):
    os.makedirs('f1_cache')

fastf1.Cache.enable_cache('f1_cache')  # Önbelleği aktif et

print("FastF1 kurulumu başarılı! 2025 Sezon verilerine erişim deneniyor...")

try:
    # Test için sadece Bahreyn sıralama seansını hafifçe dürtelim
    session = fastf1.get_session(2025, 1, 'Q')
    print(f"Erişilen Seans: {session.event.EventName} - {session.name}")
    print("Her şey yolunda, yarışa hazırız! 🏁")
except Exception as e:
    print(f"Bir hata oluştu: {e}")