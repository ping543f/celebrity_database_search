import os,pickle
import tkinter

class Gui(tkinter.Frame):
    def __init__(self,root=tkinter.Tk):
        self.root=root
        self.path=os.getcwd()+"/female_celeb.idb"
        self.data=None
        tkinter.Frame.__init__(self,root)
        self.root.resizable(1,0)
        self.root.title("data access")
        root.columnconfigure(1, weight=1)        
        
        with open(self.path,"rb") as idb:
            data=pickle.load(idb)
        self.data=data
        self.data_structure=data[0]
        self.labels=[key for key in data[0]]
        self.labels_type=[data[0][key] for key in data[0]]
        self.data.pop(0)
        
        self.d_l=len(self.data)
        self.l=len(self.labels)
        self.e_var=[tkinter.StringVar() for i in range(self.l)]
        
        self.start_point=-1
        #-----------
        for i in range(self.l):
            entry=tkinter.Entry(self.root,textvariable=self.e_var[i])
            entry.bind("<Button-3>",self.entry_command)
            entry.grid(row=i,column=1,sticky="nsew")
            label=tkinter.Label(self.root,text=self.labels[i])
            label.grid(row=i,column=0)
        
        #----frame
        self.control_frame=tkinter.LabelFrame(self.root,text="control")
        self.control_frame.grid(row=i+3,column=0,columnspan=2)
        
        self.search=tkinter.Button(self.control_frame,text="search",width=6,command=self.search_button)
        self.search.pack(side="left",fill="both",padx=2)
        
        self.update=tkinter.Button(self.control_frame,text="update",width=6,command=self.update_button)
        self.update.pack(side="left",fill="both",padx=2)
        
        self.add=tkinter.Button(self.control_frame,text="add",width=6,command=self.add_button)
        self.add.pack(side="left",fill="both",padx=2)
        
        self.delete=tkinter.Button(self.control_frame,text="delete",width=6,command=self.delete_button)
        self.delete.pack(side="left",fill="both",padx=2)         
        
        self.info=tkinter.Label(self.root,text="unit must be in cm and pound")
        self.info.grid(row=i+1,column=0,columnspan=2,sticky="ne")
        
    def __data_update(self):
        self.data.insert(0,self.data_structure)
        with open(self.path,"wb") as idb:
            pickle.dump(self.data,idb)
        self.data.pop(0)
        
    def entry_command(self,e=0):
        focus=root.focus_get()
        value=focus.get()
        focus=str(focus)[-1]
        if focus.isdigit():
            focus=self.e_var[int(focus)-1]
        else:
            focus=self.e_var[0]
        if 'in' in value:
            value=value.replace("in","")
            try:
                value=float(value)
                value=round(value*2.54,2)
                focus.set(str(value))
            except:
                focus.set('0')
        elif 'feet' in value:
            value=value.replace("feet","")
            try:
                if "," in value:
                    value=value.split(',')
                    value=((int(value[0])*12+float(value[1]))/12)*30.48
                    focus.set(str(round(value,2)))
                else:
                    value=float(value)*30.48
                    focus.set(str(round(value,2)))
            except:
                focus.set('0')
        elif 'kg' in value:
            value=value.replace("kg","")
            try:
                value=float(value)
                value=round(value*2.20462,2)
                focus.set(str(value))
            except:
                focus.set('0')
        elif 'm' in value:
            value=value.replace("m","")
            try:
                value=float(value)
                value=round(value*100,2)
                focus.set(str(value))
            except:
                focus.set('0')
                            
    def search_button(self,mode=0):
        self.start_point=-1
        name=self.e_var[0].get()
        for i in range(0,self.d_l,self.l+1):
            retrive_name=self.data[i]
            if name==retrive_name.lower():
                self.start_point=i
                break
        if self.start_point!=-1:
            count=0
            for i in range(self.start_point,self.start_point+self.l,1):
                data=self.data[i]
                self.e_var[count].set(data)
                count+=1
            self.info.config(text="%s found"%name)
        elif mode==0:
            for i in self.e_var[1:]:
                i.set('')
            self.info.config(text="%s not found"%name)
    def update_button(self):
        if self.start_point!=-1:
            count=0
            name=self.e_var[0].get()
            for i in range(self.start_point,self.start_point+self.l,1):
                self.data.pop(i)
                value=self.e_var[count].get()
                self.e_var[count].set("")
                count+=1
                self.data.insert(i,value)
            self.__data_update()
            self.info.config(text="data updated")
            
    def add_button(self):
        valid=1
        if self.e_var[0].get()=="":
            self.info.config(text="name needed")
            valid=0
        else:
            self.search_button(mode=1)
        if self.start_point==-1 and valid==1:
            temp=[]
            for i,l in enumerate(self.labels):
                value=self.e_var[i].get()
                if value=="":
                    value=self.labels_type[i]
                temp.append(value)
            for i,d in enumerate(temp):
                self.data.append(d)
                self.e_var[i].set("")
            self.data.append('end')
            self.start_point=-1
            self.__data_update()
            self.info.config(text="data Added") 
            self.d_l+=self.l
        else:
            if valid!=0:
                self.info.config(text="Already exists")
    def delete_button(self):
        self.start_point=-1
        name=self.e_var[0].get()
        for i in range(0,self.d_l,self.l+1):
            retrive_name=self.data[i]
            if name==retrive_name.lower():
                self.start_point=i
                break
        if self.start_point!=-1:
            count=0
            start=self.start_point
            end=self.start_point+self.l+1
            while start!=end:
                self.data.pop(i)
                end-=1
            self.__data_update()
            self.info.config(text="%s deleted"%name)
            self.d_l-=self.l
        else:
            for i in self.e_var[1:]:
                i.set('')
            self.info.config(text="%s not found to delete"%name)
root=tkinter.Tk()
obj=Gui(root)
obj.mainloop()
    

