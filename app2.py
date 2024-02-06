import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pickle

path_geral='/opt/render/project/src'

with open(path_geral+'/credentials/config1.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)



authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login()

with open(path_geral+"/x.pkl", "wb") as f:
    pickle.dump(st.session_state["authentication_status"], f)


if st.session_state["authentication_status"]:
    authenticator.logout(location='sidebar')
    st.write(f'Seja Bem Vindo *{st.session_state["name"]}*')
    st.title("Relatório Geral")
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


