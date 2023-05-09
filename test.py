
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from complextree import *

st.set_option('deprecation.showPyplotGlobalUse', False)
graph = lang_graph("new_language_distance_data_1-78.json","lang_list.json",0.2)

# Display the plot in Streamlit
st.pyplot(graph)

