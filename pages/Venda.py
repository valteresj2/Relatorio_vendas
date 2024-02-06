import streamlit as st
import datetime
import numpy as np
import pandas as pd


import pickle

path_geral='/opt/render/project/src'

with open(path_geral+"/x.pkl", "rb") as f:
    flag  = pickle.load(f)

if flag:

    
    local_file_path=path_geral+'/db/base_ref.csv'
   

    dt=pd.read_csv(local_file_path,sep=',')

    index=np.where(dt['Status']=='Aberto')[0]

    if 'placa_escolhida' not in st.session_state:
        st.session_state.placa_escolhida=None
    def click_button():
        st.session_state.clicked = True

    if len(index)>0:
        st.session_state.placa_escolhida = st.selectbox(
                'Selecione a placa do veiculo!',
                list(dt.loc[index,'placa']),
                index=None,
                placeholder="Selecione a placa...")
        
        if st.session_state.placa_escolhida!=None:
            st.session_state.status = st.selectbox(
            'Selecione o tipo de movimentação!',
            ['Venda','Troca'],
            index=None,
            placeholder="Selecione a movimentação...")

        st.session_state.vl_venda=st.number_input("Valor de Venda do Veiculo!", value=None, placeholder="(Ex.: 3520.30)")

        uploaded_files = st.file_uploader("Escolha as imagens do veiculo!", accept_multiple_files=True,type=['png', 'jpg'])
        
        registrar=st.button("Registrar!", on_click=click_button)

        if registrar:
            current_time = datetime.datetime.now()   
            f_data = current_time.strftime("%d-%m-%Y %H:%M:%S")

            dt.loc[index,'Status']=st.session_state.status 
            dt.loc[index,'data_venda']=f_data
            dt.loc[index,'Valor_venda']=st.session_state.vl_venda
            dt.to_csv(path_geral+'/db/base_ref.csv',index=False)
            
    else:
        st.write("Não existe carro em situação aberta!")
else:
    st.write('Login não realizado!')
