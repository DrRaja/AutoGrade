from flask import Flask,render_template,request
import spacy
import gensim
from spacy.lang.en.stop_words import STOP_WORDS
from gensim.summarization import keywords
from pymongo import MongoClient

app=Flask("__main__")
app.debug=True
nlp = spacy.load('en_core_web_sm')
client=MongoClient('mongodb://localhost:27017')

Solution="Bahria University is student"
Answer="I student Bahria University"

@app.route('/')
def main():
    
    strSol=Solution.split()
    strAns=Answer.split()

    cleanSol=[word for word in strSol if word not in STOP_WORDS]
    cleanAns=[word for word in strAns if word not in STOP_WORDS]

    sol=""
    for word in cleanSol:
        sol+=word
        sol+=" "
    
    ans=""
    for word in cleanAns:
        ans+=word
        ans+=" "

    solution=nlp(sol)
    answer=nlp(ans)

    result=solution.similarity(answer)



    db=client.Autograder
    collection=db.newcollection

    #for inserting the document
    # col={Solution:Answer}
    # temp=collection.insert_one(col)

    #if document is inserted successfully into the collection, then return its object_id
    # if temp.acknowledged:
    #     print (temp.inserted_id)

    #for finding one document in the collection
    # data=collection.find_one()
    # print(data)

    #finding all the documents into the collection
    # data=collection.find()
    # for document in data:
    #     print(document)

    #finding any document based on a filter/condition
    # data=collection.find({
    #     'hello':'world'
    # })
    # for doc in data:
    #     print(doc)

    return render_template('quiz.html',ques="Hello World")

@app.route('/',methods=["GET","POST"])
def newmain():
    ans=request.form["answer"]
    Save=request.form["save"]
    # Next=request.form["next"]
    print(Save)
    return render_template('instructor.html',answer=ans)

@app.route('/instructor')
def func():
    return render_template('instructor.html')

@app.route('/instructor',methods=["GET","POST"])
def funct():
    return render_template('add-marks.html')

@app.route('/add-marks')
def add_marks():
    return render_template('add-marks.html')

# @app.route('/html/website-instructor-course-edit-course',methods=["GET","POST"])
# def student():
#     return render_template('html/website-instructor-course-edit-course.html')





app.run()