def write_to_json(data,file_name):
    """write a nested dictionary and list into a json file"""
    import json
    data_json = json.dumps(data)
    with open(file_name, "w") as outfile:
        outfile.write(data_json)

def read_from_json(file_name):
    """read a json file into a nested dictionary and list"""
    import json
    with open(file_name, "r",encoding="UTF-8") as outfile:
        read_data = outfile.read()
    return json.loads(read_data)

def get_list_from_json(json,status,start=None,remove_duplicate=False,branch=None):
    """read the json file into nested dictionary and list, get the field related to language classification
    and proto language. These fields are a list. Collect all these list into a big list and return. If there is
    redundant element in the list, remove them. If there is unnecessary letter or symbol in the text, remove them.
    If there are dialects under one language, for every dialect, create a list and append to the big list. If there is 
    unclear element, make them clear. This big list will be used to build the classification tree."""
    import re
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
                elif ddict_1.get("Name") != None:
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
    import re
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

import re
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
        return_info += "\033[1mProto-Language Depth\033[0m: "+str(self.proto["depth"])+"\n"
        #return_info += "\033[1mLanguage Classification Parents\033[0m: "+str(self.classification["parents"])+"\n"
        return_info += "\033[1mLanguage Classification Parent\033[0m: "\
                       +", ".join(self.classification["sole parent"])+"\n"
        #return_info += "\033[1mLanguage Classification Lineage\033[0m: "\
        #               +str(self.information.get("Language family corrected"))+"\n"
        #return_info += "\033[1mLanguage Classification Lineage\033[0m: "\
        #               +str(self.information.get("Linguistic classification corrected"))+"\n"
        return_info += "\033[1mLanguage Classification Children\033[0m: "\
                       +", ".join(list(self.classification["children"].keys()))+"\n"  
        return_info += "\033[1mLanguage Classification Depth\033[0m: "+str(self.classification["depth"])+"\n"
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

import re
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

def find_lineage(json,name,status,form="long"):
    simple_tree = creat_simple_tree(json,status=status,start=None,branch=None)
    tree = create_tree(json,start=None)
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
    if form=="long":
        for lang in list_1:
            if lang in tree.langList:
                print(tree.langList[lang],"\n") 
            else: 
                print(simple_tree.langList[lang],"\n") 
    if form=="short":
        for lang in list_1:
            print(simple_tree.langList[lang],"\n") 

def find_no_parent(tree):
    list_1 = []
    for lang in tree.langList:
        if len(tree.langList[lang].parent) == 0:
            list_1.append(lang)
            print(tree.langList[lang])
    return "There are "+str(len(list_1))+" language with no parent."  

def show_simple_tree(json,status,start=None,branch=None):
    from treelib import Node, Tree
    from collections import Counter
    import re
    simplelangTree = creat_simple_tree(json,status,start,branch=branch)
    tree = Tree()
    added_list = []
    unadded_list = []
    root = None
    if status == "classification":
        for lang in simplelangTree.langList:
            if simplelangTree.langList[lang].parent == []:
                root = lang
                print("Show the linguistic tree of "+root+" languages......")
    elif status == "proto":
        for lang in simplelangTree.langList:
            if simplelangTree.langList[lang].parent == [] and re.findall(json.split(" ")[0],lang,re.M|re.I)!=[]:
                root = lang
                print("Show the linguistic tree of "+root+" languages......")
    tree.create_node(root, root)
    added_list.append(root)
    unadded_num_list = []
    n = 6
    while (len(simplelangTree.langList)-len(added_list)) > 0: 
        if len(unadded_num_list) > n and len(set(unadded_num_list[(-1)*n:])) == 1:
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
        print(str(len(simplelangTree.langList)-len(added_list))+" languages haven't been added.")
    final_unadded = \
    ", ".join(list(set(simplelangTree.langList.keys())-set([tree.nodes[k].tag for k in tree.nodes])))
    print("These languages are not added: "+final_unadded+"\n\n")
    tree.show() 

