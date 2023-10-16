import openai
import os

def init_env():
  # init env
  env_path = os.path.join(os.getcwd(), '.env')
  # Открываем файл и читаем все переменные окружения
  with open(env_path) as env:
      for line in env:
          # Удаляем пробелы по краям и разбиваем строку на две части по разделителю '='
          key, value = line.strip().split('=')
          # Устанавливаем переменную окружения
          os.environ[key] = value

init_env()          
openai.api_key = os.environ("OPENAI_API_KEY")

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Tell the world about the ChatGPT API in the style of a pirate."},
    {"role": "system", "content" : "You’re a kind helpful assistant"}
  ]
)

print(completion.choices[0].message.content)


while True:
    content = input("User: ")
    messages.append({"role": "user", "content": content})
    
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    chat_response = completion.choices[0].message.content
    print(f'ChatGPT: {chat_response}')
    messages.append({"role": "assistant", "content": chat_response})