FROM python:3.9.5
LABEL authors="42Maru"

ENV HOME /es-ojt-diane
RUN mkdir -p ${HOME}
WORKDIR ${HOME}

RUN pip install --upgrade pip
ADD requirements.txt ${HOME}
RUN python3.9 -m pip install -r requirements.txt

COPY . ${HOME}
WORKDIR ${HOME}
EXPOSE 14283
CMD ["python", "asgi.py"]