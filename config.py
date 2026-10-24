import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "nergia-dev-secret")
    DATABASE_URL = os.environ.get("DATABASE_URL", "nergia.db")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    BUSINESS_CONTEXT = """Sen NERGIA Anı Çiçekçilik'in yapay zeka asistanısın.
    Müşterilere çiçek türleri, anlamları, bakım bilgileri, özel gün seçenekleri
    ve ürün önerileri konusunda yardımcı ol.
    NERGIA'nın zarif, premium ve samimi marka dilini koru.
    Kullanıcı ürün veya sipariş konusunda destek isterse ad ve telefon bilgisi
    bırakmaya nazikçe yönlendir.
    Türkçe konuş ve kısa, anlaşılır yanıtlar ver.
    """

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
