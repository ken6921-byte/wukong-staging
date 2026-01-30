import telebot, os, openai, subprocess, re

# === 核心配置區域 ===
TG_TOKEN = "8496614831:AAHryVg8FKJqnV4wdD3KYhLjQut59NnF1pA"
OPENAI_KEY = "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"
PROJECT_ROOT = "/opt/wukong/apps/staging"
GITHUB_USER = "ken6921-byte"

bot = telebot.TeleBot(TG_TOKEN)
client = openai.OpenAI(api_key=OPENAI_KEY)

def clean_ai_code(text):
    """移除 AI 生成時自帶的 Markdown 標記"""
    return re.sub(r' ` ` ` [a-zA-Z]*\n|` ` ` ', '', text).strip()

@bot.message_handler(func=lambda message: True)
def handle_automation(message):
    if "悟空" in message.text:
        bot.reply_to(message, "🚀 執行引擎啟動，正在處理自動化開發需求...")
        try:
            # 1. AI 決策邏輯 (確保副總等級美感與專業語氣)
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"你是一位服務於{GITHUB_USER}的全棧工程師。請直接輸出程式碼，具備保險專業感與愛馬仕橘美學。不要解釋，不要Markdown標籤。"},
                    {"role": "user", "content": message.text}
                ]
            )
            code_content = res.choices[0].message.content
            
            # 2. 自動判斷檔案
            target_file = "leads.html" if "leads" in message.text else "index.html"
            file_path = os.path.join(PROJECT_ROOT, "templates", target_file)
            
            # 3. 寫入檔案
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f: 
                f.write(code_content)

            # 4. Git 自動化推送
            subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT)
            subprocess.run(["git", "commit", "-m", f"AI Dev: {target_file} update"], cwd=PROJECT_ROOT)
            push_res = subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT, capture_output=True, text=True)
            
            if push_res.returncode == 0:
                bot.send_message(message.chat.id, f"✅ 任務完成！\n檔案：{target_file} 已成功同步至 GitHub。")
            else:
                bot.reply_to(message, f"❌ Git 推送失敗：{push_res.stderr}")
                
        except Exception as e:
            bot.reply_to(message, f"❌ 系統中止：{str(e)}")
    else:
        pass

print("✅ 悟空機器人已啟動，正在守候指令...")
bot.polling(none_stop=True)
