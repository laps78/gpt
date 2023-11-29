from openai import OpenAI

print('Начало работы скрипта...')

prompt = "привет! Ты работаешь?"
key = "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"

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
