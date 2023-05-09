import streamlit as st
import re
import json

def write_to_json(data,file_name):
    """write a nested dictionary and list into a json file"""
    data_json = json.dumps(data)
    with open(file_name, "w") as outfile:
        outfile.write(data_json)

def read_from_json(file_name):
    """read a json file into a nested dictionary and list"""
    with open(file_name, "r",encoding="UTF-8") as outfile:
        read_data = outfile.read()
    return json.loads(read_data)

def get_list_from_json(json,status,start=None,remove_duplicate=False,branch=None):
    """read the json file into nested dictionary and list, get the field related to language classification
    and proto language. These fields are a list. Collect all these list into a big list and return. If there is
    redundant element in the list, remove them. If there is unnecessary letter or symbol in the text, remove them.
    If there are dialects under one language, for every dialect, create a list and append to the big list. If there is 
    unclear element, make them clear. This big list will be used to build the classification tree."""
    dictionary = read_from_json(json)
    list_2 = []
    if status == "classification":
        for i in dictionary:
            dict_1 = dictionary[i]
            list_1 = []
            if dict_1.get("Language family corrected")!= None:
                list_1 = dict_1.get("Language family corrected")
            if dict_1.get("Linguistic classification corrected")!= None:
                list_1 = dict_1.get("Linguistic classification corrected")
            if dict_1.get("Dialects")!= None:
                for dialect in dict_1.get("Dialects"):
                    if re.findall(r",|·",dialect)!=[]:
                        dialect_list = re.split(r" *, *| *· *",dialect)
                        for dialect_1 in dialect_list:
                            list_2.append(list_1+[dialect_1])
                    else:
                        dialect_1 = re.sub(r" *◇ *| *◆ *|\*","",dialect)
                        list_2.append(list_1+[dialect_1])
            else:
                list_2.append(list_1)
    if status == "proto":
        for i in dictionary:
            dict_1 = dictionary[i]
            if dict_1.get("Early forms corrected")!= None:
                list_4 = dict_1.get("Early forms corrected")
                if dict_1.get("English Name") != None:
                    list_4.append(dict_1.get("English Name"))
                elif dict_1.get("Name") != None:
                    list_4.append(dict_1.get("Name"))
                list_2.append(list_4)
            if dict_1.get("Early form corrected")!= None:
                list_4 = dict_1.get("Early form corrected")
                if dict_1.get("English Name") != None:
                    list_4.append(dict_1.get("English Name"))
                elif dict_1.get("Name") != None:
                    list_4.append(dict_1.get("Name"))
                list_2.append(list_4)
    list_3 = [i for i in list_2 if i != []]
    list_3.sort(key=lambda x: len(x)) 
    list_4 = []
    for i in range(len(list_3)):
        a = 0
        for j in range(i+1,len(list_3)):
            if list_3[i] == list_3[j][:len(list_3[i])]:
                a += 1
        if a == 0:
            list_4.append(list_3[i])
    list_4.sort(key=lambda x: len(x),reverse=True)  
    if re.findall(r"altaic",json,re.I|re.M)!=[]:
        list_10 = []
        for i in list_4:
            i = ["Altaic"]+i
            list_10.append(i)
        list_4 = list_10
    if remove_duplicate!=False:
        list_6 = []
        for i in list_4:
            list_5 = []
            for j in range(len(i)):
                if j == 0:
                    list_5.append(i[j])
                else:
                    if i[j-1] == i[j]:
                        pass
                    else:
                        list_5.append(i[j])
            list_6.append(list_5) 
        list_4 = list_6
    list_7 = []
    for i in list_4:
        list_8 = []
        for j in i:
            if j != "" and j != "?":
                list_8.append(re.sub(r" *\? *| *† *|\(.*\)|(\d)+| *\( *| *\) *","",j))
        list_7.append(list_8)
    if start != None:
        list_9 = []
        for i in list_7:
            try:
                list_9.append(i[i.index(start):])
            except:
                pass
        list_7 = list_9
    list_11 = []
    for i in range(len(list_7)):
        list_12 = []
        for j in range(len(list_7[i])):
            if re.findall(r"^ *eastern *$|^ *western *$|^ *southern *$|^ *northern *$|^ *central *$|^ *northeastern *$|^ *northwestern *$|^ *southeastern *$|^ *southwestern *$|^ *insular *$|^ *canadian *$|^ *Costeño *$|^ *Llanero *$|^ *Mainland *$",list_7[i][j],re.I|re.M)!=[]:
                list_12.append(list_7[i][j]+" "+list_7[i][j-1])
            else:
                list_12.append(list_7[i][j])
        list_11.append(list_12)
    list_7 = list_11
    if branch == "Koreanic":
        list_7 = [ x for x in list_7 if 'Koreanic' in x]
    if branch == "Japonic":
        list_7 = [ x for x in list_7 if 'Japonic' in x]
    if branch == "Turkic":
        list_7 = [ x for x in list_7 if 'Turkic' in x]
    if branch == "Mongolic":
        list_7 = [ x for x in list_7 if 'Mongolic' in x]
    if branch == "Tungusic":
        list_7 = [ x for x in list_7 if 'Tungusic' in x]
    return list_7  

