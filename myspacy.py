from flask import Flask,render_template,request,redirect, url_for
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
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
AnsDoc=[]
Title=""
count=0
collectionName=''
stdColName=""

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

class Database:
    db=client.Autograder
    collection=db.newcollection
    AllCollections=db.list_collection_names()
    CreateName="quiz"+str(len(AllCollections)+1)
    FindName="quiz"+str(len(AllCollections))

    stdDB=client.Student

    def createExam(self,question,solution,marks,title):
        newCollection=self.db[self.CreateName]
        doc={"Question":question,
        "Solution":solution,
        "Marks":marks,
        "Title":title
        }
        addDoc=newCollection.insert_one(doc) 
        return addDoc
    
    def updateCollectionNum(self):
        documents=self.collection.find({},{'collections':1,'_id':0}) #for reading whatever value is stored in the collections column/field
        for doc in documents:
            collecNum=doc['collections']
        if int(collecNum)<len(self.AllCollections):
            self.collection.update_one({
                'collections':collecNum
            },
            {
                '$set':{
                    'collections':str(len(self.AllCollections))
                }
            })
            newQuiz=True
        else:
            newQuiz=False

        return str(newQuiz)

    def AttemptExam(self,dbname):
        global stdColName
        db=client[dbname]
        # documents=self.collection.find({},{'collections':1,'_id':0}) #for reading whatever value is stored in the collections column/field
        # for doc in documents:
        #     collecNum=doc['collections']
        # if int(collecNum)<len(self.AllCollections):
        #     exam=True
        newExam=db[stdColName]
        global AnsDoc
        global Title
        questions=newExam.find()
        for quest in questions:
            AnsDoc.append(Exam(quest['Question'],"",quest['Marks']))
            Title=quest['Title']
        
        return True

    def StudentDatabase(self,stdName):
        collecList=self.db.list_collection_names()
        collecList.remove('newcollection')
        collecList.sort()
        stdDB=client[stdName]
        stdCollecList=stdDB.list_collection_names()
        for collec in collecList:
            if collec not in stdCollecList:
                newcol=stdDB[collec]
                tempdata=self.db[collec].find()
                for data in tempdata:
                    doc={
                        "Question":data['Question'],
                        "Marks":data['Marks'],
                        "Title":data['Title'],
                    }
                    result=newcol.insert_one(doc)
        
        return result
    
    def StudentNewExam(self,dbName):
        stdDB=client[dbName]
        collecList=stdDB.list_collection_names()
        new=[]
        for collec in collecList:
            count=stdDB[collec].find_one({"Answer":{'$exists':False}})
            if count!=None:
                new.append(collec)
        return new

    
    def getCollectionNames(self):
        names=self.db.list_collection_names()
        return names
    
    def getExamData(self,dbname):
        collection=self.db[dbname]
        data=collection.find({})
        mylist=[]
        for d in data:
            mylist.append(d)
        return mylist
    
    def StudentAnswer(self,dbname,question,answer,title):
        collection=self.stdDB[dbname]
        doc={
            "Question":question,
            "Answer":answer,
            "Title":title,
            "Exam":dbname
        }
        result=collection.insert_one(doc)
        return result
    
    def AddAnswer(self,dbname,colname,question,answer):
        db=client[dbname]
        coll=db[colname].update({
            'Question':question
        },
        {
            '$set':
            {
                'Answer':answer

            }
        })



        
        

    
    



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

    
    # obj = Database()
    # value=obj.StudentDatabase("Student")
    # print(str(value))
    # value=obj.StudentNewExam("Student")
    # print(value)


    # for doc in AnsDoc:

    # db=client.Autograder
    # temp=db.list_collection_names()
    # print(str(temp) +"  "+ "quiz"+str(len(temp)))

    # collection=db.newcollection

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

    # return redirect(url_for('quiz'))
    
    return redirect(url_for('student_exams'))

@app.route('/student-exams')
def student_exams():
    obj=Database()
    newList=obj.StudentNewExam("Student")
    return render_template('student-exams.html',listi=newList)

@app.route('/student-exams',methods=["GET","POST"])
def student_exam():
    global stdColName
    name=request.form["open"]
    stdColName=name.strip()
    obj=Database()
    obj.AttemptExam("Student")
    return redirect(url_for('quiz'))

@app.route('/instructor')
def instructor():
    global Title
    return render_template('instructor.html',titleValue=Title)

@app.route('/instructor',methods=["GET","POST"])
def instruct():
    dbObj=Database()
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
        for doc in ExamDoc:
            dbObj.createExam(doc.Question,doc.Solution,doc.Total_Marks,Title)
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
    global count
    global AnsDoc
    doc=AnsDoc[count]
    return render_template('quiz.html',ques=doc.Question,num=str(count+1),marks=doc.Total_Marks,total=str(len(AnsDoc)))

@app.route('/quiz',methods=["GET","POST"])
def funct():
    global count
    global AnsDoc
    global stdColName
    Answer=request.form["answer"]
    print(Answer)
    obj=Database()
    doc=AnsDoc[count]
    obj.AddAnswer("Student",stdColName,doc.Question,Answer)
    btnPress=request.form["button"]
    if btnPress=="next":
        if count==(len(AnsDoc)-1):
            return redirect(url_for('add_mark'))
        else:
            count+=1
            return redirect(url_for('quiz'))
    else:
        return redirect(url_for('add_mark'))


    # print(Answer)
    # return "<h1>Successfully Added</h1>"

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

@app.route('/instructor-exams')
def instructor_exams():
    obj=Database()
    name=obj.getCollectionNames()
    return render_template('instructor-exams.html',listi=name)

@app.route('/instructor-exams',methods=["GET","POST"])
def examsfunc():
    global collectionName
    collectionName=request.form["open"]
    return redirect(url_for('exam_questions'))

@app.route('/exam-questions')
def exam_questions():
    global collectionName
    obj=Database()
    data=obj.getExamData(collectionName.strip())
    titles=data[0]['Title']
    return render_template('exam-questions.html',title=titles,documents=data)



app.run()