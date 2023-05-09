import streamlit as st
from simpletree import *
from streamlit.components.v1 import html
from descriptions import new_description_dict
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep
import streamlit as st
from treelib import Node, Tree
import sys
import re
from complextree import lang_dendrogram, lang_graph

st.title("Visualize Linguistic Phylogenetics")

tab1, tab2, tab3 = st.tabs(["5 Language Families", "Linguistic Similarity","Data Source"])

tab1.subheader("Explore 5 Major Language Families in the World")
tab1.data_dict = {"Indo-European":"Indo-European language data.json",
             "Sino-Tibetan":"Sino-Tibetan language data.json",
             "Altaic":"Altaic language data.json", 
             "Afroasiatic":"Afroasiatic language data.json",
             "Uralic":"Uralic language data.json"}

tab1.description_dict = new_description_dict

with tab1:
    tab1.select_lang_family = st.selectbox(
    "Choose a language family to explore:",
    tab1.data_dict.keys()
    )
    with st.expander(f"Description of {tab1.select_lang_family} languages"):
        st.write(tab1.description_dict[tab1.select_lang_family], unsafe_allow_html=True)
    if tab1.select_lang_family == "Indo-European":
        tab4, tab5, tab6 = st.tabs(["Indo-European", "European","Indo-Iranian"])
        with tab4:
            st.image("pictures/Indo-European.png", caption="Map of Indo-European Languages")
        with tab5:
            st.image("pictures/European.png", caption="Map of Languages in Europe")
        with tab6:
            st.image("pictures/Indo-Iranian.png", caption="Map of Indo-Iranian Languages")
    elif tab1.select_lang_family == "Sino-Tibetan":
        tab4, tab5 = st.tabs(["Sino-Tibetan","Chinese"])
        with tab4:
            st.image("pictures/Sino-Tibetan.png", caption="Map of Sino-Tibetan Languages")
        with tab5:
            st.image("pictures/Chinese.png", caption="Map of Languages in China")
    elif tab1.select_lang_family == "Altaic":
        tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(["Altaic", "Altaic, Uralic", "Turkic", "Mongolic", "Tungusic", "Japonic","Koreanic","Central Asia"])
        with tab4:
            st.image("pictures/Altaic.png", caption="Map of Altaic Languages")
        with tab5:
            st.image("pictures/Altaic_Uralic.png", caption="Map of Altaic and Uralic Languages")
        with tab6:
            st.image("pictures/Turkic.png", caption="Map of Turkic Languages")
        with tab7:
            st.image("pictures/Mongolic.png", caption="Map of Mongolic Languages")
        with tab8:
            st.image("pictures/Tungusic.png", caption="Map of Tungusic Languages")
        with tab9:
            st.image("pictures/Japonic.png", caption="Map of Japonic Languages")
        with tab10:
            st.image("pictures/Koreanic.png", caption="Map of Koreanic Languages")
        with tab11:
            st.image("pictures/Central Asia.png", caption="Map of Languages in Central Asia")
    elif tab1.select_lang_family == "Afroasiatic":
        tab4, tab5 = st.tabs(["Afroasiatic", "Arabic"])
        with tab4:
            st.image("pictures/Afroasiatic.png", caption="Map of Afroasiatic Languages")
        with tab5:
            st.image("pictures/Arabic.png", caption="Map of Arabic Languages")
    elif tab1.select_lang_family == "Uralic":
        tab4, tab5 = st.tabs(["Uralic", "Altaic, Uralic"])
        with tab4:
            st.image("pictures/Uralic.png", caption="Map of Uralic Languages")
        with tab5:
            st.image("pictures/Altaic_Uralic.png", caption="Map of Altaic and Uralic Languages")

    tab1.langTree = create_tree(tab1.data_dict[tab1.select_lang_family],start=None)
    tab1.lang_selected = tab1.selectbox(
        "Search for a language in this family:",
        tab1.langTree.langList.keys()
    )
    html_text_1 = tab1.langTree.langList[tab1.lang_selected].get_html_text()
    st.write(html_text_1, unsafe_allow_html=True)
    if re.match(".*\u2020.*",html_text_1) != None:
        st.write("<p>\u2020 indicates the language is extinct.</p>", unsafe_allow_html=True)
    if re.match(".*\(\?\).*",html_text_1) != None:
        st.write("<p>(?) indicates the existence of the language is questionable.</p>", unsafe_allow_html=True)

    st.write("<p></p><p></p><h5>Show Linguistic Tree</h5>", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1])
    tree_type_dict = {"Linguistic Classification Tree":"classification", "Proto Language Tree":"proto"}
    with col1:
        col1.tree_type = col1.selectbox(
            "Choose tree type: ",
            ["Linguistic Classification Tree", "Proto Language Tree"],
            key = 1
        )
    with col2:
        col2.start_point = col2.selectbox(
            "Choose the root of the tree: ",
            ["(None)"]+list(tab1.langTree.langList.keys())
        )
    if col2.start_point == "(None)":
        pass
    else:
        simple_tree = creat_simple_tree(tab1.data_dict[tab1.select_lang_family],status=tree_type_dict[col1.tree_type],start=col2.start_point)
        tree_to_be_shown = show_simple_tree(simple_tree,status=tree_type_dict[col1.tree_type],json=tab1.data_dict[tab1.select_lang_family])
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    if col2.start_point == "(None)":
        pass
    else:
        tree_to_be_shown.show()
    console_output = mystdout.getvalue()
    sys.stdout = old_stdout
    if col2.start_point == "(None)":
        pass
    else:
        with st.expander(f"Show the {tree_type_dict[col1.tree_type]} of {col2.start_point} Languages"):
            if re.search(r"(\d)+",console_output) is not None:
                st.write("```\n" + "The chosen root is a leaf in the language tree. There is no tree.")
            else:
                st.write("```\n" + console_output + "```")
    st.write("<p></p><p></p><h5>Show the Lineage of Languages</h5>", unsafe_allow_html=True)
    col3, col4, col5 = st.columns([3,3,1])
    tree_type_dict = {"Linguistic Classification Tree":"classification", "Proto Language Tree":"proto"}
    with col3:
        col3.start_point = col3.selectbox(
            "Choose the Language: ",
            ["(None)"]+list(tab1.langTree.langList.keys())
        )
    with col4:
        col4.tree_type = col4.selectbox(
            "Choose tree type: ",
            ["Linguistic Classification Tree", "Proto Language Tree"],
            key = 2
        )
    with col5:
        col5.start_point = col5.selectbox(
            "Form: ",
            ["Brief", "Detailed"]
        )
    format_dict = {"Brief":"short", "Detailed":"long"}
    if col3.start_point == "(None)":
        pass
    else:

        with st.expander(f"Show the Lineage of {col3.start_point} in {col4.tree_type} in {col5.start_point} Format"):
            simple_tree = creat_simple_tree(tab1.data_dict[tab1.select_lang_family],status=tree_type_dict[col4.tree_type],start=None)
            returned_html_text = find_lineage(simple_tree,tab1.langTree,col3.start_point,form=format_dict[col5.start_point])
            st.write(returned_html_text, unsafe_allow_html=True)

