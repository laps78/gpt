from openai import OpenAI

print('Начало работы скрипта...')

prompt = "привет! Ты работаешь?"

client = OpenAI(api_key = key)

responce = client.chat.completions.create(
  messages=[
      {
        "role": "user",
        "content": prompt
      }
    ],
    model = "gpt-4",
  )

print(responce)
