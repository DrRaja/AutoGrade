from flask import Flask
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
app=Flask("__main__")
app.debug=True
nlp=spacy.load('en_core_web_sm')



@app.route('/')
def main():
    Solution="i am a girl"
    Answer="i am a woman"
    marks=5

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

    sim=solution.similarity(answer)
    result=sim*marks
    print("%.2f" % result)

    return str(result)

    

  






app.run()