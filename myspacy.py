from flask import Flask,render_template,request,redirect, url_for
import spacy
import gensim
from spacy.lang.en.stop_words import STOP_WORDS
from gensim.summarization import keywords
from pymongo import MongoClient

app=Flask("__main__")
app.debug=True
nlp = spacy.load('en_core_web_sm')
client=MongoClient('mongodb://localhost:27017')

Total_Marks=""
Question=""
Solution="Bahria University is student"
Answer="I student Bahria University"

ExamDoc=[]
Title=""

class Exam:
    Question=""
    Solution=""
    Total_Marks=""
    count=0

    def __init__(self,question,solution,total_marks):
        self.Question=question
        self.Solution=solution
        self.Total_Marks=total_marks
        Exam.count+=1

    def print(self):
        string=self.Question+"  "+self.Solution+"   "+self.Total_Marks+"    "
        return string

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

    return redirect(url_for('instructor'))

@app.route('/instructor')
def instructor():
    global Title
    return render_template('instructor.html',titleValue=Title)

@app.route('/instructor',methods=["GET","POST"])
def instruct():
    global Title
    Title=request.form["title"]
    Question=request.form["quest"]
    Solution=request.form["solution"]
    Total_Marks=request.form["marks"]
    global ExamDoc
    btnRequest=request.form["button"]
    if btnRequest=="save":
        ExamDoc.append(Exam(Question,Solution,Total_Marks))
        print(len(ExamDoc))
        print(str(ExamDoc[len(ExamDoc)-1].Question))
        return redirect(url_for('add_mark'))
    else:
        ExamDoc.append(Exam(Question,Solution,Total_Marks))
        return redirect(url_for('instructor'))
        

@app.route('/', methods=["GET","POST"])
def newmain():
    global Question
    Question=request.form["quest"]
    print(Question)
    global Solution
    Solution=request.form["solution"]
    print(Solution)
    Save=request.form["button"]
    # Next=request.form["next"]
    print(Save)
    return redirect(url_for('add_marks'))

@app.route('/quiz')
def quiz():
    global Question
    return render_template('quiz.html',ques=Question)

@app.route('/quiz',methods=["GET","POST"])
def funct():
    global Answer
    Answer=request.form["answer"]
    print(Answer)
    return "<h1>Successfully Added</h1>"

@app.route('/add_marks')
def add_mark():
    return render_template('add-marks.html')

@app.route('/add_marks',methods=["GET","POST"])
def get_marks():
    global Total_Marks
    Total_Marks=request.form["marks"]
    print(Total_Marks)
    global Question
    return redirect(url_for('quizfunc'))

# @app.route('/html/website-instructor-course-edit-course',methods=["GET","POST"])
# def student():
#     return render_template('html/website-instructor-course-edit-course.html')





app.run()