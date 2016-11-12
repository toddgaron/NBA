from flask import Flask, render_template, request, redirect
from requests import get
from simplejson import loads
#from pandas import DataFrame,to_datetime
from dill import load
from dateutil.relativedelta import *
from asteval import Interpreter
from numpy import mean
import pandas as pd
from collections import defaultdict, Counter


app = Flask(__name__)
app.vars = {}
app.players = load(open('scoringChamps','rb'))
app.games = load(open('gameData','rb'))
aeval = Interpreter()

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
	if request.method=='GET':
		return render_template('stockinfo.html')
	else:
		app.vars['Name']=request.form['name']
		print app.vars
		try:
			w =  map(lambda x: aeval(str(x).join(app.vars['Name'].split('%'))), range(100))
			if None in w:
				return render_template('errorpage.html')
			v = playerScoring(app.players, lambda x: w[int(x)])
			u = reScoreSeason(app.games, lambda x: w[int(x)])
			return render_template('outpage.html', name=app.vars['Name'], pts = [[x,y] for x,y in enumerate(w)], players = v, games = u)
		except:
			return render_template('errorpage.html')



def reScoreSeason(games, func, fts=True):
    west = ['GSW','LAC','SAS','HOU','POR','DAL','OKC','PHX','MEM','UTA','SAC','DEN','NOP','LAL','MIN']
    scores = defaultdict(list)
    for i in games:
        s = i.playGame(func, fts)
        #print s
        for j in s:
            scores[j[0]].append(j[1:]) 
	
    newScores = []
    for key in scores.keys():
        newScores.append((key, sum([1 for i in scores[key] if i[0] > 0 ]),
                      sum([1 for i in scores[key] if i[0] < 0]),
                      sum([1 for i in scores[key] if i[0] == 0]),
                      round(mean([i[1] for i in scores[key]]),1),
                      round(mean([i[1]-i[3] for i in scores[key]]),1),
                      round(mean([i[2] for i in scores[key]]),1),
                      round(mean([i[2]-i[4] for i in scores[key]]),1),
                      1 if key in west else 0 ))
    newScores.sort(key= lambda (name, a,b,c,d, e,f,g,h): (h,-a,-c,b, name ,d, e,f,g))

    return newScores


def playerScoring(pts, func, fts = True):
	r = []
	for player,games in pts.iteritems():
		r.append((player,round(mean([sum(map( lambda x: func(x) , i['shot_distance']))+ i['fts'] if fts else 0 for i in games ]),1), round(mean([sum( i['points'] )+ i['fts'] if fts else 0 for i in games ]),1)))
	return sorted(r, key = lambda (i, j, k): (-j, -k, i))





if __name__ == '__main__':
	app.run(port=33507)
