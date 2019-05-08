import os,pickle
from classifier import Classifier

class Lookup(object):
    def __init__(self,info_label=None):
        database="female_celeb.idb"
        #database="/female_celeb.idb"
        path= os.getcwd()+"/"+database
        with open (path,"rb") as idb:
            self.body_info=pickle.load(idb)
        
        
        self.unit={'name':"",'height':0.0328084,'weight':0.453592,'bra size':"",\
                  'chest':0.393701,'waist':0.393701,'hip':0.393701,'birthday':"",'nationality':"",'occupation':"",'eye':""}
        
        self.label_text=[key for key in self.body_info[0]]
        self.l_text=len(self.label_text)
        self.l_text+=1
        self.body_info.pop(0)
        self.l=len(self.body_info)
        self.mode_selector={'height':10,'chest':52,'waist':52,'hip':52,'weight':90}
        if info_label:
            info_label.config(text="database : "+database+" | total data: %d -loaded"%(self.l/self.l_text))
    
    def unit_convert(self,data={},rounding=2):
        """automatic convert unit based on mode_selector data"""
        for key in data:
            if key in self.unit:
                value=self.unit[key]
                if value=="":
                    pass #string no modification
                else:
                    mode_val=self.mode_selector[key]
                    data_val=float(data[key])
                    if data_val<mode_val:
                        temp=str(round(data_val/value,rounding))
                        data[key]=temp
                    else:
                        temp=str(round(data_val*value,rounding))
                        data[key]=temp
        return data
    
    def __labeler(self,retrived_data) -> dict:
        #["name","height","weight","bra size","chest","waist","hip","birthday","nationality","occupation","eye"]
        labels=self.label_text
        holder_d={}
        retrived_data.remove('end')
        for i,d in enumerate(retrived_data):
            label=labels[i]
            holder_d[label]=d
        return holder_d    
    
    def retrive(self,key):
        holder=[]
        if type(key)!=int:
            index=self.body_info.index(key)
        else:
            index=key
        for i in range(index,index+self.l_text):
            holder.append(self.body_info[i])
        return self.__labeler(holder)
    
    def unit_labeler(self,data={}):
        height=float(data["height"])
        if height<10:
            units={'height':"feet",'weight':"kg",'chest':"in",'waist':"in",'hip':"in"}
        else:
            units={'height':"cm",'weight':"lb",'chest':"cm",'waist':"cm",'hip':"cm"}
        
        for key in units:
            unit=units[key]
            data[key]=data[key]+" "+unit
        h_d=data['height']
        if " feet" in h_d:
            h_d=h_d.replace(" feet","")
            h_d=float(h_d)
            h_d="%d feet %d inch"%(int(h_d),int(round((h_d*12)%12,0)))
            data['height']=h_d 
        return data
    
    def fuzzy_search(self,common=(),thres=5,**kwarg):
        thres_list=["chest","waist","hip","height","weight"]
        fuzzy_holder=[]
        if common:
            for i,value in enumerate(common):
                key_C=thres_list[i]
                kwarg[key_C]=value
            print("fuzzy search :", kwarg,"\n")
            
        l_kwarg=len(kwarg)
        if l_kwarg>=1:
            for k in kwarg:
                if k not in self.label_text:
                    return -1 #stop here
            else:
                kwarg=self.unit_convert(kwarg)
        
        for i in range(0,self.l,self.l_text):

            retrived_profile=self.retrive(i) #i is index of name, retrive_profile ->dict
            counter=0
            for key in kwarg:
                kw_val=kwarg[key]
                try:
                    retrived_val=retrived_profile[key] #all the key of self.unit is valid
                except:
                    raise KeyError("keyword : %s is not valid"%key)
                if key in thres_list:
                    retrived_val=float(retrived_val)
                    percent=(float(kw_val)*thres)/100
                    low=float(kw_val)-percent
                    high=low+(percent*2)
                    if low<retrived_val<high: #if retrived_val (height,weight....) is between threhold
                        counter+=1
                else:
                    if kw_val.lower() in retrived_val.lower():
                        counter+=1
            if counter==l_kwarg: #counter is counting how many kwarg value is matching, if every value mathced then append
                fuzzy_holder.append(retrived_profile)
        return fuzzy_holder
           
    def search_type(self,key,mode=1):
        """mode =1 first match, mode =2 both first and second"""
        cl_obj=Classifier(label_text=self.label_text)
        count=0
        type_result=[]
        for i in range(0,self.l,self.l_text):
            retrived_profile=self.retrive(i) #i=index of name
            t=cl_obj.celeb_data_handler(retrived_profile,1)
            if mode==1:
                if t["shape 1"][0]==key:
                    count+=1
                    type_result.append(retrived_profile)
                    
            elif mode==2:
                if t["shape 1"][0]==key or t["shape 2"][0]==key:
                    count+=1
                    type_result.append(retrived_profile)
        return (count,type_result)

if __name__=="__main__":
    obj=Lookup()
    kwarg={'name':"ale"}
    x=obj.fuzzy_search(**kwarg)
    for i in x:
        print(i)
