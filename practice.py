from flask import Flask
app=Flask("__main__")
app.debug=True



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

    l=[]
    l.append(Exam("Hello","World","10"))
    l.append(Exam("I","Am","9"))
    l.append(Exam("Rabia","Shah","8"))
    l[0].question="Hello I am changed"

    return str(len(l))






app.run()