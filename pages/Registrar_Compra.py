import streamlit as st

import datetime
import numpy as np
import pandas as pd
import requests
import ast
import pickle

path_geral='/opt/render/project/src'

with open(path_geral+"/x.pkl", "rb") as f:
    flag  = pickle.load(f)



if flag:

    

    def click_button():
        st.session_state.clicked = True

    if 'marca' not in st.session_state:
        st.session_state.marca=None

    if 'modelo' not in st.session_state:
        st.session_state.modelo=None

    if 'cor_veiculo' not in st.session_state:
        st.session_state.cor_veiculo=None

    if 'ano_fabricacao' not in st.session_state:
        st.session_state.ano_fabricacao=None

    if 'info_fipe' not in st.session_state:
        st.session_state.info_fipe=None

    if 'valor_compra' not in st.session_state:
        st.session_state.valor_compra=None

    placa = st.text_input('Digite a placa do Veiculo!', '')
    placa=placa.upper()

    st.session_state.valor_compra=st.number_input("Inserir o valor de compra", value=None, placeholder="(Ex.: 3520.30)")



    r = requests.get('https://parallelum.com.br/fipe/api/v1/carros/marcas')
    marca_v=[]
    codigo_v=[]
    list_marca=ast.literal_eval(r.text)
    for i in list_marca:
        marca_v.append(i['nome'])
        codigo_v.append(i['codigo'])


    st.session_state.tp_compra = st.selectbox(
        'Qual a modalidade da compra?',
        ['Compra','Troca'],
        index=None,
        placeholder="Selecione a modalidade...")

    st.session_state.marca = st.selectbox(
        'Selecione a marca do veiculo!',
        marca_v,
        index=None,
        placeholder="Selecione a marca...")
    #marca='Nissan'
    #http_modelo='https://parallelum.com.br/fipe/api/v1/carros/marcas/'+codigo_v[np.where(marca==np.array(marca_v))[0][0]]+'/modelos'
    if st.session_state.marca!=None:
        http_modelo='https://parallelum.com.br/fipe/api/v1/carros/marcas/'+codigo_v[np.where(st.session_state.marca==np.array(marca_v))[0][0]]+'/modelos'
        r_modelos = requests.get(http_modelo)
        list_modelo=ast.literal_eval(r_modelos.text)
        modelo_v=[]
        codigo_mv=[]
        for i in list_modelo['modelos']:
            modelo_v.append(i['nome'])
            codigo_mv.append(i['codigo'])

        st.session_state.modelo = st.selectbox(
        'Selecione o modelo do veiculo!',
        modelo_v,
        index=None,
        placeholder="Selecione o modelo...")
        #modelo='MARCH SL 1.6 16V FlexStart 5p Aut.'
        #http_modelo='https://parallelum.com.br/fipe/api/v1/carros/marcas/'+codigo_v[np.where(marca==np.array(marca_v))[0][0]]+'/modelos/'+str(codigo_mv[np.where(modelo==np.array(modelo_v))[0][0]])+'/anos'
        if st.session_state.modelo!=None:
            http_modelo='https://parallelum.com.br/fipe/api/v1/carros/marcas/'+codigo_v[np.where(st.session_state.marca==np.array(marca_v))[0][0]]+'/modelos/'+str(codigo_mv[np.where(st.session_state.modelo==np.array(modelo_v))[0][0]])+'/anos'
            r_anos = requests.get(http_modelo)
            list_anos=ast.literal_eval(r_anos.text)
            ano_v=[]
            codigo_av=[]
            for i in list_anos:
                ano_v.append(i['nome'])
                codigo_av.append(i['codigo'])

            st.session_state.ano_fabricacao = st.selectbox(
            'Selecione o ano do veiculo!',
            ano_v,
            index=None,
            placeholder="Selecione o ano...")

            #ano_fabricacao='2019 Gasolina'
            #http_modelo='https://parallelum.com.br/fipe/api/v1/carros/marcas/'+codigo_v[np.where(marca==np.array(marca_v))[0][0]]+'/modelos/'+str(codigo_mv[np.where(modelo==np.array(modelo_v))[0][0]])+'/anos/'+codigo_av[np.where(ano_fabricacao==np.array(ano_v))[0][0]]

            if st.session_state.ano_fabricacao!=None:
                http_modelo='https://parallelum.com.br/fipe/api/v1/carros/marcas/'+codigo_v[np.where(st.session_state.marca==np.array(marca_v))[0][0]]+'/modelos/'+str(codigo_mv[np.where(st.session_state.modelo==np.array(modelo_v))[0][0]])+'/anos/'+codigo_av[np.where(st.session_state.ano_fabricacao==np.array(ano_v))[0][0]]
                r_valor = requests.get(http_modelo)
                st.session_state.info_fipe=ast.literal_eval(r_valor.text)

            cor=['Branco','Prata','Preto','Cinza','Vermelho','Marrom/Bege','Azul','Verde','Amarelo/Dourado','Outros']

            st.session_state.cor_veiculo = st.selectbox(
                'Selecione a cor do veiculo!',
                cor,
                index=None,
                placeholder="Selecione a cor...")
            
            uploaded_files = st.file_uploader("Escolha as imagens do veiculo!", accept_multiple_files=True,type=['png', 'jpg'])




    if (len(placa)>0) & (st.session_state.marca!=None) & (st.session_state.modelo!=None)  & (st.session_state.cor_veiculo!=None) & (st.session_state.info_fipe!=None) & (st.session_state.valor_compra!=None):
        registrar=st.button("Registrar!", on_click=click_button)

        if registrar:
            current_time = datetime.datetime.now()   
            f_data = current_time.strftime("%d-%m-%Y %H:%M:%S")
            dt={'placa':[placa],'tipo_compra':[st.session_state.tp_compra],'marca':[st.session_state.marca],'modelo':[st.session_state.modelo],'ano':str(st.session_state.info_fipe['AnoModelo']),'cor':[st.session_state.cor_veiculo],
                'Valor_Fipe':st.session_state.info_fipe['Valor'],'Valor_Compra': st.session_state.valor_compra,'Codigo_Fipe':st.session_state.info_fipe['CodigoFipe'],
                'Data_Registro':[f_data],'Status':['Aberto'],'data_venda':[None],'Valor_venda':[None]

                }
            dt=pd.DataFrame(dt)
            local_file_path=path_geral+'/db/base_ref.csv'
            dt.to_csv(local_file_path,mode='a',index=False)
            

            st.dataframe(dt)
else:
    st.write('Login não realizado!')


