# celebrity_database_search
a collection of celebrities data and multi point search

**"readme.pdf" inside the celeb_idb contain images and explanation, read that for better understanding**

**BACKGROUND**

I have started this project for several reasons, those are

1. To get some experience on Data scraping from online
2. To get some experience on Python &quot;BeautifulSoup&quot; package.
3. How to make own database and parse them
4. How to use tkinter table widget.
5. And overall to strengthen my python skill

**IDB DATABASE**

It is a custom made database system (for sake of trying). It is mainly python multidimensional list which is pickled by python pickle package. The first element of the list is a Dictionary. The list look like this [{},[],[]]. The first element of the list, which is a dictionary contain the title/header name and datatype. Currently it supports two types of data 1. String 2.  Float. Integers are automatically converted to a floating point.

Example of idb data.

[{&quot;id&quot;:&quot;&quot;,&quot;name&quot;:&quot;&quot;,&quot;salary&quot;:&quot;0&quot;}, [&quot;01&quot;,&quot;abcd&quot;,1200.00],[&quot;02&quot;,&quot;efgh&quot;,1100.00]]

To explore the database use pickle.load()

**LIMITATION**

The &quot;lookup.py&quot; is the main module which handle this database, unfortunately this &quot;lookup.py&quot; module and to be exact the whole program is heavily customized to open &quot;female\_celeb.idb&quot; data. In future I will try to add a General purpose idb handler module.

**HOW TO USE THE PROGRAM**

User can input mainly four Commands in input entry box they are Name, Input, Type, Fuzzy. After typing input one should must use &quot;:&quot; colon sign without any space. Then specific arguments next to that colon. The output of that command will be shown in table. All the commands and respected arguments are described below.

**Name**

Command should look like this &quot;name:kate&quot; first the command key &quot;name&quot; then colon &quot;:&quot; and the last is the argument of that command, here we use &quot;kate&quot; as an argument. Press enter to activate the command. It will return celebrity information which contain &quot;kate&quot; in their name.

You can use &quot;name:kate,comment=1&quot; &quot;comment=1&quot; and &quot;comment=2&quot; argument at the end of main name argument. Which will return estimated body type of that celebrity. Comment=1 is for short information, comment=2 is detail version. The body type ratios are in &quot;classifier.py&quot; module, you can change the ratio as your preferences.

**Input**

Command should look like this &quot;input:5.4&quot; or &quot;input:5.4,34,27,35&quot;, here first one is only height, and second one is, height, chest, waist, and hip. If you use second way you must need to specify all three arguments with height value.

Let say someone&#39;s measurement is 5.4,35,27,36, this command will show which celebrities are sharing almost same body shape. Or how much modification needed to be a perfect body shape, or other five type shapes classified in classifier.py module.

Though height value looks like decimal, but it is not. Here 5.4 means 5 feet 4 inches. This system is wired, need to be changed. [In future]

You can also use centimeter value instead of inch and feet. There is a bug in conversation of unit. Need to fix.

At the end of argument, using &quot;comment=1&quot; or &quot;comment=2&quot; will provide comments and &quot;thres=1&quot; or any numeric value after &quot;thres=&quot; will give much for precise result. Default threshold is 5.

**Type**

Command should look like this &quot;type:perfect&quot; or &quot;type:big hip&quot;, there are 5 body type included in &quot;classifier.py&quot; module. You can add more option by including the name and ratio in that module.&quot;comment=1 or 2&quot; can be use here. you can change the ratio as your preferences.

**Fuzzy- most useful**

**To make this program general purpose (work with any database) this method need to polish more.**

It is actually multiple point search (not strictly fuzzy) and the most powerful command. You can use any of the command described before, or combined two or more commands. You can use data title/header as well. The listed title in &quot;female\_celeb.idb&quot; are, height, weight, bra size, chest, waist, hip, birthday, nationality, occupation and eye.

If you want to find celebrity with brown eyes, height 5 feet 5 and waist 27 inch then the fuzzy search will look like this  &quot;fuzzy:eye=brown,height=5.5,waist=27&quot;

If you want more precise result you can use threshold, so it will look like this.

&quot;fuzzy:eye=brown,height=5.5,waist=27,thres=1&quot; Or with comment

&quot;fuzzy:eye=brown,height=5.5,waist=27,thres=1,comment=1&quot;

**Extra**

show:1 command will enable image viewer, and show:0 will disable the viewer

size:500,500 (or any x,y value) will change the viewer size.

save: command will save &quot;show&quot; and &quot;size&quot; value in option.opt

Python imaging library (pillow, pip install pillow) will required. For this commands.

Image enabled database required for this, the image title will contain the path of the image file. &quot;image title contain the path of the image&quot;.

&quot;data\_access.pyw&quot; is a simple program to modify &quot;female\_celeb.idb&quot; database and should work with other &quot;idb&quot; database where first element is the dictionary with title and type. (Maybe won&#39;t work right now, bug need to be fixed)

In name entry box type the name and press search, it will return all the value the name contain. The name must need to be exact as stored in database for safety purpose.

You can add new info by providingall the information.