def check(json,status,mode):
    """This function is only used for finding out languages with abnormal data. This function finds
    languages that have repetitive elements in the classification field, and languages with keywords such as 
    "eastern", "western", "southern", "northern" in the classification units, which are unclear messages"""
    dictionary = read_from_json(json)
    list_2 = []
    if status == "classification":
        for i in dictionary:
            dict_1 = dictionary[i]
            list_1 = []
            if dict_1.get("Language family corrected")!= None:
                list_1 = dict_1.get("Language family corrected")
            if dict_1.get("Linguistic classification corrected")!= None:
                list_1 = dict_1.get("Linguistic classification corrected")
            if dict_1.get("Dialects")!= None:
                for dialect in dict_1.get("Dialects"):
                    if re.findall(r",|·",dialect)!=[]:
                        dialect_list = re.split(r" *, *| *· *",dialect)
                        for dialect_1 in dialect_list:
                            list_2.append((list_1+[dialect_1],dict_1["English Name"]))
                    else:
                        dialect_1 = re.sub(r" *◇ *| *◆ *|\*","",dialect)
                        list_2.append((list_1+[dialect_1],dict_1["English Name"]))
            else:
                list_2.append((list_1,dict_1["English Name"]))
    if status == "proto":
        for i in dictionary:
            dict_1 = dictionary[i]
            if dict_1.get("Early forms corrected")!= None:
                list_4 = dict_1.get("Early forms corrected")
                if dict_1.get("English Name") != None:
                    list_4.append(dict_1.get("English Name"))
                elif dict_1.get("Name") != None:
                    list_4.append(dict_1.get("Name"))
                list_2.append((list_4,dict_1["English Name"]))
            if dict_1.get("Early form corrected")!= None:
                list_4 = dict_1.get("Early form corrected")
                if dict_1.get("English Name") != None:
                    list_4.append(dict_1.get("English Name"))
                elif dict_1.get("Name") != None:
                    list_4.append(dict_1.get("Name"))
                list_2.append((list_4,dict_1["English Name"]))
    return_list = []
    for i in range(len(list_2)):
        if mode == "repetitve":
            if len(set(list_2[i][0])) < len(list_2[i][0]):
                if dictionary[list_2[i][1]] not in return_list:
                    return_list.append(dictionary[list_2[i][1]])
        if mode == "direction":
            a = 0
            for j in list_2[i][0]:
                if re.findall(r"^ *eastern *$|^ *western *$|^ *southern *$|^ *northern *$|^ *central *$|^ *northeastern *$|^ *northwestern *$|^ *southeastern *$|^ *southwestern *$|^ *insular *$|^ *canadian *$|^ *Costeño *$|^ *Llanero *$|^ *Mainland *$"\
                              ,j,re.I|re.M)!=[]:
                    a += 1
                if a > 0:
                    if dictionary[list_2[i][1]] not in return_list:
                        return_list.append(dictionary[list_2[i][1]])
    return return_list  

def search_from_json(json,status,term):
    list_2 = get_list_from_json(json,status,remove_duplicate=False)
    lang_list = [i for i in list_2 if i != []]
    lang_list.sort(key=lambda x: len(x)) 
    return_list = []
    for i in lang_list:
        a = 0
        for j in i:
            if re.findall(term,j,re.I)!=[]:
                a += 1
        if a > 0:
            return_list.append(i)
    return return_list