with tab2:
    tab2.subheader("Draw dendrogram based on language similarity")
    col1, col2, col3 = st.columns([3,3,2])
    with col1:
        col1.dendrogram_lang_family = col1.selectbox(
            "Choose the Language Family: ",
            ["All"]+list(tab1.data_dict.keys())
        )
    with col2:
        col2.start_list = col2.multiselect(
            "Choose start of the tree: ",
            list(tab1.langTree.langList.keys()),
        )
    with col3:
        col3.orientation = col3.selectbox(
            "Orientation: ",
            ["Vertical","Horizontal"],
        )
    tab2.submit_button_1 = tab2.button(label="Submit", key=3)
    if col3.orientation == "Vertical":
        orientation = "left"
    else:
        orientation = "right"
    if tab2.submit_button_1:
        if col1.dendrogram_lang_family == "All":
            dendrogram = lang_dendrogram("new_language_distance_data_total.json","lang_list.json",orientation=orientation)
        else:
            if col2.start_list == []:
                dendrogram = lang_dendrogram("new_language_distance_data_total.json","lang_list.json",\
                        json=tab1.data_dict[col1.dendrogram_lang_family],start=None,orientation=orientation)
            else:
                dendrogram = lang_dendrogram("new_language_distance_data_total.json","lang_list.json",\
                            json=tab1.data_dict[col1.dendrogram_lang_family],start=col2.start_list,orientation=orientation)
        st.pyplot(dendrogram)
    tab2.subheader("Draw language cluster graph")
    col4, col5 = st.columns([1,1])
    with col4:
        col4.threshold = st.slider('Select a similarity threshold', 0.0, 1.0, step=0.01)
    with col5:
        col5.submit_button = col5.button(label="Submit", key=4)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    if col5.submit_button:
        graph = lang_graph("new_language_distance_data_1-78.json","lang_list.json",col4.threshold)
        st.pyplot(graph)

with tab3:
    text_1 = """
    <p>
    This project is cerated by Yifei Sun as the final project for SI 507 Intermediate Programming at the University of Michigan.
    </p>
    <p><a href="https://github.com/YifeiSun01/Linguistic_phylogenetics/tree/main">Github link</a></p>
    <p><b>Data Source:</b></p>
    <p><a href="http://www.elinguistics.net/Compare_Languages.aspx">eLinguistics.net</a></p>
    <p><a href="https://www.wikipedia.org/">Wikipedia</a></p>
    
    """
    st.markdown(text_1, unsafe_allow_html=True)


