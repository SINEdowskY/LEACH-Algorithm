import streamlit as st
from environment import Environment
st.set_option('deprecation.showPyplotGlobalUse', False)

amount_nodes = st.sidebar.slider("Amount of nodes", min_value=50, max_value=100)

env = Environment(nodes_amount=amount_nodes)

st.pyplot(env.draw_graph())
