from lookup import Lookup
from classifier import Classifier
from tkinter import ttk
try:
    from PIL import ImageTk,Image
except:
    pass
import tkinter,os

#------------------------------------------------------------------------------------------------------------------------------------------------
class Main_UI(tkinter.Frame):
    def __init__(self,root=tkinter.Tk):
        self.cwd=os.getcwd()+"/option.opt"
        if not os.path.exists(self.cwd):
            with open (self.cwd, "w") as txt:
                txt.write("0,200,200")
        
        tkinter.Frame.__init__(self,root)
        self.root=root
        self.root.title("celebrity")
        self.root.minsize(385,458)
        
        self.column=["title","value"]
        self.column_width=[130,220]
        self.entry_var=tkinter.StringVar()
        
        #----frame---
        self.view_frame=tkinter.LabelFrame(self.root,text="Viewer")
        self.view_frame.pack(padx=2,pady=2,fill="both",expand=True)
        
        #---treeview---
        self.tree=ttk.Treeview(self.view_frame,height=18)
        self.tree.pack(padx=2,pady=3,fill="both",expand=True)
        
        self.tree["columns"]=self.column
        self.tree.bind("<<TreeviewSelect>>",self.treeview_bind)
        
        self.show_img=0
        self.image_path=os.getcwd()+"/images"
        
        for index,col in enumerate(self.column):
            self.tree.heading(col,text=col)
            self.tree.column(col,width=self.column_width[index])
            
        self.tree.column('#0',width=20,stretch=0)
        self.tree.column('title',stretch=0)
        #---treeview tag------
        self.tree.tag_configure("gray",background="gray95")
        self.tree.tag_configure("white",background="white")
        self.tree.tag_configure("gray2",background="ghost white")
        
        #----------entry-----------------
        self.entry=tkinter.Entry(self.root,textvariable=self.entry_var)
        self.entry.pack(padx=3,pady=1,fill="x")
        self.entry.bind("<Return>",self.entry_command)
        self.entry.focus()
        #----------label-----------------
        self.info=tkinter.Label(self.root,text="Information panel")
        self.info.pack(anchor="se")
        
        #module
        self.classifier=Classifier()
        self.lookup=Lookup(info_label=self.info)        
        
        #canvas
        self.top_level=None
        self.count=0
        self.img=None
        self.t_size=(200,200)
        self.__load_opt()
        
        self.col_d=0
        self.img_counter=0
        self.old_val=None
    def parser(self,arg):
        tuple_arg=None #fuzzy:()
        kwarg=None     #fuzzy:name=""
        base=None      #name:"", type:""
        
        error=0
        def tuple_get(arg=""):
            if "(" in arg and ")" in arg:
                try:
                    point_f=arg.index("(")
                    point_s=arg.index(")",point_f)
                    extract=arg[point_f+1:point_s]
                    extract=extract.split(",")
                    if point_f!=0:
                        point_f-=1
                    elif point_f==0:
                        point_s+=1                    
                    arg=arg.replace(arg[point_f:point_s+1],"")
                    return (arg,extract)
                except:
                    error=1
                    self.info.config(text="invalid tuple data")
            else:
                return (arg,None)
        def base_get(arg=''): #without tuple
            arg_temp=arg.split(",")
            base_val=[]
            for i in list(arg_temp):
                if "=" not in i and i!="":
                    base_val.append(i)
                    arg_temp.remove(i)
            if base_val:
                return (",".join(arg_temp),base_val)
            else:
                return (",".join(arg_temp),None)
            
        def kwarg_get(arg=""): #without tuple, base
            arg=arg.split(",")
            if arg[0]=="":
                return None
            else:
                k_holder={}
                for item in arg:
                    if "=" not in item:
                        self.info.config(text="invalid keyword argument")
                        error=1
                    else:
                        item=item.split("=")
                        k_holder[item[0]]=item[1]
                return k_holder

        arg,tuple_arg=tuple_get(arg)
        if not error:
            arg,base=base_get(arg)
            kwarg=kwarg_get(arg)
            
        if not error:
            return {'base':base,'tuple':tuple_arg,'kwarg':kwarg}
        else:
            return 0
        
        

                
    def __load_opt(self):
        with open(self.cwd,"r") as txt:
            val=txt.read()
            val=val.split(",")
            self.show_img=int(val[0])
            self.t_size=(int(val[1]),int(val[2]))
            
    def fuzzy_command(self,t_arg=(),kwarg={},type_search=False):
        thres=5
        comment=0
        unit=1
        key=None #type search
        mode=1 #type search
        def pop_retrive(key):
            val=kwarg[key]
            kwarg.pop(key)
            return val
        if 'thres' in kwarg:
            thres=int(pop_retrive('thres'))
        if 'comment' in kwarg:
            comment=int(pop_retrive('comment'))
        if 'unit' in kwarg:
            unit=int(pop_retrive('unit'))
        if 'key' in kwarg:
            key=pop_retrive('key')
        if 'mode' in kwarg:
            mode=int(pop_retrive('mode'))
        if 'height' in kwarg:
            temp=kwarg['height']
            if float(temp)<10 and type(temp)!=float:
                kwarg['height']=self.__height_convert(temp)
        if t_arg:
            if len(t_arg)==4:
                h=t_arg[3]
                if float(h)<10:
                    if "." in h:
                        h=h.split(".")
                        f=int(h[0])*12+int(h[1])
                        h=str(round(f/12,2))
                        t_arg_temp=list(t_arg)
                        t_arg_temp.pop(3)
                        t_arg_temp.append(h)
                        t_arg=t_arg_temp
            
        if not type_search:
            fuzzy_result=self.lookup.fuzzy_search(t_arg,thres,**kwarg)
            result_found=len(fuzzy_result)
        else:
            if kwarg:
                fuzzy_result1=self.lookup.fuzzy_search(t_arg,thres,**kwarg)
                result_found,fuzzy_result2=self.lookup.search_type(key,mode)
                fuzzy_result=[]
                result_found=0
                for i in fuzzy_result1:
                    if i in fuzzy_result2:
                        result_found+=1
                        fuzzy_result.append(i)
            else:
                result_found,fuzzy_result=self.lookup.search_type(key,mode)                   
            
        
        if fuzzy_result==-1:
            self.info.config(text="Error: something wrong with inputed fuzzy argument")
        else:
            if not type_search:
                self.info.config(text="%d result found, threshold %.2f"%(result_found,thres))
            else:
                self.info.config(text="%d \'%s\' result found"%(result_found,key))
            if comment:
                for i,item in enumerate(fuzzy_result):
                    fuzzy_result_convert=self.lookup.unit_convert(dict(item))
                    height=fuzzy_result_convert['height']
                    bust=fuzzy_result_convert['chest']
                    waist=fuzzy_result_convert['waist']
                    hip=fuzzy_result_convert['hip']
                    if comment==1:
                        report=self.classifier.report_simple((height,bust,waist,hip))
                    elif comment==2:
                        report=self.classifier.report((height,bust,waist,hip))
                    
                    if unit==2:
                        self.data_arrange(self.lookup.unit_labeler(fuzzy_result[i]),report,comment=comment,count=i)
                    else:
                        self.data_arrange(self.lookup.unit_labeler(fuzzy_result_convert),report,comment=comment,count=i)
            else:
                for i,item in enumerate(fuzzy_result):
                    fuzzy_result_convert=self.lookup.unit_convert(dict(item))
                    if unit==2:
                        self.data_arrange(self.lookup.unit_labeler(item),comment=comment,count=i)
                    else:
                        self.data_arrange(self.lookup.unit_labeler(fuzzy_result_convert),comment=comment,count=i)
                        
                    
                    
            
    def __insert_tree(self,name,data,i=0):
        tag='gray'
        if i%2==0:
            tag="white"
        try:
            self.tree.insert("",'end',name,value=(name,''),tag=tag)
        except:
            self.col_d+=1
            name=name+" "+str(self.col_d)
            self.tree.insert("",'end',name,value=(name,''),tag=tag)
        
        for n,key in enumerate(data):
            tag2="gray2"
            if n%2==0:
                tag2="white"
            self.tree.insert(name,'end',value=("  "+key,data[key]),tag=tag2)
            
    def data_arrange(self,data,report=None,comment=None,count=0):
        if comment==1: #simple
            name=data['name']
            data.pop('name')
            shape1=report['shape 1']
            shape2=report['shape 2']
            inp=report['input']
            tree_comment="shape is between \'%s\' and \'%s\'"%(shape1[0],shape2[0])
            data[" "]=""
            data["COMMENT"]=tree_comment  
            
            inp=[str(f) for f in inp]
            shape1s=[str(f) for f in shape1[1]]
            shape2s=[str(f) for f in shape2[1]]
        
            inp="%-10s%-10s%-10s"%(inp[0],inp[1],inp[2])
            shape1s="%-10s%-10s%-10s"%(shape1s[0],shape1s[1],shape1s[2])
            shape2s="%-10s%-10s%-10s"%(shape2s[0],shape2s[1],shape2s[2]) 
            data["measurement"]=inp
            data[shape1[0]]=shape1s
            data[shape2[0]]=shape2s    
            self.__insert_tree(name, data,count)
            
        elif comment==2:
            name=data['name']
            data.pop('name')            
            shape=report['shape']
            comments=report['comment']
            
            data[" "]=""                   
            tree_comment="shape is between \'%s\' and \'%s\'"%(comments[0][0],comments[1][0])
            data["COMMENT"]=tree_comment
            
            for i in comments:
                key=comments[i][0]
                val=comments[i][1]
                shape_val=shape[key]
                
                if len(shape_val)==3:
                    vals=[str(f) for f in shape_val]
                    temp=[str(f) for f in val]
                    vals="%-10s%-10s%-10s"%(vals[0],vals[1],vals[2])
                    temp="%-10s%-10s%-10s"%(temp[0],temp[1],temp[2])
                    data[key]=vals
                    data["      %-15s%s"%(key,"+-")]=temp
            self.__insert_tree(name,data,count)
            
        elif comment==0: #no comment
            name=data['name']
            data.pop('name')
            self.__insert_tree(name,data,count)
            
    def __height_convert(self,h=""):
        if "." in h:
            temp=h.split(".")
            height=int(temp[0])*12+int(temp[1])
            height=round(height/12,1)
            return str(height)
        else:
            return str(h)    
                    
    def name_parser(self,kwarg={}):
        self.fuzzy_command(kwarg=kwarg)
            
            
    def input_command(self,base=[],kwarg={}):
        height_val=base[0]
        base=[float(i) for i in base]
        error=0
        l=len(base)

        if l>4:
            error=1
            self.info.config(text="Error: height,bust,waist,hip, ex: 5.7,34,24,36")
        elif l>1 and l<4 or l==0:
            error=1
            self.info.config(text="Error: height,bust,waist,hip, ex: 5.7,34,24,36")
        elif l==1:
            data={}
            height=self.__height_convert(height_val)
            print(height)
            five=self.classifier.five_shape(height)
            height=five['height'][0]
            five.pop('height')
            name='input'
            data['height']=height
            for key in five:
                vals=five[key]
                vals=[str(f) for f in vals]
                vals="%-10s%-10s%-10s"%(vals[0],vals[1],vals[2])
                data[key]=vals
            h_d=float(data["height"])
            h_d="%d feet %d inch"%(int(h_d),int(round((h_d*12)%12,0)))
    
            data['height']=h_d
            self.__insert_tree(name,data)
            self.tree.insert("",'end',"space",value=('',''))
            self.tree.insert("",'end',"best match",value=("CELEBRITY",'celebrity that best match to your shape'))            
            kwarg['height']=height
            self.fuzzy_command(kwarg=kwarg)
            
        elif l==4:
            height=self.__height_convert(height_val)
            bust=base[1]
            waist=base[2]
            hip=base[3]
            
            
        #input:5.7,32,27,32,thres=5.9,comment=2
                     
            report=self.classifier.report((height,bust,waist,hip))
            shape=report["shape"]
            comments=report["comment"]
            data={}
            data['name']='input'
            h_d=float(height)
            h_d="%d feet %d inch"%(int(h_d),int(round((h_d*12)%12,0)))
            data['height']=h_d            
            data['bust']=str(bust)+" in"
            data['waist']=str(waist)+" in"
            data['hip']=str(hip)+" in"
            self.data_arrange(data,report,comment=2)    
            
            self.tree.insert("",'end',"space",value=('',''))
            self.tree.insert("",'end',"best match",value=("CELEBRITY",'celebrity that best match to your shape'))
            
            arg_tuple=(bust,waist,hip,height)
            self.fuzzy_command(arg_tuple,kwarg=kwarg)
        else:
            error=1
            self.info.config(text="Error: height,bust,waist,hip, ex: 5.7,34,24,36")            
            
    
    def type_command(self,k_arg):
        self.fuzzy_command(kwarg=k_arg,type_search=True)
    
    def treeview_bind(self,e=0):
        if self.top_level:
            self.top_level.destroy()        
        focused_item=self.tree.focus()
        values=self.tree.item(focused_item)["values"]
        if 'image' in values[0]:
            if self.show_img:
                images=values[1].split(";")
                if self.img_counter>len(images)-1:
                    self.img_counter=0
                if values!=self.old_val:
                    self.img_counter=0
                self.viewer(images[self.img_counter])
                self.old_val=values
                self.img_counter+=1
    def viewer(self,val):
        def sub(image_tk,size=()):
            x = root.winfo_x()
            y = root.winfo_y()
            val_x=size[0]
            val_y=size[1]
            
            self.top_level = tkinter.Toplevel(self)
            self.top_level.geometry("%dx%d+%d+%d" % (val_x, val_y, x + 400, y))
            self.top_level.wm_title("viewer (%d,%d)"%(val_x,val_y))
            
            canvas = tkinter.Canvas(self.top_level,width=val_x,height=val_y)
            canvas.pack()
            canvas.create_image(int(val_x/2),int(val_y/2),image=image_tk)
            
        if self.top_level:
            self.top_level.destroy()
        if ".jpg" in val or ".JPG":
            try:
                p_img=r"%s"%(self.image_path+val)
                self.img=Image.open(p_img)
                self.img.thumbnail(self.t_size, Image.ANTIALIAS)
                self.img=ImageTk.PhotoImage(self.img)
                y=self.img.height()
                x=self.img.width()
                sub(self.img,size=(x,y))
                self.info.config(text="Image loaded %d, %d"%(x,y))
            except:
                self.info.config(text="Error: can't open image")
                
        
    def entry_command(self,event):
        self.tree.delete(*self.tree.get_children())
        command_list=["fuzzy","input","type","name","show","size","save"]
        text=self.entry_var.get()
        error=0
        if text.count(":")!=1:
            self.info.config(text="Error: wrong input")
            error=1
        elif "unit=" in text:
            b=text.find("unit=")+5
            e=text.find(",",b)
            try:
                if e!=-1:
                    num=int(text[b:e])
                else:
                    num=int(text[b:])
                if num>2 or num<1:
                    error=1
                    self.info.config(text="Error: wrong unit value, unit=1 or 2")
            except:
                self.info.config(text="Error: wrong unit value, unit=1 or 2")
                error=1        
        else:
            temp=text.split(":")
            if temp[0] not in command_list:
                error=1
                self.info.config(text="Error: wrong command, available commands : %s"%", ".join(command_list))

        if error!=1:
            text=text.split(":")
            command=text[0]
            arg=text[1]
            if command=="test":
                x=self.parser(arg)
                if x:
                    for i in x:
                        print(i,":",x[i])
                else:
                    self.info.config(text="Error: something wrong with input")
            if command=="fuzzy":
                parsed=self.parser(arg)
                if parsed:
                    t_arg=parsed['tuple']
                    k_arg=parsed['kwarg']
                    if k_arg==None:
                        k_arg={}
                    self.fuzzy_command(t_arg,k_arg,)
            elif command=="name":
                parsed=self.parser(arg)
                name=parsed['base'][0]
                kwarg=parsed['kwarg']
                if not kwarg:
                    kwarg={}
                kwarg['name']=name
                self.name_parser(kwarg=kwarg)
            elif command=="input":
                parsed=self.parser(arg)
                base=parsed['base']
                kwarg=parsed['kwarg']
                if not kwarg:
                    kwarg={}
                self.input_command(base,kwarg)
            elif command=="type":
                parsed=self.parser(arg)
                key=parsed['base'][0]
                k_arg=parsed['kwarg']
                if k_arg:
                    k_arg['key']=key
                else:
                    k_arg={}
                    k_arg['key']=key                      
                self.type_command(k_arg)
            elif command=="show":
                parsed=self.parser(arg)
                key=parsed['base'][0]
                try:
                    key=int(key)
                    if key==0:
                        self.show_img=0
                        self.info.config(text="image viewer disabled")
                    elif key==1:
                        self.show_img=1
                        self.info.config(text="image viewer enabled")
                    else:
                        self.info.config(text="Error: show_image value can be only 0 or 1")
                except:
                    self.info.config(text="Error: invalid show_image value")
                    
            elif command=="size":
                parsed=self.parser(arg)
                key=parsed['base']
                try:
                    x=int(key[0])
                    y=int(key[1])
                    self.t_size=(x,y)
                    self.info.config(text="viewer size changed to %d, %d"%(x,y))
                except:
                    self.info.config(text="wrong viewer size value ex:200,200")
                    
            elif command=="save":
                with open(self.cwd,"w") as txt:
                    txt.write("%d,%d,%d"%(self.show_img,self.t_size[0],self.t_size[1]))
                    self.info.config(text="option saved")
            
if __name__=="__main__":
    root=tkinter.Tk()
    obj=Main_UI(root)
    obj.mainloop()
