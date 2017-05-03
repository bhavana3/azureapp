"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
import pymongo

from flask import Flask,render_template,request,session
from pymongo import MongoClient

import uuid
import base64
import datetime
import os


#client = MongoClient('mongodb://104.154.62.17:27017/')
#db = MongoClient('mongodb://104.154.62.17:27017/').gridfs_example
#fs = gridfs.GridFS(db)
#fs = gridfs.GridFS(client)

#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','jpe','JPG'])


app = Flask(__name__)
app.secret_key="sunitakey"


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.




@app.route('/')
def index():
    client = MongoClient('mongodb://104.154.62.17:27017/')
    if session.get('logged_in')==True:
        
        client.close()
        return render_template('upload.html')
    else:
        client.close()
        return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    client = MongoClient('mongodb://104.154.62.17:27017/')
    user=request.form['username'];
    pwd=request.form['password'];
    users=client.sunitadb.sunitacollection.find_one({"username":user})
    pass1=users['password']

    if str(pass1)==str(pwd):
        session['logged_in']=True
        session['username']=user
        client.close()
        return render_template('upload.html')
    else:
        session['logged_in']=False
        client.close()
        return render_template('login.html')

def allowed_file(filename):
    client = MongoClient('mongodb://104.154.62.17:27017/')
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jpe', 'JPG'])
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



def insert_img(username,post_id,image_data,filename,cmnt,size_in_kb):
    client = MongoClient('mongodb://104.154.62.17:27017/')
    user=session.get('username')
    img_coll = client.sunitadb.images
    post_dict = {}
    post_dict['filename']=filename
    post_dict['username']=username
    post_dict['post_id']=post_id
    encoded_string = base64.b64encode(image_data)
    post_dict['image_data']=encoded_string
    post_dict['post_time']=str(datetime.datetime.now())
    post_dict['comments']=str(cmnt)
    post_dict['size'] = str(size_in_kb)
    output = img_coll.save(post_dict)
    images1=client.sunitadb.comments.insert({"username":user,"filename":filename,"comment":cmnt})
    client.close()
    return str(output)+""+str(cmnt)

@app.route('/upload',methods =['GET','POST'])
def upload():
    client = MongoClient('mongodb://104.154.62.17:27017/')
    cmnt=[]
    
    print 'in upload'
    file = request.files['file']
    comment = request.form['comment']
    size1=os.stat(file.filename).st_size
    size_in_kb=size1/1024
    allowed_size=10000
    allowed_count=20;
    allowed_total_size=100000000
    #cmnt = request.form['comments']
    
    total_size=0

    username=session.get('username')
    #username = "sunita"
    count=client.sunitadb.images.count({'username':username})
    total1=client.sunitadb.images.find({"username":username})
    for total2 in total1:
        total_size=total_size+int(total2['size'])
    #print count
   # if count>=5:
    #    client.close()
     #   return "sorry you cannot upload more files: limit excedded"

    if file and allowed_file(file.filename):
            if size_in_kb<allowed_size and count<allowed_count and (allowed_total_size-total_size)>size_in_kb:
                fname = str(file.filename)
                image_data = open(fname, "rb").read()
                post_id = str(uuid.uuid1())
                output=insert_img(username,post_id,image_data,str(file.filename),comment,size_in_kb)
        #size=os.path.getsize(file)
            else:
                return"you exceed your limit either count , tatal size or the input fileis not valid"
        #print size
    client.close()
    return "success"


@app.route('/delete1/<folder_name>',methods =['GET','POST'])
def delete1(folder_name):
     client = MongoClient('mongodb://104.154.62.17:27017/')
     images1=client.sunitadb.images.remove({"filename":folder_name})
     images2=client.sunitadb.comments.remove({"filename":folder_name})
     client.close()
     return "selected image successfully deleted"



@app.route('/show',methods =['GET','POST'])
def show():
    client = MongoClient('mongodb://104.154.62.17:27017/')
    l=""
    a=[]
    user=session.get('username')
    #images1=client.sunitadb.images.find({"username":user})
    images1=client.sunitadb.images.find()
    for images2 in images1:
        imagename=images2['filename']
        #print "imagesname: "+str(imagename)
        #l=l+"<a href='"+imagename+"' onclick='a()'/>"+imagename+"</a><br>"
        a.append(imagename)
        client.close()
    return render_template('display.html', result=a)
    #return a[0]
	

	@app.route('/display',methods =['GET','POST'])
def display():
    client = MongoClient('mongodb://104.154.62.17:27017/')
    images1=client.sunitadb.images.find()
    imgs=[]
    for images2 in images1:
        imgs.append(images2)
        #imagename=images2['filename']
        #print "imagesname: "+str(imagename)
    for i1 in imgs:
        img1=i1['image_data']
        comments =i1['comments']
        decode = img1.decode()
    return render_template('result.html', result=decode)

@app.route('/comments',methods =['GET','POST'])
def comments():
    client = MongoClient('mongodb://104.154.62.17:27017/')
    print "in comments"
    user=session.get('username')
    cc1=request.form['comment1']
    cc2=request.form['filename1']
    images1=client.sunitadb.comments.insert({"username":user,"filename":cc2,"comment":cc1})
    client.close()
    return "success comments"


@app.route('/imagelist/<folder_name>',methods =['GET','POST'])
def imagelist(folder_name):
    client = MongoClient('mongodb://104.154.62.17:27017/')
    images1=client.sunitadb.images.find({"filename":folder_name})
    imgs=[]
    com1=[]
    user=session.get('username')
    for images2 in images1:
        imgs.append(images2)
        #imagename=images2['filename']
        #print "imagesname: "+str(imagename)
    for i1 in imgs:
        img1=i1['image_data']
        comments =i1['comments']
        decode = img1.decode()
    images1=client.sunitadb.comments.find({"filename":folder_name,"username":user})
    for images2 in images1:
        com1.append(images2['comment'])
    client.close()

    return render_template('comment.html', result=decode,comm=com1,file=folder_name)






@app.route('/logout')
def logout():
    client = MongoClient('mongodb://104.154.62.17:27017/')
    session['logged_in']=False
    client.close()
    return render_template('login.html')



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

if __name__ == "__main__":

    app.run()