def get_parent_child_pair(json,status,start=None,branch=None):
    list_of_pairs = []
    list_of_list = get_list_from_json(json,status,start,remove_duplicate=True)
    if branch == "Koreanic":
        list_of_list = [ x for x in list_of_list if 'Koreanic' in x]
    if branch == "Japonic":
        list_of_list = [ x for x in list_of_list if 'Japonic' in x]
    if branch == "Turkic":
        list_of_list = [ x for x in list_of_list if 'Turkic' in x]
    if branch == "Mongolic":
        list_of_list = [ x for x in list_of_list if 'Mongolic' in x]
    if branch == "Tungusic":
        list_of_list = [ x for x in list_of_list if 'Tungusic' in x]
    for list_1 in list_of_list:
        for i in range(len(list_1)):
            if i+1!=len(list_1):
                if (list_1[i],list_1[i+1]) not in list_of_pairs:
                    list_of_pairs.append((list_1[i],list_1[i+1])) 
    list_of_pairs.sort(key=lambda x: x[0])        
    return list_of_pairs

def get_length_dict(json):
    lang_list = get_list_from_json(json)
    d = {}
    for k, v in [(len(i),i) for i in lang_list]:
        d.setdefault(k, []).append(v)
    return d

def formTree(json,status):
    tree = {}
    for item in get_list_from_json(json,status,remove_duplicate=True):
        currTree = tree
        for key in item:
            if key not in currTree:
                currTree[key] = {}
            currTree = currTree[key]   
    return tree      

