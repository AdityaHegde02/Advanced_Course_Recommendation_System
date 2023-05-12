from flask import Flask, render_template, request, jsonify
import json
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')




app = Flask(__name__)
CORS(app)

df=pd.read_csv('Coursera_500.csv')


skills = set()

for i in range(500):
  temp = df['Skills'][i].split("  ")
  skills.update(temp)

skills = list(skills)

def para_cleaning(para):
    para=para.lower()
    clean_para = re.sub(r'\b\w*\\n\w*\b|[^\w\s]+', '', para)
    clean_para = re.sub(r'[\\\x00-\x1f\x7f]', '', clean_para)
    clean_para = clean_para.replace("\'s", "")
    
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [word for word in clean_para.split() if word.lower() not in stop_words]
    filtered_para =' '.join(filtered_sentence)
    
    words = word_tokenize(filtered_para)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    lemmatized_paragraph = ' '.join(lemmatized_words)
    
    words = word_tokenize(lemmatized_paragraph)
    ps = PorterStemmer()
    stemmed_words = [ps.stem(w) for w in words]
    stemmed_paragraph = " ".join(stemmed_words)
    return stemmed_paragraph


# Cosine similarity function
def cos_sim(s1,s2):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([s1, s2])
    cosine_similarities = cosine_similarity(tfidf[0], tfidf[1]).flatten()

    return cosine_similarities[0]


def course_extract(course_desc):

    course_skill = []

    course_desc = para_cleaning(course_desc)

    print("Loading...")
    for i in skills:
        if(cos_sim(course_desc,i)>0.03):
            course_skill.append(i)
  
    course_rank=[]

    for i in range(500):
        temp = para_cleaning(df['Course Description'][i])
        score = 0
        for j in course_skill:
            score+=cos_sim(temp,j)
            course_rank.append([i,score])

    course_rank.sort(key=lambda x: x[1])
    course_rank = course_rank[::-1]
    data = []
    for i in range(30):
        data.append([df['Course Name'][course_rank[i][0]],df['Course URL'][course_rank[i][0]]])

    return data



@app.route("/") 
def index():
    print("index page")
    return '414 project'

@app.route('/predict')
def predict_courses():
    desc = request.args.get('desc') 
    print(desc)
    # desc = desc.split('-').join(' ')
    print(desc)
    data = course_extract(desc)

    print(data)

    result = {
        "status":"ok",
        "data":data
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)