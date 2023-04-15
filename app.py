# importing neccessary libraries
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)


# reading csv file, taking user input and listing the tags
df = pd.read_csv("static/unique.csv")
def combined_features(row):
    return str(row['Title'])+" "+str(row['Description'])+" "+str(row['Author'])

df["combined_features"] = df.apply(combined_features, axis =1)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form['title']
    s=name
    s=s.lower()

    # removing the unneccesary words
    s=s+' ' 
    arr=['books','book','best','recommend','for','in','market','of','seller','by','buy','author','written','show','other','the','me','all','what','are','world','get','rating']
    x=""
    y=""
    for i in range(0,len(s)):
        if(s[i]!=' '):
            x=x+s[i]
        else:
            if(arr.count(x)==0):
                y=y+x+' '
            x=""
    s=y
    df

    # listing the name of the books
    title_arr=list(df["Title"])
    price_arr=list(df["Price"])
    rating_arr=list(df["Rating"])
    author_arr=list(df["Author"])
    url_arr=list(df["LINK"])
    comb_arr=list(df["combined_features"])

    # implementing the Jaccard similarity
    def Jaccard_Similarity(doc1, doc2): 
        
        # List the unique words in a document
        words_doc1 = set(doc1.lower().split()) 
        words_doc2 = set(doc2.lower().split())
        
        # Find the intersection of words list of doc1 & doc2
        intersection = words_doc1.intersection(words_doc2)

        # Find the union of words list of doc1 & doc2
        union = words_doc1.union(words_doc2)
            
        # Calculate Jaccard similarity score 
        # using length of intersection set divided by length of union set
        return float(len(intersection)) / len(union)


    # calling the Jaccard_Similarity for calculating the similarity
    similar=[]
    add=0  # variable to check whether atleast one recommendation is there or not
    for item in comb_arr:
        similar.append(Jaccard_Similarity(item,s))
        jc=Jaccard_Similarity(item,s)
        add=add+jc

    # storing the deatils of each book in an array
    reco=[]
    for i in range(0,len(title_arr)):
        pair=((similar[i],title_arr[i],price_arr[i],author_arr[i],rating_arr[i],url_arr[i]))
        reco.append(pair)

    # printing the recommended books
    l=[]
    ans=[]
    reco.sort(reverse=True)
    count=0
    if add!=0:
        for item in reco:
            if(item[0]>0):
                l=[]
                l.append(item[1])
                l.append(item[3])
                l.append(item[2])
                l.append(item[4])
                l.append(item[5])
                ans.append(l)
                
    ans.sort(key=lambda x:x[3],reverse=True)
    return render_template('index2.html', names=ans, name=name)


if __name__ == "__main__":
    app.run(debug=False)

