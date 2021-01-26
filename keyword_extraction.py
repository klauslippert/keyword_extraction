import pandas as pd

class DictLU_Create_Dict():
    def __init__(self,df):
        '''
        USAGE: 
            from dictionary_lookup import *
            DC = DictLU_Create_Dict(df_lookuplist)
            dicts_lower = DC.dicts_lower
            dicts_upper = DC.dicts_upper
            
        input: df with columns "id" and "term"
        output: 2 lists of dicts (for uppercase and lowercase words)
                sorted each by num of grams
                with each having:
                    key: ' ' + term + ' '  
                    value: MeSH-id
        
        2do check input type
        2do check input column-names
        '''
        self.df = df
        _=self.split_into_upper_lower()
        
        self.dicts_upper = self.create_dicts(self.dfupper,False)
        self.dicts_lower = self.create_dicts(self.dflower,True)
        
        
    def split_into_upper_lower(self):
        ''' split into plain upper and upper/lower-mixed words
            keep upper ones and lower/mixed ones
        '''
        self.df['pure_upper']=[x.isupper() for x in self.df['term']]
        self.df['numb_grams'] = [len(s.split()) for s in self.df['term']]

        self.dfupper = self.df[self.df['pure_upper']==True]\
                       .reset_index(drop=True)\
                       .drop(columns='pure_upper')
        self.dflower = self.df[self.df['pure_upper']==False]\
                       .reset_index(drop=True)\
                       .drop(columns='pure_upper')
    
    def create_dicts(self,df2,flag_lower):
        ''' create list of dicts with one dict for each n-gram.
            key: term  value: id
        '''
        alldicts=[]
        
        for ngrams in range(1,max(df2['numb_grams'])+1):
            df3 = df2[df2['numb_grams']==ngrams].reset_index(drop=True)
            if flag_lower:
                alldicts.append(dict(zip([x.lower() for x in df3['term']],
                                         df3['id'])))
            else:
                alldicts.append(dict(zip(df3['term'],
                                         df3['id'])))
        return alldicts        
    
    
class DictLU_Extract_Exact():
    def __init__(self,dicts_upper,dicts_lower):
        
        '''USAGE:
           from dictionary_lookup import *
           DEE=DictLU_Extract_Exact(dicts_upper,dicts_lower)
           DEE.run(text)
           result = DE.result
           
        '''
        #load list of dicts
        self.dicts_upper = dicts_upper
        self.dicts_lower = dicts_lower

        self.punct_list = [' ',',', '.', '?', '!','"',':','’',
                           '(',')','[',']','{','}' ]        
        

        
    def run(self,raw_text):
        '''extraction process
        '''
        
        self.text = raw_text
        
        text, found_words_upper = self.extract(self.dicts_upper,raw_text)
        
        text = text.lower()
        text, found_words_lower = self.extract(self.dicts_lower,text)                    
        #print(found_words_lower)
        
        found_words = found_words_upper + found_words_lower
                    
        unique_ids = list(set([x[1] for x in found_words]))

        words = [x[0] for x in found_words]
        ids   = [x[1] for x in found_words]
        start = [x[2] for x in found_words]
        end   = [x[3] for x in found_words]

        idx=[]
        for this_id in unique_ids:
            idx.append([i for i,val in enumerate(ids) if val==this_id])
    
        result=dict()   
        for this_idx in idx:
            result.update( {ids[this_idx[0]]: {'count':len(this_idx),
                                               'term': words[this_idx[0]] ,  
                                               'pos':[(start[x],  end[x]) for x in this_idx]
                                              }
                            }
                          )
        self.result=result
        self.proc_text = text
        
    def extract(self,all_dicts,text):   
        
        found_words=[]
        text=text+' '
        for this_dict in all_dicts[::-1]:
    
            for searchword in list(this_dict.keys()):
            #searchword = proc_punct(searchword)
                
        
                while 1==1:
                    start_index = text.find(searchword)
                    
                    if start_index not in [-1]:
                        end_index = start_index + len(searchword) 
                        ## is it a word with only punctuation as sourounding?
                        ## yes ? then extract it
                        if ( (start_index == 0) and \
                             (text[end_index] in self.punct_list) ) \
                           or \
                           ( (text[start_index-1] in self.punct_list) and \
                             (text[end_index] in self.punct_list) ) :
                           
                            search_id=this_dict[searchword]
                            found_words.append((searchword,search_id,start_index,end_index))
                            
                        ## anyway, mask the word for next loop
                        text = text[:start_index] +\
                               '_'*len(searchword) +\
                               text[end_index:]
                    else: 
                        break
        return text, found_words
    
            
    def create_html(self):
        '''creates an html page out of the text 
           with the extracted words in red
        '''
        text=self.text
        a=[x[1]['pos'] for x in self.result.items()]
        b=[item for sublist in a for item in sublist]
        c = sorted(b, key=lambda tup: tup[0])
        
        pre = '<!DOCTYPE html> <html>  <head>  <!-- head definitions go here -->    </head>    <body>'
        post = '</body> </html>'

        string=pre+text[:c[0][0]]
        for i in range(0,len(c)):
            string = string + '<font color="red">{'+text[c[i][0]:c[i][1]]+'}</font>'
            if i != len(c)-1:
                string = string + text[c[i][1]:c[i+1][0]]
            
        string = string + text[c[-1][1]:]+post
        
        self.html=string

        # try: as hover information give the mesh-ID
        #d=[x[0] for x in DEE.result.items()]
        #print(d)
        #<span title="I am hovering over the text">This is the text I want to have a mousover</span>

        
        
        

    
class DictLU_Extract_Fuzzy():
    def __init__(self,dicts_upper,dicts_lower):
        ''' the idea is to calc a string distance (levenshtein or jaccard) score to 
        find mesh terms with typos, singular/plural, etc.
        '''
        pass
    
