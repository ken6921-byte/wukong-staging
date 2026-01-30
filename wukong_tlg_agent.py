import telebot, os, openai, subprocess, re

# === 核心配置 (請確保引號完整) ===
TG_TOKEN = "8496614831:AAHryVg8FKJqnV4wdD3KYhLjQut59NnF1pA"
OPENAI_KEY = "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"
PROJECT_ROOT = "/opt/wukong/apps/staging"

bot = telebot.TeleBot(TG_TOKEN)
client = openai.OpenAI(api_key=OPENAI_KEY)

@bot.message_handler(func=lambda message: True)
def handle_automation(message):
    if "悟空" in message.text:
        bot.reply_to(message, "🚀 執行引擎啟動...")
        try:
            new_text = message.text.replace("悟空", "").strip()
            file_path = os.path.join(PROJECT_ROOT, "templates/index.html")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            content = "<html><body><marquee>初始內容</marquee></body></html>"
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f: content = f.read()
            
            new_content = re.sub(r"(<marquee[^>]*>).*?(</marquee>)", rf"\1{new_text}\2", content, flags=re.DOTALL|re.IGNORECASE)
            with open(file_path, "w", encoding="utf-8") as f: f.write(new_content)

            subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT)
            subprocess.run(["git", "commit", "-m", f"AI Update: {new_text}"], cwd=PROJECT_ROOT)
            subprocess.run(["git", "push", "origin", "main", "--force"], cwd=PROJECT_ROOT)
            bot.send_message(message.chat.id, f"✅ 任務完成！內容：{new_text}")
        except Exception as e:
            bot.reply_to(message, f"❌ 執行出錯：{str(e)}")
    else:
        try:
            res = client.chat.completions.create(
                model="gpt-4o", 
                messages=[{"role":"system","content":"你是一位專業的數位行銷與保險專家，稱呼使用者為老闆。說話正式、精簡。"},{"role":"user","content":message.text}]
            )
            bot.reply_to(message, res.choices[0].message.content)
        except Exception as e:
            bot.reply_to(message, f"❌ AI連線失敗：{str(e)}")

print("👑 悟空「全自動執行版」啟動！")
bot.polling(none_stop=True)
