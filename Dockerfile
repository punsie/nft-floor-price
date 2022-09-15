FROM python:3

ADD fp_kira.py /

ADD requirements.txt /

RUN pip install -r requirements.txt

RUN pip install -U aiohttp

RUN pip install -U discord.py

CMD [ "python", "./fp_kira.py"]