def show_complex_tree(json,status,start=None,branch=None):
    import networkx as nx
    from networkx.algorithms import community
    import re
    import matplotlib.pyplot as plt
    import pydot
    from networkx.drawing.nx_pydot import graphviz_layout
    import itertools
    simplelangTree = creat_simple_tree(json,status,start,branch=branch)
    G = nx.Graph()
    added_list = []
    unadded_list = []
    root = None
    if status == "classification":
        for lang in simplelangTree.langList:
            if simplelangTree.langList[lang].parent == []:
                root = lang
                print("root: ",root)
                print("Show the linguistic tree of "+root+" languages......")
    elif status == "proto":
        for lang in simplelangTree.langList:
            if simplelangTree.langList[lang].parent == [] and re.findall(json.split(" ")[0],lang,re.M|re.I)!=[]:
                root = lang
                print("Show the linguistic tree of "+root+" languages......")
    G.add_node(root)
    added_list.append(root)
    unadded_num_list = []
    n = 8
    while (len(simplelangTree.langList)-len(added_list)) > 0: 
        if len(unadded_num_list) > n and len(set(unadded_num_list[(-1)*n:])) == 1:
            break
        else:
            for lang in simplelangTree.langList:
                if lang not in added_list:
                    try:
                        G.add_node(lang)
                        G.add_edge(lang,simplelangTree.langList[lang].parent[0])
                        added_list.append(lang)
                    except:
                        unadded_list.append(lang)   
        unadded_num_list.append(len(simplelangTree.langList)-len(added_list))
        print(str(len(simplelangTree.langList)-len(added_list))+" languages haven't been added.")
    final_unadded = \
    ", ".join(list(set(simplelangTree.langList.keys())-set(list(G.nodes))))
    print("These languages are not added: "+final_unadded+"\n\n")
    depth = 0
    nx.set_node_attributes(G, depth, "depth")
    for node in G:
        G.nodes[node]["depth"] = nx.shortest_path_length(G, source=root, target=node)
    max_len = 0
    for node in G:
        if G.nodes[node]["depth"] > max_len:
            max_len = G.nodes[node]["depth"]
    plt.figure(figsize=(25, 25))
    color_map = []
    size_map = []
    for node in G:
        if node == root:
            color_map.append('red')
            size_map.append(500)
        elif node in G.neighbors(root):
            color_map.append('orange')
            size_map.append(400)
        elif G.nodes[node]["depth"] == 2:
            color_map.append('green')
            size_map.append(int(450*(1-G.nodes[node]["depth"]/max_len)+10*(G.nodes[node]["depth"]/max_len)))
        elif G.nodes[node]["depth"] == 3:
            color_map.append('brown')
            size_map.append(int(450*(1-G.nodes[node]["depth"]/max_len)+10*(G.nodes[node]["depth"]/max_len)))
        else: 
            color_map.append('yellow')
            size_map.append(int(450*(1-G.nodes[node]["depth"]/max_len)+10*(G.nodes[node]["depth"]/max_len)))
    nx.draw(G,node_size=size_map, alpha=1, node_color=color_map,with_labels=True)
    plt.title('Linguistic Tree of '+root+" Languages",fontsize=20)
    plt.axis("equal")
    plt.show()

def lang_graph(lang_dist_json,lang_list_json,threshold=1):
    import networkx as nx
    from networkx.algorithms import community
    import re
    import matplotlib.pyplot as plt
    import pydot
    from networkx.drawing.nx_pydot import graphviz_layout
    import itertools
    import math
    lang_dist = read_from_json(lang_dist_json)
    lang_list = read_from_json(lang_list_json)
    G = nx.Graph()
    for lang in lang_list:
        G.add_node(lang)
    for sublist in lang_dist:
        if sublist[-1]<threshold:
            G.add_edge(sublist[0][0],sublist[0][1],weight=sublist[-1])
    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(G,k=2/math.sqrt(len(lang_list)))
    nx.draw(G, pos, alpha=1, node_size=10, with_labels=False, edge_color='blue')  
    nx.draw_networkx_labels(G, pos, font_color='black', font_size=16)
    plt.title("Linguistic Graph of 243 Languages\nThreshold="+str(threshold),fontsize=20)
    plt.axis("equal")
    plt.show()

def get_sim_matrix(lang_dist_json,lang_list_json):
    lang_dist = read_from_json(lang_dist_json)
    lang_list = read_from_json(lang_list_json)
    dict_1 = {}
    for sublist in lang_dist:
        pair = sublist[0]
        dict_1[tuple(pair)] = sublist[-1]
        pair.reverse()
        dict_1[tuple(pair)] = sublist[-1]
    for lang in lang_list:
        dict_1[(lang,lang)] = 0
    return dict_1

