"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
#import pymongo
#import gridfs
from flask import Flask,render_template,request,session, send_file
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
#import csv
import os

from plotly.offline import plot
from plotly.graph_objs import Scatter

#from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
#from sklearn.preprocessing import scale
#
#np.random.seed(42)
#
#digits = load_digits()
#data = scale(digits.data)
#
#print(data)
#read from the csv file and return a Pandas DataFrame. - code referred from given document


app = Flask(__name__)
app.secret_key="Bhavana secret key"

# "Position (pos)" is the class attribute we are predicting - code referred from given document

#The dataset contains many attributes 
#We know that sokme of them are not useful for classification and thus do not 
#include them as features. 
#===========code referred from given document=============
#feature_columns = ['Age', 'MP', 'FG', 'FGA', '3P', '3PA', \
#    '2P', '2PA', '2P%', 'eFG%', 'FT%', 'ORB', 'DRB', \
#    'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PS/G']
    

@app.route('/')
def index():
    return render_template('index.html')
        

@app.route('/upload',methods =['GET','POST'])
def upload():
    print("inside Upload")
    file = request.files['myfile']
    print("here")
    print(file.filename)
    nba_stats = pd.read_csv(file.filename)
    print("check-1")
    feature_columns = request.form['attributes']
    print("check-2")
    clusters = request.form['clustercount']
    print("check-3")
    col = str.split(feature_columns)
    print(col)
    nba_feature = nba_stats[col]
    #Pandas DataFrame allows you to select columns. 
    #We use column selection to split the data into features and class.
    #===========code referred from given document=============
#    nba_feature = nba_stats[feature_columns]
    print("check-4")
    reduced_data = PCA(n_components=2).fit_transform(nba_feature)
    print("check-5")
   
    k_means = KMeans(n_clusters=int(clusters))
    k_means.fit(reduced_data)
    
    centroids=k_means.cluster_centers_
    labels= k_means.labels_
    
    print(centroids)
    print(labels)

    plt.scatter(centroids[:,0],centroids[:,1],marker="x",s=150,linewidths=5,zorder=10)
    
    plt.show()
    img = plot([Scatter(x=centroids[:,0], y=centroids[:,1])],output_type='div')
#    img.show()
#    return render_template('show.html', div_placeholder=my_plot_div)
    return render_template('show.html', title=Markup(img))
#    return send_file(img)
    
#@app.route('/fig/<img>')
#def fig(img):
##    fig.savefig(img)
##    img.seek(0)
#    return send_file(img)
    
if __name__ == "__main__":
    
    app.run()