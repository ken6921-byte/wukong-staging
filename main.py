import telebot, os, openai, subprocess, re, sys

# === 核心配置區域 ===
TG_TOKEN = "8496614831:AAHryVg8FKJqnV4wdD3KYhLjQut59NnF1pA"
OPENAI_KEY = "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"
PROJECT_ROOT = "/opt/wukong/apps/staging"

print("--- 系統初始化中 ---")

try:
    bot = telebot.TeleBot(TG_TOKEN)
    client = openai.OpenAI(api_key=OPENAI_KEY)
    print("✅ 配置載入成功")
except Exception as e:
    print(f"❌ 配置載入失敗: {e}")
    sys.exit(1)

def clean_ai_code(text):
    return re.sub(r'```[a-zA-Z]*\n|```', '', text).strip()

@bot.message_handler(func=lambda message: True)
def handle_automation(message):
    print(f"📩 收到指令: {message.text}")
    if "悟空" in message.text:
        bot.reply_to(message, "🚀 執行引擎啟動...")
        try:
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "你是一位專業全棧工程師。請直接輸出程式碼，不要廢話。"},
                          {"role": "user", "content": message.text}]
            )
            code_content = clean_ai_code(res.choices[0].message.content)
            target_file = "leads.html" if "leads" in message.text else "index.html"
            file_path = os.path.join(PROJECT_ROOT, "templates", target_file)
            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f: f.write(code_content)

            subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT)
            subprocess.run(["git", "commit", "-m", f"AI Dev: {target_file}"], cwd=PROJECT_ROOT)
            subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT)
            
            bot.send_message(message.chat.id, f"✅ 任務完成！檔案：{target_file} 已同步。")
        except Exception as e:
            bot.reply_to(message, f"❌ 執行異常：{str(e)}")

print("🚀 悟空機器人正式啟動，正在監聽 Telegram...")
bot.polling(none_stop=True)
