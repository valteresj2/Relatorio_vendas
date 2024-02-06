import streamlit as st
import pandas as pd
import os
import pickle

path_geral='/opt/render/project/src'

with open(path_geral+"/x.pkl", "rb") as f:
    flag  = pickle.load(f)



if flag:

    local_file_Rpath=path_geral+'/db/base_ref.csv'
    st.session_state.exist_ref = os.path.exists(local_file_Rpath)
    if st.session_state.exist_ref==True:
        dt=pd.read_csv(local_file_Rpath,sep=',')
        st.dataframe(dt)
    local_file_Wpath=path_geral+'/db/base_gasto.csv'
    st.session_state.exist_custo  = os.path.exists(local_file_Wpath)
    if st.session_state.exist_custo==True:
        dt1=pd.read_csv(local_file_Wpath,sep=',')
        st.dataframe(dt1)
     
     
    
else:
    st.write('Login não realizado!')