class Language:
    def __init__(self, dictionary):
        self.information = dictionary
        self.proto = {}
        self.classification = {}
        self.proto["parents"] = {}
        self.proto["sole parent"] = []
        self.proto["children"]= {}
        self.proto["depth"] = 0
        self.classification["parents"] = {}
        self.classification["sole parent"] = []
        self.classification["children"] = {}
        self.classification["depth"] = 0
        for i in dictionary:
            if re.findall(r"linguistic classification|language family",i,re.I|re.M) != []:
                if isinstance(dictionary[i],list):
                    self.classification["depth"] = len(dictionary[i])
                else:
                    self.classification["depth"] = 1
            if re.findall(r"early form",i,re.I|re.M) != []:
                if isinstance(dictionary[i],list):
                    self.proto["depth"] = len(dictionary[i])
                else:
                    self.proto["depth"] = 1
 
    def __str__(self):
        return_info = ""
        for i in self.information:
            if re.findall(r"Name|English Name",i,re.I|re.M)!=[] and re.findall(r"Other|Local",i,re.I|re.M)==[]:
                if isinstance(self.information.get(i),list):
                    info = '\033[91m\033[1m'+i+'\033[0m\033[0m'+": "+", ".join(self.information.get(i))+"\n"
                    return_info += info
                else:
                    info = '\033[91m\033[1m'+i+'\033[0m\033[0m'+": "+self.information.get(i)+"\n"
                    return_info += info
            elif re.findall(r"corrected",i,re.I|re.M)!=[]:
                pass
            elif re.findall(r"early form",i,re.I|re.M)!=[]:
                info = '\033[1m'+i+'\033[0m'+": "+" ——> ".join(self.information.get(i)+[self.information.get("English Name")\
                                                         or self.information.get("Name")])+"\n"
                return_info += info
            elif re.findall(r"linguistic classification|proto.*language|language family",i,re.I|re.M) != []:
                info = '\033[1m'+i+'\033[0m'+": "+" ——> ".join(self.information.get(i))+"\n"
                return_info += info
            elif isinstance(self.information.get(i),list):
                info = '\033[1m'+i+'\033[0m'+": "+", ".join(self.information.get(i))+"\n"
                return_info += info
            elif isinstance(self.information.get(i),dict):
                string = "\n".join([key+": "+", ".join(self.information.get(i)[key]) for key in self.information.get(i)])
                info = '\033[1m'+i+'\033[0m'+": "+string+"\n"
                return_info += info
            else:
                info = '\033[1m'+i+'\033[0m'+": "+self.information.get(i)+"\n"
                return_info += info
        #return_info += "\033[1mProto-Language Parents\033[0m: "+str(self.proto["parents"])+"\n"
        return_info += "\033[1mProto-Language Parent\033[0m: "+", ".join(self.proto["sole parent"])+"\n"
        #return_info += "\033[1mProto-Language Lineage\033[0m: "\
        #               +str(self.information.get("Early form corrected"))+"\n"
        #return_info += "\033[1mProto-Language Lineage\033[0m: "\
        #               +str(self.information.get("Early forms corrected"))+"\n"
        #return_info += "\033[1mProto-Language Lineage\033[0m: "\
        #               +str(self.information.get("Reconstructed ancestors"))+"\n"
        return_info += "\033[1mProto-Language Children\033[0m: "+", ".join(self.proto["children"])+"\n"
        # return_info += "\033[1mProto-Language Depth\033[0m: "+str(self.proto["depth"])+"\n"
        #return_info += "\033[1mLanguage Classification Parents\033[0m: "+str(self.classification["parents"])+"\n"
        return_info += "\033[1mLanguage Classification Parent\033[0m: "\
                       +", ".join(self.classification["sole parent"])+"\n"
        #return_info += "\033[1mLanguage Classification Lineage\033[0m: "\
        #               +str(self.information.get("Language family corrected"))+"\n"
        #return_info += "\033[1mLanguage Classification Lineage\033[0m: "\
        #               +str(self.information.get("Linguistic classification corrected"))+"\n"
        return_info += "\033[1mLanguage Classification Children\033[0m: "\
                       +", ".join(list(self.classification["children"].keys()))+"\n"  
        # return_info += "\033[1mLanguage Classification Depth\033[0m: "+str(self.classification["depth"])+"\n"
        return return_info

    def get_html_text(self):
        return_info = ""
        for i in self.information:
            if self.information.get(i) == [] or re.findall(r"corrected|^URL$",i,re.I|re.M)!=[]:
                pass
            elif self.information.get(i) == "Normal":
                pass
            else:
                if re.findall(r"Name|English Name",i,re.I|re.M)!=[] and re.findall(r"Other|Local",i,re.I|re.M)==[]:
                    if isinstance(self.information.get(i),list):
                        info = '<p><b style="color:#FF0000;">'+i+'</b>'+": "+f"<a href={self.information.get('URL')}>"+", ".join(self.information.get(i))+"123</a></p>"
                    else:
                        info = '<p><b style="color:#FF0000;">'+i+'</b>'+": "+f"<a href={self.information.get('URL')}>"+self.information.get(i)+"</a></p>"
                    return_info += info
                elif re.findall(r"early form",i,re.I|re.M)!=[]:
                    info = '<p><b>'+i+'</b>'+": "+" &DoubleLongRightArrow; ".join(self.information.get(i)+[self.information.get("English Name")\
                                                            or self.information.get("Name")])+"</p>"
                    return_info += info
                elif re.findall(r"linguistic classification|proto.*language|language family",i,re.I|re.M) != []:
                    info = '<p><b>'+i+'</b>'+": "+" &DoubleLongRightArrow; ".join(self.information.get(i))+"</p>"
                    return_info += info
                elif isinstance(self.information.get(i),list):
                    if re.findall(r"Related URLs",i,re.I|re.M)!=[]:
                        links = self.information.get(i)
                        names = [re.sub(".*/","",k).replace("_"," ") for k in self.information.get(i)]
                        a_tag_list = [f"<a href={link}>{name}</a>" for link, name in zip(links, names)]
                        info = '<p><b>Links</b>'+": "+", ".join(a_tag_list)+"</p>"
                    elif re.findall(r"other names",i,re.I|re.M)!=[]:
                        info = '<p><b>Native Names</b>'+": "+", ".join(self.information.get(i))+"</p>"
                    else:
                        info = '<p><b>'+i+'</b>'+": "+", ".join(self.information.get(i))+"</p>"
                    return_info += info
                elif isinstance(self.information.get(i),dict):
                    string = "\n".join([key+": "+", ".join(self.information.get(i)[key]) for key in self.information.get(i)])
                    info = '<p><b>'+i+'</b>'+": "+string+"</p>"
                    return_info += info
                else:
                    info = '<p><b>'+i+'</b>'+": "+self.information.get(i)+"</p>"
                    return_info += info
        return_info += ("<p><b>Proto-Language Parent</b>: "+", ".join(self.proto["sole parent"])+"</p>" if self.proto["sole parent"] != [] and self.proto["sole parent"] != {} else "")
        return_info += ("<p><b>Proto-Language Children</b>: "+", ".join(self.proto["children"])+"</p>" if self.proto["children"] != [] and self.proto["children"] != {} else "")
        return_info += ("<p><b>Language Classification Parent</b>: "\
                    +", ".join(self.classification["sole parent"])+"</p>" if self.classification["sole parent"] != [] and self.classification["sole parent"] != {} else "")
        return_info += ("<p><b>Language Classification Children</b>: "\
                    +", ".join(list(self.classification["children"].keys()))+"</p>" if self.classification["children"] != [] and self.classification["children"] != {} else "")
        return return_info



    def get_all_attributes(self):
        return self.__dict__

