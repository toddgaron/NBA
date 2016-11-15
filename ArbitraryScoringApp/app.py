from flask import Flask, render_template, request, redirect
#from pandas import DataFrame,to_datetime
from dill import load
from asteval import Interpreter
from numpy import mean, inf
from collections import defaultdict, Counter


app = Flask(__name__)
app.vars = {}
app.vars['scoring prob'] = [[0, 0.8437591992934943], [1, 0.6227063044592517], [2, 0.5439440106646353], [3, 0.4285026480500722], [4, 0.37752769474239495], [5, 0.3896667323999211], [6, 0.3950091296409008], [7, 0.40369393139841686], [8, 0.39677744209466265], [9, 0.41600227790432803], [10, 0.39260830051499546], [11, 0.403338898163606], [12, 0.4000619770684847], [13, 0.4083076923076923], [14, 0.4118663594470046], [15, 0.4085207100591716], [16, 0.40458309262468706], [17, 0.40657894736842104], [18, 0.39879062736205595], [19, 0.4022117860930162], [20, 0.3993319725366487], [21, 0.38645635028555886], [22, 0.38565368299267255], [23, 0.383383253027738], [24, 0.36440859447498036], [25, 0.3603967304625199], [26, 0.34375875268415645], [27, 0.3332474890548545], [28, 0.32034294621979736], [29, 0.2737306843267108], [30, 0.25252525252525254], [31, 0.19791666666666666], [32, 0.125], [33, 0.18181818181818182], [34, 0.08823529411764706], [35, 0.11538461538461539], [36, 0.06060606060606061], [37, 0.037037037037037035], [38, 0.14705882352941177], [39, 0.0], [40, 0.08888888888888889], [41, 0.14634146341463414], [42, 0.0], [43, 0.047619047619047616], [44, 0.1], [45, 0.05], [46, 0.05263157894736842], [47, 0.043478260869565216], [48, 0.043478260869565216], [49, 0.1], [50, 0.0]]

app.players = load(open('scoringChamps','rb'))
app.games = load(open('gameData','rb'))

aeval = Interpreter()

#examples loaded when we reload scoringinfo.html. The entries are [Text, Function, Free Throws (where 1 is "yes" and 2 is "no")].
app.examples = [["Only Two Pointers", "2",1], ["A Thirty Foot Four Point Line", "2 if % < 23 else 3 if % < 30 else 4", 1 ],["The Knicks are the First Seed in the East", "-2*exp(-%) + log(1+%)", 1 ], ["The Kings are the First Seed in the West", "2 if 3 <= % <= 5 else 0", 2]]


@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
	if request.method=='GET':
	
		return render_template('scoringinfo.html', examples = app.examples)
		
	else:
	
		app.vars['Name'] = request.form['name'].strip()
		app.vars['Fts'] = bool(request.form['inlineRadioOptions'])

		try:
			
			#we take your function and evaluate it
			w =  map(lambda x: aeval(str(x).join(app.vars['Name'].split('%'))), range(100))
			
			#check if there are any infinities or Nones
			if None in w or -inf in w or inf in w:
				return render_template('errorpage.html', message ='Please enter a function that doesn\'t diverge.')
			
			v = playerScoring(app.players, lambda x: w[int(x)], app.vars['Fts'])
			u = reScoreSeason(app.games, lambda x: w[int(x)], app.vars['Fts'])
			z = map(lambda (i,j): [j[0], i*j[1]], zip(w, app.vars['scoring prob']))
			
			return render_template('outpage.html', name=app.vars['Name'], pts = [[x,y] for x,y in enumerate(w)][:51], players = v, games = u, expected = z, fts = app.vars['Fts'])
			
		except:
			return render_template('errorpage.html', message = 'Something\'s wrong')



def reScoreSeason(games, func, fts=True):
	'''
	Each game is in an object with a playGame method which rescores the game accoring to a function
	'''
    west = ['GSW','LAC','SAS','HOU','POR','DAL','OKC','PHX','MEM','UTA','SAC','DEN','NOP','LAL','MIN']
    scores = defaultdict(list)
    for i in games:
        s = i.playGame(func, fts)
        #print s
        for j in s:
            scores[j[0]].append(j[1:]) 
	
	#consolidates each game and returns summary stats
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
	'''
	The players are a dictionary of dictionaries where each dictionary are their stats of that game. We calculate a few summary stats and return the sorted list
	'''
	r = []
	for player,games in pts.iteritems():
		r.append((player,round(mean([sum(map( lambda x: func(x) , i['shot_distance']))+ (i['fts'] if fts else 0) for i in games ]),1),\
		round(mean([sum( i['points'] )+ (i['fts'] if fts else 0) for i in games ]),1),\
		round(1.*sum(reduce(lambda x,y: x+y, [ map( lambda x: func(x) , i['shot_distance'])  + [(i['fts'] if fts else 0)]  for i in games ]))/sum([i['shots'] for i in games] ),2),\
		round(1.*sum(reduce(lambda x,y: x+y, [ i['points'] + [(i['fts'] if fts else 0)]  for i in games ]))/sum([i['shots'] for i in games] ),2)
		))
	return sorted(r, key = lambda (i, j, k, l, m): (-j, -k, i, l, m))

# + [(i['fts'] if fts else 0)]

@app.errorhandler(404)
def error(e):
	return render_template('errorpage.html',message='Something\'s wrong.')
	
@app.errorhandler(500)
def error(e):
	return render_template('errorpage.html',message='Something\'s wrong.')

if __name__ == '__main__':
	app.run(port=33507)
