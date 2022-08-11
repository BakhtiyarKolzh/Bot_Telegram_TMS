FROM python:3

WORKDIR D:\GITHUB\Telegram_bot\Bot_Telegram_TMS
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "main.py" ]

# Настроить и активировать виртуальную среду
# ENV VIRTUAL_ENV "/venv"
# RUN python -m venv $VIRTUAL_ENV
# ENV PATH "$VIRTUAL_ENV/bin:$PATH"