class Tree:
    def __init__(self):
        self.langList = {}
        self.numLangs = 0

    def addLang(self,dictionary):
        self.numLangs = self.numLangs + 1
        newLang = Language(dictionary)
        if dictionary.get("English Name") != None:
            self.langList[re.sub(r"\[\d+\]","",dictionary.get("English Name"))] = newLang
        elif dictionary.get("Name") != None: 
            self.langList[re.sub(r"\[\d+\]","",dictionary.get("Name"))] = newLang
        return newLang

    def getLang(self,name):
        if name in self.langList:
            return self.langList[name]
        else:
            return None

    def searchLang(self,name):
        lang_list = []
        for lang in self.langList:
            if re.findall(name,lang,re.I|re.M) != []:
                lang_list.append(lang)
        for i in lang_list:
            print(self.langList[i],"\n")  
        
    def __contains__(self,name):
        return name in self.langList
    
    def getLangs(self):
        return self.langList.keys()
    
    def __iter__(self):
        return iter(self.langList.values())
    
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res        

@st.cache_data
def create_tree(json,start=None): 
    dictionary = read_from_json(json)
    lang_list = []
    if start != None:
        for i in get_parent_child_pair(json,status="classification",start=start):
            for j in i:
                if j not in lang_list:
                    lang_list.append(j)
    else:
        lang_list = dictionary.keys()
    lang_tree = Tree()
    for i in lang_list:
        try:
            new_lang = lang_tree.addLang(dictionary[i])
        except:
            pass
    for pair in get_parent_child_pair(json,status="classification",start=start):
        if pair[0] in lang_tree.langList.keys() and pair[1] in lang_tree.langList.keys():
            if pair[1] not in lang_tree.langList[pair[0]].classification["children"]:
                lang_tree.langList[pair[0]].classification["children"][pair[1]] = 1
            else:
                lang_tree.langList[pair[0]].classification["children"][pair[1]] += 1
            if pair[0] not in lang_tree.langList[pair[1]].classification["parents"]:
                lang_tree.langList[pair[1]].classification["parents"][pair[0]] = 1
            else:
                lang_tree.langList[pair[1]].classification["parents"][pair[0]] += 1
    for pair in get_parent_child_pair(json,status="proto",start=start):
        if pair[0] in lang_tree.langList.keys() and pair[1] in lang_tree.langList.keys():
            if pair[1] not in lang_tree.langList[pair[0]].proto["children"]:
                lang_tree.langList[pair[0]].proto["children"][pair[1]] = 1
            else:
                lang_tree.langList[pair[0]].proto["children"][pair[1]] += 1
            if pair[0] not in lang_tree.langList[pair[1]].proto["parents"]:
                lang_tree.langList[pair[1]].proto["parents"][pair[0]] = 1
            else:
                lang_tree.langList[pair[1]].proto["parents"][pair[0]] += 1
    for lang in lang_tree.langList:
        class_parents = lang_tree.langList[lang].classification["parents"]
        class_parents_list = []
        if class_parents != {}:
            prepared_list_1 = []
            if len(class_parents) == 1:
                lang_tree.langList[lang].classification["sole parent"] += list(class_parents.keys())
            else:
                for class_parent in class_parents:
                    class_parent_children = list(lang_tree.langList[class_parent].classification["children"].keys())
                    other_class_parents = list(class_parents.keys())
                    n = 0
                    for other_class_parent in other_class_parents:
                        if other_class_parent in class_parent_children:
                            n += 1
                    if n == 0:
                        if class_parent not in prepared_list_1:
                            prepared_list_1 += [class_parent]  
            prepared_list_1 = [*set(prepared_list_1)]
            if len(prepared_list_1)<=1: 
                lang_tree.langList[lang].classification["sole parent"] += prepared_list_1
            else:
                if lang_tree.langList[lang].information.get("Language family corrected"):
                    if len(lang_tree.langList[lang].information.get("Language family corrected")) > 1:
                        for i in prepared_list_1:
                            if i == lang_tree.langList[lang].information.get("Language family corrected")[-2]:
                                if i not in lang_tree.langList[lang].classification["sole parent"]:
                                    lang_tree.langList[lang].classification["sole parent"].append(i)
                if lang_tree.langList[lang].information.get("Linguistic classification corrected"):
                    if len(lang_tree.langList[lang].information.get("Linguistic classification corrected")) > 1:
                        for i in prepared_list_1:
                            if i == lang_tree.langList[lang].information.get("Linguistic classification corrected")[-2]:
                                if i not in lang_tree.langList[lang].classification["sole parent"]:
                                    lang_tree.langList[lang].classification["sole parent"].append(i)
    for lang in lang_tree.langList:
        class_parents = lang_tree.langList[lang].proto["parents"]
        class_parents_list = []
        if class_parents != {}:
            prepared_list_2 = []
            if len(class_parents) == 1:
                lang_tree.langList[lang].proto["sole parent"] += list(class_parents.keys())
            else:
                for class_parent in class_parents:
                    class_parent_children = list(lang_tree.langList[class_parent].proto["children"].keys())
                    other_class_parents = list(class_parents.keys())
                    n = 0
                    for other_class_parent in other_class_parents:
                        if other_class_parent in class_parent_children:
                            n += 1
                    if n == 0:
                        if class_parent not in prepared_list_2:
                            prepared_list_2 += [class_parent]  
            prepared_list_2 = [*set(prepared_list_2)]
            if len(prepared_list_2)<=1:
                lang_tree.langList[lang].proto["sole parent"] += prepared_list_2
            else:
                if lang_tree.langList[lang].information.get("Early forms corrected"):
                    if len(lang_tree.langList[lang].information.get("Early forms corrected")) > 0:
                        for i in prepared_list_2:
                            if i == lang_tree.langList[lang].information.get("Early forms corrected")[-1]:
                                if i not in lang_tree.langList[lang].proto["sole parent"]:
                                    lang_tree.langList[lang].proto["sole parent"].append(i)
                if lang_tree.langList[lang].information.get("Early form corrected"):
                    if len(lang_tree.langList[lang].information.get("Early form corrected")) > 0:
                        for i in prepared_list_2:
                            if i == lang_tree.langList[lang].information.get("Early form corrected")[-1]:
                                if i not in lang_tree.langList[lang].proto["sole parent"]:
                                    lang_tree.langList[lang].proto["sole parent"].append(i) 
                if lang_tree.langList[lang].information.get("Reconstructed ancestors"):
                    if len(lang_tree.langList[lang].information.get("Reconstructed ancestors")) > 0:
                        for i in prepared_list_2:
                            if i == lang_tree.langList[lang].information.get("Reconstructed ancestors")[-1]:
                                if i not in lang_tree.langList[lang].proto["sole parent"]:
                                    lang_tree.langList[lang].proto["sole parent"].append(i) 
    for lang in lang_tree.langList:
        if (len(lang_tree.langList[lang].classification["sole parent"])==0 and \
            len(lang_tree.langList[lang].classification["parents"])!=0):
            if lang_tree.langList[lang].information.get("Language family corrected"):
                if len(lang_tree.langList[lang].information.get("Language family corrected")) > 1:  
                    lang_tree.langList[lang].classification["sole parent"] +=\
                    [lang_tree.langList[lang].information.get("Language family corrected")[-2]]
            if lang_tree.langList[lang].information.get("Linguistic classification corrected"):
                if len(lang_tree.langList[lang].information.get("Linguistic classification corrected")) > 1:  
                    lang_tree.langList[lang].classification["sole parent"] +=\
                    [lang_tree.langList[lang].information.get("Linguistic classification corrected")[-2]]
        if (len(lang_tree.langList[lang].proto["sole parent"])==0 and \
            len(lang_tree.langList[lang].proto["parents"])!=0):    
            if lang_tree.langList[lang].information.get("Early forms corrected"):
                if len(lang_tree.langList[lang].information.get("Early forms corrected")) > 0:  
                    lang_tree.langList[lang].proto["sole parent"].\
                    append(lang_tree.langList[lang].information.get("Early forms corrected")[-1])
            if lang_tree.langList[lang].information.get("Early form corrected"):
                if len(lang_tree.langList[lang].information.get("Early form corrected")) > 0:  
                    lang_tree.langList[lang].proto["sole parent"].\
                    append(lang_tree.langList[lang].information.get("Early form corrected")[-1])
            if lang_tree.langList[lang].information.get("Reconstructed ancestors"):
                if len(lang_tree.langList[lang].information.get("Reconstructed ancestors")) > 0:  
                    lang_tree.langList[lang].proto["sole parent"].\
                    append(lang_tree.langList[lang].information.get("Reconstructed ancestors")[-1])
    return lang_tree       

