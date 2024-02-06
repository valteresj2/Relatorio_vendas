import streamlit as st
import datetime
import numpy as np
import pandas as pd

import pickle


path_geral='/app'

with open(path_geral+"/x.pkl", "rb") as f:
    flag  = pickle.load(f)

if flag:

    
    local_file_Rpath=path_geral+'/db/base_ref.csv'
  


    dt=pd.read_csv(local_file_Rpath,sep=',')

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
            st.session_state.refeicao=st.number_input("Inserir o valor da refeicao", value=None, placeholder="(Ex.: 3520.30)")
            st.session_state.combustivel=st.number_input("Inserir o valor do combustivel", value=None, placeholder="(Ex.: 3520.30)")
            st.session_state.funilaria=st.number_input("Inserir o valor da funilaria", value=None, placeholder="(Ex.: 3520.30)")
            st.session_state.oficina=st.number_input("Inserir o valor da oficina", value=None, placeholder="(Ex.: 3520.30)")
            st.session_state.acessorios=st.number_input("Inserir o valor de acessorios", value=None, placeholder="(Ex.: 3520.30)")
            st.session_state.pneus=st.number_input("Inserir o valor dos pneus", value=None, placeholder="(Ex.: 3520.30)")
            st.session_state.lavagem=st.number_input("Inserir o valor do lava-jato", value=None, placeholder="(Ex.: 3520.30)")
            st.session_state.comissao=st.number_input("Inserir o valor de comissão", value=None, placeholder="(Ex.: 3520.30)")
            on = st.toggle('Outros')
            if on:
                st.session_state.novo_gasto= st.text_input('Digite o novo tipo de gasto!', '')
                st.session_state.valor_others=st.number_input("Inserir o valor do novo gasto", value=None, placeholder="(Ex.: 3520.30)")
            
            registrar=st.button("Registrar!", on_click=click_button)

            if registrar:
                current_time = datetime.datetime.now()   
                f_data = current_time.strftime("%d-%m-%Y %H:%M:%S")
                dt={'placa':[st.session_state.placa_escolhida],
                    'Data_Registro':[f_data],'Status':['Aberto'],
                    'refeicao':[st.session_state.refeicao],
                    'combustivel':[st.session_state.combustivel],
                    'funilaria':[st.session_state.funilaria],
                    'oficina':[st.session_state.oficina],
                    'acessorios':[st.session_state.acessorios],
                    'pneus':[st.session_state.pneus],
                    'lavagem':[st.session_state.lavagem],
                    'comissao':[st.session_state.comissao],
                    'novo_gasto':[st.session_state.novo_gasto],
                    'valor_novo_gasto':[st.session_state.valor_others]

                    }
                dt=pd.DataFrame(dt)
                local_file_Wpath=path_geral+'/db/base_gasto.csv'
                dt.to_csv(local_file_Wpath,mode='a',index=False)
            
                st.dataframe(dt)
                st.session_state.refeicao=None
                st.session_state.combustivel=None
                st.session_state.funilaria=None
                st.session_state.oficina=None
                st.session_state.acessorios=None
                st.session_state.pneus=None
                st.session_state.lavagem=None
                st.session_state.comissao=None
    else:
        st.write("Não existe carro em situação aberta!")
else:
    st.write('Login não realizado!')