def lang_dendrogram(lang_dist_json,lang_list_json,json=None,start=None,orientation="right"):
    import numpy as np
    from scipy.cluster.hierarchy import dendrogram, linkage
    from scipy.spatial.distance import squareform
    import matplotlib.pyplot as plt
    import re
    lang_dist = read_from_json(lang_dist_json)
    lang_list = read_from_json(lang_list_json)
    sim_dict = get_sim_matrix(lang_dist_json,lang_list_json)
    if start==None:
        pass
    else:
        if isinstance(start,list):
            list_4=[]
            for start_1 in start:
                list_of_pairs = get_parent_child_pair(json,status="classification",start=start_1)
                list_3 = []
                for i in list_of_pairs:
                    if i[0] not in list_3:
                        list_3.append(i[0])
                    if i[1] not in list_3:
                        list_3.append(i[1])
                for lang in lang_list:
                    n = 0
                    for lang_3 in list_3:
                        if re.findall(lang,lang_3,re.M|re.I)!=[]:
                            n += 1
                    if n >0:
                        list_4.append(lang)
        else:
            list_of_pairs = get_parent_child_pair(json,status="classification",start=start)
            list_3 = []
            for i in list_of_pairs:
                if i[0] not in list_3:
                    list_3.append(i[0])
                if i[1] not in list_3:
                    list_3.append(i[1])
            list_4 = []
            for lang in lang_list:
                n = 0
                for lang_3 in list_3:
                    if re.findall(lang,lang_3,re.M|re.I)!=[]:
                        n += 1
                if n >0:
                    list_4.append(lang)
        lang_list = list(set(list_4))
    list_2 = []
    for lang_1 in lang_list:
        list_1 = []
        for lang_2 in lang_list:
            list_1.append(sim_dict[(lang_1,lang_2)])
        list_2.append(list_1) 
    mat = np.array(list_2)
    print(mat.shape)
    dists = squareform(mat)
    linkage_matrix = linkage(dists, "single")
    if start==None:
        if orientation == "right":
            fig = plt.figure(figsize=(100, 40))
            ax = fig.add_subplot(1, 1, 1)
            dendrogram(linkage_matrix, labels=lang_list,ax=ax)
        else:
            fig = plt.figure(figsize=(15,mat.shape[0]/3))
            ax = fig.add_subplot(1, 1, 1)
            dendrogram(linkage_matrix, labels=lang_list,ax=ax,orientation='left')
        plt.title("Linguitic dendrogram of 243 Languages",fontsize=80)
        ax.tick_params(axis='x', which='major', labelsize=20)
        ax.tick_params(axis='y', which='major', labelsize=20)

    elif start=="Altaic" or "Altaic" in start:
        if isinstance(start,list):
            start = ", ".join(start)
        else:
            pass
        if orientation == "right":
           fig = plt.figure(figsize=(15, 7))
           ax = fig.add_subplot(1, 1, 1)
           dendrogram(linkage_matrix, labels=lang_list,ax=ax)
        else:
           fig = plt.figure(figsize=(10,mat.shape[0]/4))
           ax = fig.add_subplot(1, 1, 1)
           dendrogram(linkage_matrix, labels=lang_list,ax=ax,orientation='left')
        plt.title("Linguitic dendrogram of "+str(start)+" Languages",fontsize=20)
        ax.tick_params(axis='x', which='major', labelsize=10)
        ax.tick_params(axis='y', which='major', labelsize=10)

    else:
        if isinstance(start,list):
            start = ", ".join(start)
        else:
            pass
        if orientation == "right":
            fig = plt.figure(figsize=(15, 7))
            ax = fig.add_subplot(1, 1, 1)
            dendrogram(linkage_matrix, labels=lang_list,ax=ax, color_threshold=0.3)
        else:
            fig = plt.figure(figsize=(10,mat.shape[0]/4))
            ax = fig.add_subplot(1, 1, 1)
            dendrogram(linkage_matrix, labels=lang_list,ax=ax, color_threshold=0.3,orientation='left')
        plt.title("Linguitic dendrogram of "+start+" Languages",fontsize=20)
        ax.tick_params(axis='x', which='major', labelsize=10)
        ax.tick_params(axis='y', which='major', labelsize=10)

    return fig



