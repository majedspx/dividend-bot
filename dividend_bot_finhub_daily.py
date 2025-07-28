
import requests
import schedule
import time
from datetime import datetime
import pytz

# إعدادات المستخدم
API_KEY = "d23qfjhr01qv4g01qf40d23qfjhr01qv4g01qf4g"
TOKEN = "7586050914:AAEtN9efTese1Y5tTrEQeXwI1cRVamEBBzI"
CHAT_ID = "487818111"

# أقوى 50 شركة (أمثلة، يمكن استبدالها بالقائمة الفعلية)
TOP_50_SYMBOLS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK.B", "UNH",
    "JNJ", "V", "PG", "MA", "HD", "XOM", "CVX", "LLY", "MRK", "PEP", "ABBV",
    "KO", "AVGO", "COST", "TMO", "WMT", "DIS", "BAC", "ADBE", "CSCO", "MCD",
    "ABT", "CRM", "DHR", "ACN", "TXN", "PFE", "NFLX", "NKE", "LIN", "INTC",
    "QCOM", "PM", "UNP", "HON", "MDT", "NEE", "BMY", "UPS", "AMGN", "RTX"
]

def get_dividends():
    url = "https://finnhub.io/api/v1/calendar/dividends"
    today = datetime.now(pytz.timezone("Asia/Riyadh")).strftime("%Y-%m-%d")
    params = {
        "from": today,
        "to": today,
        "token": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "dividends" not in data:
        return "❌ لم يتم العثور على توزيعات أرباح اليوم."

    results = []
    for item in data["dividends"]:
        if item["symbol"] in TOP_50_SYMBOLS:
            results.append(
                f"{item['symbol']}: ${item['amount']} للسهم - تاريخ الاستحقاق: {item['exDate']} - العائد: {item.get('dividendYield', 0)*100:.2f}%"
            )

    if not results:
        return "📭 لا توجد توزيعات أرباح لأقوى 50 شركة اليوم."

    message = "📢 *توزيعات الأرباح لأقوى الشركات الأمريكية اليوم:*

"
    message += "\n".join(results)
    return message

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    print("✅ تم إرسال الرسالة." if response.status_code == 200 else f"❌ خطأ: {response.text}")

def job():
    print("📤 جاري إرسال التنبيه...")
    message = get_dividends()
    send_message(message)

# جدولة الإرسال يوميًا الساعة 4 مساءً بتوقيت السعودية
schedule.every().day.at("16:00").do(job)

print("🤖 البوت يعمل وسيقوم بالإرسال يوميًا الساعة ٤ مساءً.")
while True:
    schedule.run_pending()
    time.sleep(30)