class Simplified_Language:
    def __init__(self,name):
        self.name = name
        self.parents = {}
        self.parent = []
        self.children = {}
        self.real_children = []
    
    def __str__(self):
        string = "\n".join(("\033[91m\033[1mLanguage Name\033[0m\033[0m: "+self.name,\
                            "\033[1mParent\033[0m: "+", ".join(self.parent),\
                            "\033[1mParents\033[0m: "+str(self.parents),\
                            "\033[1mChildren\033[0m: "+", ".join(self.real_children)))
        return string
    
    def get_html_text(self,child=None):
        if child == None:
            string = "".join(("<p><b style='color:#FF0000;'>Language Name</b>: <b>"+self.name+"</b></p>",\
                                "<p><b>Parent</b>: "+"<b style='color:Brown;'>"+", ".join(self.parent)+"</b></p>",\
                                "<p><b>Children</b>: "+", ".join(self.real_children)+"</p>"))
        else:
            string_1 = "<p><b>Children</b>: "+", ".join(["<b style='color:Brown;'>"+i+"</b>" if i == child else i for i in self.real_children])+"</p>"
            string = "".join(("<p><b style='color:#FF0000;'>Language Name</b>: <b>"+self.name+"</b></p>",\
                                "<p><b>Parent</b>: "+"<b style='color:Brown;'>"+", ".join(self.parent)+"</b></p>",\
                                string_1))
        return string
        
