#!/bin/bash

# define variables
br="\n\n"

# initial actions
echo "Запуск скрипта установщика бота на сервер ubuntu..."
echo "                                             "
echo " (              (    (       (               "
echo " )\ )    (      )\ ) )\ )    )\ )         )  "
echo "(()/(    )\    (()/((()/(   (()/(    ) ( /(  "
echo " /(_))((((_)(   /(_))/(_))   /(_))( /( )\()) "
echo "(_))   )\ _ )\ (_)) (_))    (_))  )(_)|(_)\  "
echo "| |    (_)_\(_)| _ \/ __|   | |  ((_)_| |(_) "
echo "| |__ _ / _ \ _|  _/\__ \_  | |__/ _\'| '_ \ "
echo "|____(_)_/ \_(_)_|(_)___(_) |____\__,_|_.__/ "
echo "                                             "
echo "L.A.P.S. GPT TELEGRAM BOT ATOMATIC INSTALLER FOR SPRINTBOX v0.1:$br init..."

# create bot user
echo "Будет создан пользователь gpt_bot. Вам будет предложено ввести и подтвердить UNIX пароль, а также заполнить дополнительную информацию о пользователе. Обязательно требуется точно ввести и повторить пароль, остальные данные - просто нажимайте enter";
adduser gpt_bot

# install packages
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip -y

# switch to non-root user & configure user environment
su - gpt_bot
pip3 install virtualenv --user
export PATH=$HOME/.local/bin:$PATH
virtualenv --system-site-packages python
source ~/python/bin/activate

# install libraries
pip install openai telebot datetime
echo "Требуемые модули библиотек python подключены."

# clone project
git clone https://github.com/laps78/gpt && cd gpt # TODO change project repo configuration

# create env & set api tokens
touch .env

echo "                                 _____ "  
echo "________________________________ ___(_)"
echo "_  __ \__  __ \  _ \_  __ \  __ `/_  / "              
echo "/ /_/ /_  /_/ /  __/  / / / /_/ /_  /  "             
echo "\____/_  .___/\___//_/ /_/\__,_/ /_/   "            
echo "      /_/                              "  
echo "***************************************"
echo "Введите токен, полученный на сайте openai.com:"
read OPENAI_TOKEN
echo ""
echo "_____     ______                                      "
echo "__  /________  /___________ _____________ _______ ___ "
echo "_  __/  _ \_  /_  _ \_  __ `/_  ___/  __ `/_  __ `__ \"
echo "/ /_ /  __/  / /  __/  /_/ /_  /   / /_/ /_  / / / / /"
echo "\__/ \___//_/  \___/_\__, / /_/    \__,_/ /_/ /_/ /_/ "
echo "                    /____/                            "
echo "******************************************************"

echo "Введите токен, полученный в Telegram от @botFather:"
read TG_TOKEN
echo "OPENAI_TOKEN=$OPENAI_TOKEN" > .env
echo "TG_TOKEN=$TG_TOKEN" >> .env
echo "Переменные окружения установлены."

# install watchdog daemon systemctl service
cat > /etc/systemd/system/laps-gpt-bot.service << EOF
[Unit]
Description=L.A.P.S. GPT Bot v1.1
After=syslog.target
After=network.target

[Service]
Type=simple
User=gpt_bot
WorkingDirectory=/root/gpt
ExecStart=/usr/bin/python3 /root/gpt/gpt-bot.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable laps-gpt-bot
systemctl start laps-gpt-bot

echo "Демон настроен и активирован";

# final commands
echo "Установка завершена."
