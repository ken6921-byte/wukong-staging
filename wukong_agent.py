import os
import subprocess
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_wukong(prompt):
    # 這裡讓 OpenAI 決定要下什麼 Linux 指令
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "你是一位專業的 AI 工程師。請根據用戶要求，直接輸出修改檔案的 Bash 指令，包含 git commit 與 push。"},
            {"role": "user", "content": prompt}
        ]
    )
    cmd = response.choices[0].message.content
    print(f"悟空正在執行：\n{cmd}")
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    task = input("請輸入指令給悟空：")
    ask_wukong(task)
