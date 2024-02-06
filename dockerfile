FROM python:3.10.13


#RUN sudo add-apt-repository ppa:mozillateam/firefox-next
#RUN sudo apt-get update
#RUN apt update && apt install software-properties-common -y && add-apt-repository ppa:deadsnakes/ppa
#RUN apt install python3.10 -y
#RUN rm /usr/bin/python3 && ln -s /usr/bin/python3.10 /usr/bin/python

WORKDIR /app

COPY requirements.txt ./requirements.txt
COPY app2.py ./app2.py

RUN mkdir -p /app/credentials

COPY ./credentials/config1.yml ./credentials/config1.yml

RUN mkdir -p /app/db

RUN mkdir -p /app/pages

COPY /pages/Custo.py ./pages/Custo.py
COPY /pages/Registrar_Compra.py ./pages/Registrar_Compra.py
COPY /pages/Venda.py ./pages/Venda.py
COPY /pages/Baixar_Dados.py ./pages/Baixar_Dados.py

#RUN cd /app
RUN pip install streamlit==1.30.0 streamlit-authenticator==0.3.1 pandas==2.2.0 numpy==1.26.3

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["app2.py"]