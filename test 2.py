
from complextree import *

"""
dendrogram = lang_dendrogram("new_language_distance_data_total.json","lang_list.json",\
                    json="Indo-European language data.json",start=["Germanic","Slavic","Romance","Baltic","Celtic"])

dendrogram.show()
"""


import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Generate some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a plot
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('A simple plot')

# Display the plot in Streamlit
st.pyplot(fig)