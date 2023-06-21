#!/bin/bash
# initial actions
echo "L.A.P.S. GPT TELEGRAM BOT ATOMATIC INSTALLER FOR SPRINTBOX v0.1:\n\n init..."

# create bot user
echo "Будет создан пользователь gpt_bot. Вам будет предложено ввести и подтвердить UNIX пароль, а также заполнить дополнительную информацию о пользователе. Обязательно требуется точно ввести и повторить пароль, остальные данные - просто нажимайте enter";
echo "adduser gpt_bot";

# install packages
echo "sudo apt update && sudo apt upgrade-y";
echo "sudo apt install python3-pip -y";


# clone project
echo "git clone https://github.com/laps78/gpt && cd gpt";

# create env
echo "touch .env";
echo "Введите токен, полученный на сайте openai.com:"
read OPENAI_TOKEN
echo "Введите токен, полученный в Telegram от @botFather:"
read TG_TOKEN
echo "OPENAI_TOKEN=$OPENAI_TOKEN" > .env
echo "TG_TOKEN=$TG_TOKEN" >> .env
echo "Переменные окружения установлены."

# install libraries
echo "pip install openai telebot datetime --break-system-packages";
echo "Требуемые модули библиотек python подключены."

# install watchdog daemon service
cat > /etc/systemd/system/awesomebot.service << EOF
[Unit]
Description=L.A.P.S. GPT BOT v1.1
After=syslog.target
After=network.target

[Service]
Type=simple
User=gpt_bot
WorkingDirectory=/home/gpt
ExecStart=/usr/bin/python3 /home/gpt/gpt-bot.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "systemctl daemon-reload";
echo "systemctl enable root";
echo "systemctl start root";
echo "Демон настроен и активирован";

# final commands
echo "Установка завершена."