class Simplified_Tree():
    def __init__(self):
        self.langList = {}
        self.numLangs = 0
    def addLang(self,name):
        self.numLangs = self.numLangs + 1
        newLang = Simplified_Language(name)
        self.langList[name] = newLang
        return newLang
    def searchLang(self,name):
        list_1 = []
        for lang in self.langList:
            if re.findall(name,lang,re.I|re.M) != []:
                list_1.append(lang)
        for i in list_1:
            print(self.langList[i],"\n")

@st.cache_data
def creat_simple_tree(json,status,start=None,branch=None):
    longTree = create_tree(json,start=start)
    list_of_pair = get_parent_child_pair(json,status,start=start,branch=branch)
    lang_tree = Simplified_Tree()
    for pair in list_of_pair:
        if pair[0] not in lang_tree.langList:
            lang_tree.addLang(pair[0])
            lang_tree.langList[pair[0]].children[pair[1]] = 1
        else:
            if pair[1] not in lang_tree.langList[pair[0]].children:
                lang_tree.langList[pair[0]].children[pair[1]] = 1
            else:
                lang_tree.langList[pair[0]].children[pair[1]] += 1
        if pair[1] not in lang_tree.langList:
            lang_tree.addLang(pair[1])
            lang_tree.langList[pair[1]].parents[pair[0]] = 1
        else:
            if pair[0] not in lang_tree.langList[pair[1]].parents:
                lang_tree.langList[pair[1]].parents[pair[0]] = 1
            else:
                lang_tree.langList[pair[1]].parents[pair[0]] += 1
    for lang in lang_tree.langList:
        parents = lang_tree.langList[lang].parents
        if len(parents) <= 1:
            lang_tree.langList[lang].parent += parents
        else:
            for parent in parents:
                parent_children = list(lang_tree.langList[parent].children.keys())
                other_parents = list(parents.keys())
                n = 0
                for other_parent in other_parents:
                    if other_parent in parent_children:
                        n += 1
                if n == 0:
                    lang_tree.langList[lang].parent += [parent]
    for lang in lang_tree.langList:
        if len(lang_tree.langList[lang].parent) > 1:
            if lang in longTree.langList:
                if status == "classification":
                    lang_tree.langList[lang].parent = longTree.langList[lang].classification["sole parent"]
                if status == "proto":
                    lang_tree.langList[lang].parent = longTree.langList[lang].proto["sole parent"]
    for lang in lang_tree.langList:
        if len(lang_tree.langList[lang].parent) > 1:
            lang_tree.langList[lang].parent = [lang_tree.langList[lang].parent[0]]
    for lang in lang_tree.langList:
        children = lang_tree.langList[lang].children
        for child in children:
            child_parent = list(lang_tree.langList[child].parents.keys())
            child_parent_parent = []
            for x in list(lang_tree.langList[child].parents.keys()):
                child_parent_parent += list(lang_tree.langList[x].parents.keys())
            other_children = list(children.keys())
            n = 0
            for other_child in other_children:
                if other_child in child_parent or other_child in child_parent_parent:
                    n += 1
            if n == 0:
                lang_tree.langList[lang].real_children += [child]
    for lang in lang_tree.langList:
        if len(lang_tree.langList[lang].parent)==0 and len(lang_tree.langList[lang].parents)>0:
            lang_tree.langList[lang].parent = [list(lang_tree.langList[lang].parents.keys())[0]]
    return lang_tree

