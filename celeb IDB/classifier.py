class Classifier(object):
    def __init__(self,label_text=[]):
        self.r=1 #rounding          0-waist,  1-hip,    2-bust
        self.ratio={'perfect':     [0.406313, 1.391733, 1.310501],
                    'thin perfect':[0.38951,  1.282578, 1.236774],
                    'curvy':       [0.420529, 1.514601, 1.49053 ],
                    'big hip':     [0.375014, 1.532229, 1.353514],
                    'big bust':    [0.420529, 1.293529, 1.490553]
                    }
        self.label_text=label_text
    def set_label(self,label_text):
        self.label_text=label_text

    def five_shape(self,height):
        shape_holder={}
        height=float(height)

        if height<10:
            height=height*12 #if feet >to inch
        else:
            height=height*0.393701 #if cm >to inch

        shape_holder["height"]=[round(height/12,self.r)]

        for key in self.ratio:
            shape_ratio=self.ratio[key]
            waist=round(height*shape_ratio[0],self.r)
            hip=round(waist*shape_ratio[1],self.r)
            bust=round(waist*shape_ratio[2],self.r)
            shape_holder[key]=[bust,waist,hip]

        return shape_holder
    #---------------------------------------------------------------------------------------------------------------------------------------------
    def inputed_shape(self,data=()):
        if len(data)!=4:
            return 0
        else:
            height,bust,waist,hip=data
            five_shape=self.five_shape(height)
            five_shape["input"]=[round(float(bust),self.r),round(float(waist),self.r),round(float(hip),self.r)]
            return five_shape

    def difference(self,inputed_five_data):
        inputed_five=dict(inputed_five_data)
        input_val=inputed_five["input"]
        inputed_five.pop("input")
        inputed_five.pop("height")
        diff_holder={}
        for shape in inputed_five:
            temp=[]
            val=inputed_five[shape]
            for i in range(3):
                m=val[i]-input_val[i]
                temp.append(round(m,self.r))
            diff_holder[shape]=temp
        return diff_holder

    def comment(self,difference):
        diff_holder={}
        sub=0.001
        def diff_calc(data=[]):
            h=0
            l=0
            for i in data:
                if i>0:
                    h+=i
                else:
                    l+=i
            return (h-l)
        temp_d={}
        for key in difference:
            val=difference[key]
            diff=diff_calc(val)
            if diff in temp_d:
                sub+=0.0001
                diff=diff+sub
            temp_d[diff]=[key,val]
        for i,key in enumerate(sorted(temp_d)):
            diff_holder[i]=temp_d[key]
        return diff_holder

    def report(self,shape=()):
        data={}
        inp_shape=self.inputed_shape(shape)
        difference=self.difference(inp_shape)
        comment=self.comment(difference)

        data["shape"]=inp_shape
        data["comment"]=comment
        return data

    def report_simple(self,shape=()):
        output={}
        if type(shape)==tuple:
            report=self.report(shape)
        else:
            report=shape
        output["input"]=report["shape"]["input"]
        output["shape 1"]=report["comment"][0]
        output["shape 2"]=report["comment"][1]
        return output

    def celeb_data_handler(self,data,report=0):
        if type(data)==dict:
            temp=[]
            for i in data:
                temp.append(data[i])
            data=temp
        height_in=self.label_text.index('height')
        c_in=self.label_text.index('chest')
        w_in=self.label_text.index('waist')
        h_in=self.label_text.index('hip')

        height=round(float(data[height_in]),self.r)
        chest=round(float(data[c_in]),self.r)
        waist=round(float(data[w_in]),self.r)
        hip=round(float(data[h_in]),self.r)
        if not height<10:
            height=round(height*0.0328084,self.r)
            chest=round(chest*0.393701,self.r)
            waist=round(waist*0.393701,self.r)
            hip=round(hip*0.393701,self.r)
        if report==0:
            return self.report((height, chest,waist,hip))
        elif report==1:
            return self.report_simple((height, chest,waist,hip))

if __name__=="__main__":
    import lookup
    obj1=lookup.Lookup()
    x=obj1.fuzzy_search(name="alex")
    obj=Classifier(label_text=obj1.label_text)
    for i in x:
        print(obj.celeb_data_handler(i))
