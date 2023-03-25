import sys
import os
import openai

env_path = os.path.join(os.getcwd(), '.env')
# Открываем файл и читаем все переменные окружения
with open(env_path) as env:
    for line in env:
        # Удаляем пробелы по краям и разбиваем строку на две части по разделителю '='
        key, value = line.strip().split('=')
        # Устанавливаем переменную окружения
        os.environ[key] = value

openai.api_key = os.environ['OPENAI_TOKEN']

engine = "text-davinci-003"

def ask(prompt):
    completion = openai.Completion.create(engine = engine, prompt = prompt, temperature = 0.5, max_tokens = 4096)
    print('Вопрос: ', prompt)
    print('\n>>> Ответ: ')                                    
    print(completion.choices[0]["text"])
    print('>>>')

while (True):
    print("Составьте Ваш запрос в текстовом формате и нажмите enter>>>\nИли введите \"exit\" для завршения программы...")
    prompt = str(input())
    if prompt == "exit":
        sys.exit() 
    ask(prompt)
