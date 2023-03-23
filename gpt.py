import sys
import openai
openai_token = "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"

openai.api_key = openai_token

engine = "text-davinci-003"
# prompt = str(input())

def ask(prompt):
    completion = openai.Completion.create(engine = engine,
                                      prompt = prompt,
                                      temperature = 0.5,
                                      max_tokens = 1000)
    print('Вопрос: ', prompt)
    print('\nОтвет: ')                                    
    print(completion.choices[0]["text"])

while (True):
    print("Составьте Ваш запрос в текстовом формате и нажмите enter>>>\nИли введите \"exit\" для завршения программы...")
    prompt = str(input())
    prompt == "exit" if sys.exit() else ask(prompt)