def find_lineage(simple_tree,tree,name,form="long"):
    list_1 = [name]
    start = simple_tree.langList[name]
    i = 20
    while i > 0:
        i -= 1
        try:
            list_1.append(", ".join(start.parent))
        except:
            pass
        try:
            start = simple_tree.langList[", ".join(start.parent)]
        except:
            pass
    list_1.reverse()
    list_1 = [x for x in list_1 if x != ""]
    return_text = ""
    if form=="long":
        for i, lang in enumerate(list_1):
            if lang in tree.langList:
                return_text += "<br>"+tree.langList[lang].get_html_text()+"<br>"
            else:
                if i < len(list_1):
                    try:
                        return_text += "<br>"+simple_tree.langList[lang].get_html_text(list_1[i+1])+"<br>"
                    except:
                        pass
                else:
                    return_text += "<br>"+simple_tree.langList[lang].get_html_text()+"<br>"
    if form=="short":
        for i, lang in enumerate(list_1):
            if i < len(list_1):
                    try:
                        return_text += "<br>"+simple_tree.langList[lang].get_html_text(list_1[i+1])+"<br>"
                    except:
                        pass
            else:
                return_text += "<br>"+simple_tree.langList[lang].get_html_text()+"<br>"
    return return_text

def find_no_parent(tree):
    list_1 = []
    for lang in tree.langList:
        if len(tree.langList[lang].parent) == 0:
            list_1.append(lang)
            print(tree.langList[lang])
    return "There are "+str(len(list_1))+" language with no parent."  

def show_simple_tree(simplelangTree,status,json):
    from treelib import Node, Tree
    from collections import Counter
    tree = Tree()
    added_list = []
    unadded_list = []
    root = None
    if status == "classification":
        for lang in simplelangTree.langList:
            if simplelangTree.langList[lang].parent == []:
                root = lang
                # print("Show the linguistic tree of "+root+" languages......")
    elif status == "proto":
        for lang in simplelangTree.langList:
            if simplelangTree.langList[lang].parent == [] and re.findall(json.split(" ")[0],lang,re.M|re.I)!=[]:
                root = lang
                # print("Show the linguistic tree of "+root+" languages......")
    tree.create_node(root, root)
    added_list.append(root)
    unadded_num_list = []
    while (len(simplelangTree.langList)-len(added_list)) > 0:
        if len(unadded_num_list) > 6 and len(set(unadded_num_list[-5:])) == 1:
            break
        else:
            for lang in simplelangTree.langList:
                if lang not in [tree.nodes[k].tag for k in tree.nodes] and lang not in added_list:
                    try:
                        tree.create_node(lang, lang, parent=simplelangTree.langList[lang].parent[0])
                        added_list.append(lang)
                    except:
                        unadded_list.append(lang)
        unadded_num_list.append(len(simplelangTree.langList)-len(added_list))
    return tree
