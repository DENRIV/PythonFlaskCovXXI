# python flask_app.py 
# http://127.0.0.1:5000/

# http://anahome.pythonanywhere.com/

import pandas as pd
from flask import Flask, render_template
app = Flask(__name__)
global _IDMAIN
global _STRMENU
global _MSG
_IDMAIN = 0
_MSG = 0
global _READ #  1 XLS. / 2 CSV 
_READ = 1
global _WEBPATH
_WEBPATH = ""
global _RUN # 0 continue / 1 run / 2 run-debug
_RUN = 0
global _MODE # 1 LOCAL / 2 LOCAL DEBUG/ 4 WEB PYTHON ANYWHERE
_MODE = 1
#
def setupapp():
    global _MSG
    global _READ
    global _RUN
    global _WEBPATH
    if _MODE == 1:
        _MSG = 0
        _READ = 1
        _RUN = 1
        _WEBPATH = ""
    if _MODE == 2:
        _MSG = 1
        _READ = 1
        _RUN = 2
        _WEBPATH = ""        
    if _MODE == 4:
        _MSG = 0
        _READ = 2
        _RUN = 0
        _WEBPATH = "/home/ANAHOME/mysite/"    
#
def m1():
    if _READ == 1 :
        df = pd.read_excel('covmenu.xlsx', sheet_name='Hoja1')
    if _READ == 2 :
        df = pd.read_csv(_WEBPATH+'covmenu1.csv')        
    #
    df = df[df['ONOFF'] == 1]
    #
    strmenu = ""
    for index, row in df.iterrows():
        #strmenu = strmenu + "<li><a href='{{ url_for('"+row['MENU']+"') }}'>"+row['MENU']+"</a></li>"
        if row['ONOFF']==1:
            strmenu = strmenu + "<li><a href='"+row['ROUTE']+"'>"+row['MENU']+"</a></li>"
    #print(strmenu)
    return strmenu
def m2(id):
    if _READ == 1 :
        dft = pd.read_excel('covmenu.xlsx', sheet_name='Hoja2')
    if _READ == 2 :
        dft = pd.read_csv(_WEBPATH+'covmenu2.csv')
    #
    dft = dft[(dft['ONOFF'] == 1) & (dft['IDMAIN'] == id)]
    #
    strtitle = ""
    strtext  = ""
    for index, row in dft.iterrows():
        if row['IDMAIN']==id:
            if row['TYPE']=="TEXT":
                if row['TITLE']=="TIT":
                    lvl = row['TITLELEVEL']
                    if lvl>=1:
                        strtitle = str(row['TEXT'])
                        strtext = strtext + "<h"+str(int(lvl))+">" + str(row['TEXT']) + "</h"+str(int(lvl))+">"
                    if lvl==0:
                        strtext = strtext + "<strong>" + str(row['TEXT']) + "</strong>"   
                else:
                    strtext = strtext + "<p>" + str(row['TEXT']) + "</p>"
            if row['TYPE']=="IMG":   
                    # <img src="img.jpg" alt="G" width="500" height="600">
                    strtyle = "width='"+str(row['WIDTH'])+"' height='"+str(row['HEIGHT'])+"'"
                    strtext = strtext + "<p>" + "<img id='img' src='/static/images/" +  str(row['MEDIA']) +"'"+ " " + strtyle +">" + "</p>"
            if row['TYPE']=="VID":   
                    strtyle = "width='"+str(row['WIDTH'])+"' height='"+str(row['HEIGHT'])+"'"
                    #strtext = strtext + "<p>" + "<video width='320' height='240' controls> <source src='/static/images/mywashhands4.mp4' type='video/mp4'> !? </video>" +   "</p>"
                    strtext = strtext + "<p>" + "<video "+strtyle+" controls> <source src='/static/video/"+str(row['MEDIA'])+"' type='video/mp4'> !? </video>" +   "</p>"
            if row['TYPE']=="URL":   
                    strtext = strtext + "<a href='"+str(row['URL'])+"' target='_blank'>"+str(row['TEXT'])+"</a>"

    #print(strmenu)
    return strtitle, strtext    
# - - - - - - - - - - - - - - - - - - - - - 
def fmarquee():
    if _READ == 1 :
        dfi = pd.read_excel('covmenu.xlsx', sheet_name='Hoja2')
    if _READ == 2 :
        dfi = pd.read_csv(_WEBPATH+'covmenu2.csv')
    #
    dfi = dfi[(dfi['TYPE'] == "IMG")]
    #
    path = "/static/images/"
    txtimages = ""
    #listimags = [ "SARS-CoV-2b.jpg","curv1.jpg","curv2.jpg","curv3.jpg","SARS-CoV-2a.jpg" ]
    #for img in listimags:
    for index, row in dfi.iterrows():
        img = str(row['MEDIA'])
        txtimages = txtimages + "<a href='"+path+img+"' target='_blank'><img title='' alt='' src='"+path+img+"' height ='100px' width='100px'/></a>"
    
    textmarquee = "<marquee  scrolldelay='1' scrollamount='2' direction='left' loop='infinite' onmouseout='this.start()' onmouseover='this.stop()'>"
    textmarquee = textmarquee + txtimages + "</marquee>"
    
    return textmarquee
# - - - - - - - - - - - - - - - - - - - - - 


app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello from Flask...1234!'

@app.route("/")
def home():
    textmarquee = fmarquee()
    return render_template("home.html",menu=_STRMENU, marquee = textmarquee)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/id/<int:id>')
def idmenu(id):   
   global _IDMAIN
   _IDMAIN = id
   if _MSG == 1 : print("_IDMAIN id:",_IDMAIN)
   idtitle,iddata = m2(_IDMAIN)
   return render_template("id.html", idtitle=idtitle, iddata=iddata)

setupapp()
_STRMENU = m1()   
if __name__ == "__main__":
    if _RUN == 1 :
        app.run()
    if _RUN == 2 :        
        app.run(debug=True)
    #if _RUN == 0 :
    #    continue
