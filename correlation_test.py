import pygame as pg
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
import numpy as np
import ngram_call
import random as rand
from datetime import datetime
import sys
import time


WIDTH = 1000
HEIGHT = 680
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (7, 114, 105)
GREEN = (34,139,34)


class Player:
	def __init__(self, name):
	    self.name = name
	    self.score = 0
	    self.points = []
	    self.points_count = 0
	    self.done = False


class Button:
	def __init__(self,box_type,color,x,y,w,h):
	    self.type = box_type
	    self.clicked = False
	    self.rect = pg.Rect(x,y,w,h)
	    self.color = color
	    self.text = ""
	    self.enter = False
	    self.push_count = 0

	def handle(self,event, outside=False):
	    if pg.mouse.get_pressed()[0]:
	        self.clicked = True
	    if (event.type == pg.MOUSEBUTTONUP and self.type == "draw" and gamestart) or (self.type == "draw" and gamestart and outside):
	        self.clicked = False
	        # remove duplicate x axis points (make it a function!)
	        curr_player.points = interpolate_new(points, curr_player.points_count)
	        curr_player.points.sort(key=lambda x: x[0])
	        pg.draw.rect(screen, WHITE, pg.Rect(plot_box.rect.x+5 , plot_box.rect.y+5, plot_box.rect.w-7, plot_box.rect.h-7))

	    if self.clicked:
	        if self.type == "text":
	            self.color = BLUE
	            if event.type == pg.KEYDOWN:
	                if event.key == pg.K_RETURN:
	                    self.enter = True
	                    self.clicked = False
	                    self.cover()
	                if event.key == pg.K_BACKSPACE:
	                    self.text = self.text[:-1]
	                self.text += event.unicode
	                self.cover()
	        
	        if self.type == "button":
	            # cover done box, new game, etc.
	            if pg.mouse.get_pressed()[0]:
	                self.push_count = self.push_count + 1
	        
	        if self.type == "draw":
	            if event.type != pg.MOUSEMOTION and gamestart:
	                curr_player.points_count = len(points)
	            if event.type == pg.MOUSEMOTION and gamestart:
	                points.append(event.pos)

	    if not self.clicked:
	        if self.type == "text":
	            self.color = BLACK
	        if event.type == pg.KEYDOWN and self.type == "draw":
	            if event.key == pg.K_c:
	                curr_player.points.clear()
	                screen.fill(WHITE)
	                draw_dates()

	# more text stuff? maybe cursor blinking!
	def cover(self):
	    #cover up box, by overlaying smalller white box
	    pg.draw.rect(screen, WHITE, pg.Rect(self.rect.x+1 , self.rect.y, self.rect.w-1, self.rect.h-1))
	    if not self.enter:
	        text_surface = font.render(self.text, True, BLACK)
	        screen.blit(text_surface, (self.rect.x+10, self.rect.y+10))
	    pg.display.update(self.rect)


# general UI text blitting (using pygame's but making useful)
def text_blit(location, text, surf, box):
	x = location[0]
	y = location[1]
	text_w , text_h = smallfont.size(text)
	screen.blit(surf, (box.rect.x+x, box.rect.y-y))
	pg.display.update(pg.Rect(box.rect.x+x, box.rect.y-y, text_w, text_h))


# redraw game text
def draw_dates():
	# draw min, max data vals, min max dates, and middle date
	# any text added to game later can be drawn here too
	text_blit([10,20],date1,date1surf,plot_box)
	text_blit([plot_box.rect.w,20],date1,date2surf,plot_box)
	text_blit([(plot_box.rect.w)/2,20],middate,middatesurf,plot_box)
	# x buffer from plot box more for scientific notation numbers
	if len(min_val) > 3 or len(max_val) > 3:
	    buffer = (4)*len(min_val)
	else:
	    buffer = (2)*len(min_val)
	text_blit([-40-buffer,-plot_box.rect.h+30],min_val,minsurf,plot_box)
	text_blit([-40-buffer,-10],max_val,maxsurf,plot_box)
	# cover old plotting name
	pg.draw.rect(screen, WHITE, pg.Rect(plot_box.rect.x+10,plot_box.rect.y+290,240,30))
	pg.display.update(pg.Rect(plot_box.rect.x+10,plot_box.rect.y+290,240,30))
	text_blit([10,-290],"[" +curr_player.name+" please plot]",namesurf,plot_box)
	text_blit([10,-320],"Hover over plotting and press c to clear all points",clearsurf,plot_box)
	# cover old question
	#pg.draw.rect(screen, WHITE, pg.Rect(plot_box.rect.x+10,plot_box.rect.y-60,740,30))
	#pg.display.update(pg.Rect(plot_box.rect.x+10,plot_box.rect.y-60,740,30))
	text_blit([10,60],ques,quessurf,plot_box)


# redraw score section
def draw_scores():
	# blit white rectangle over area
	pg.draw.rect(screen, WHITE, pg.Rect(770,130,140,150))
	# blit banner
	screen.blit(score_banner, (780,140))
	pg.draw.line(screen, BLACK, (780,165), (785+90,165), 2)
	# then for each player in players, blit score
	for i in range(len(players)):
	   p = players[i]
	   surf = smallfont.render(p.name+"  "+str(round(p.score,3)), True, BLACK)
	   screen.blit(surf, (760, 180+i*30))
	pg.display.update(pg.Rect(760,130,50,(len(players)*30)+5))


# given the turn, get the question data
def get_this_question():
	ques  = list(questions[which_ques].keys())[0]  
	data = questions[which_ques][ques][0]
	# get the dates/range players wil plot over
	date1 = str(questions[which_ques][ques][1])
	date2 = str(questions[which_ques][ques][2])
	if len(date1) > 4:
	    kind = "trend"
	else:
	    kind = "ngram"
	middate = half_date(kind,date1,date2)
	max_val = str(max(data))
	min_val = str(min(data))
	max_val, min_val = check_vals(min_val,max_val)
	return ques, data, date1, date2, middate, min_val, max_val


# for the data of this round's question, render surfs to blit
def get_surfs():
	date1surf = smallfont.render(date1, True, BLUE)
	date2surf = smallfont.render(date2, True, BLUE)
	middatesurf  = smallfont.render(middate, True, BLUE)
	minsurf = smallfont.render(min_val, True, BLUE)
	maxsurf = smallfont.render(max_val, True, BLUE)
	quessurf = smallfont.render(ques,True, GREEN)
	namesurf = smallfont.render("[" +curr_player.name+" please plot]",True,BLACK)
	return date1surf, date2surf, middatesurf, minsurf, maxsurf, quessurf, namesurf


# check a given players points, and return the "closeness" = total squared deviation
def score(draw_points, min_val, max_val, data):
	points = []
	for i in range(len(draw_points)):
	    points.append([i,draw_points[i][1]])

	max_y_point = max(points, key=lambda x: (x[1]))[1]
	max_x_point = max(points, key=lambda x: (x[0]))[0]
	pointsy = []
	pointsx = []
	for i in range(len(points)):
	    fixed_y = abs((plot_box.rect.y+plot_box.rect.h)-points[i][1])  # first adjust for opposite pygame y coords
	    pointsy.append(fixed_y*(max(data))/(max_y_point))  # then scale to data
	    pointsx.append(i*(len(data))/max_x_point)

	datax = list(range(len(data)))
	# build 1-D interpolating functions
	fplayer = interp1d(pointsx, pointsy)
	fdata = interp1d(datax,data)
	
	# now align the x space and interpolate
	fill = 100
	xp = np.linspace( min(pointsx), max(pointsx), num = fill) 
	xd = np.linspace( min(datax), max(datax), num = fill) 
	datanew = fdata(xd) 
	playernew = fplayer(xp) 
	
	# calc total squared deviation, point by point (they now match this way!)
	squared_dist = 0
	furthest = (min(datanew) - max(datanew))**2
	for i in range(len(datanew)):
	    squared_dist = squared_dist + ((playernew[i] - datanew[i])**2)/furthest
	#plt.scatter(xd,datanew, color="blue")
	#plt.scatter(xp,playernew, color="red", s=.5)
	#plt.show()
	return squared_dist


# for new points overlaying old, replace with fair interpolation
def interpolate_new(points, old_count):
	new_points = points[old_count:]
	old_points  = points[:old_count]
	xs = []
	ys = []
	remove_list = []
	# remove old points that overlap by x values
	if len(new_points) > 0:
	    min_x = min(new_points, key=lambda x: (x[0]))[0]
	    max_x = max(new_points, key=lambda x: (x[0]))[0]
	    for i in range(len(old_points)):
	        if old_points[i][0] > min_x and old_points[i][0] < max_x:
	            remove_list.append(old_points[i])
	    for point in remove_list:
	        old_points.remove(point)

	for i in range(len(new_points)):
	    if new_points[i][0] not in xs:
	        xs.append(new_points[i][0])
	        ys.append(new_points[i][1])
	
	if len(xs) > 1:
	    f = interp1d(xs, ys)  # this is now interpolation function for new addition
	    new_ys = f(xs)
	    new_points = []
	    for i in range(len(xs)):
	        new_points.append([xs[i],new_ys[i]])
	return old_points+new_points


# build the str that is the question to ask
def build_question(kind, kind_return):
	if kind == "ngram":
	    min_year = kind_return[0]
	    max_year = kind_return[1]
	    word = kind_return[2]
	    question = "Plot the frequency of the term "+str(word)+" in US books"
	if kind == "trend":
	    date_range = kind_return[0]+ " "+kind_return[1]
	    word = kind_return[2]
	    question = "Plot the popularity of the term "+str(word)+" in Google searches"
	return question


# return string of halfway between different date types
def half_date(kind,date1,date2):
	if kind == "trend":
	    a = datetime(int(date1[:4]), int(date1[5:7]), int(date1[8:]))
	    b = datetime(int(date2[:4]), int(date2[5:7]), int(date2[8:]))
	    return str(a + (b - a)/2)[:10]
	if kind == "ngram":
	    mid = int((int(date2) + int(date1))/2)
	    return str(mid)


# make small min,max vals suitable for drawing
def check_vals(min_val,max_val):
	replace_min = min_val
	replace_max = max_val
	if "e" in min_val:
	    e_index = min_val.index("e")
	    replace_min = min_val[0]+min_val[e_index:]
	if "e" in max_val:
	    e_index = max_val.index("e")
	    replace_max = max_val[0]+max_val[e_index:]
	# cover small but not scientific vals
	if float(min_val) < .1 and float(min_val) > 0 and "e" not in min_val:
	    replace_min = "{:.2e}".format(float(min_val))
	if float(max_val) < .1 and float(max_val) > 0 and "e" not in max_val:
	    replace_max = "{:.2e}".format(float(max_val))
	return replace_max,replace_min


pg.init()
pg.display.set_caption('Match the Trend!')
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# coordinates of box to drawn in, 600 by 280 (last args are w,h)

plot_box = Button("draw", BLACK, 100, 135, 600, 280)
plot_box.enter = True

# coordinates of input box to enter names and guesses into

done_box = Button("button", BLACK, 750, 380, 200, 50)

boxes = [done_box,plot_box]

# variable initialization

players = []
names = []  # purely for directing guessing
round_scores = []
num_turns = 3
quit = False
overall_count = 0   # will track game progression
which_ques = 0

# get vals from args
num_players = len(sys.argv)
for i in range(1,num_players):
	players.append(Player(sys.argv[i]))

# fonts

bigfont = pg.font.SysFont('couriernew', 26, bold=True)
font = pg.font.SysFont('couriernew', 20, bold=True)
smallfont  = pg.font.SysFont('couriernew', 18, bold=False)
tinyfont = pg.font.SysFont('couriernew', 12, bold=False)

# request question data
# here, set up list of lists, list of data sets!
# by rand num choose ngram or trends, call that script, return data set, store
questions = []
for i in range(num_turns):
	r = rand.randint(1,1)
	if r != 2:
	    ngram_return = ngram_call.get_data()
	    data = ngram_return[3]
	    date1 = ngram_return[0]
	    date2 = ngram_return[1]
	    questions.append({build_question("ngram", ngram_return): [data,date1,date2]})

gamestart = True
points = []
plot_box.clicked = False
curr_player = players[0]
screen.fill(WHITE)

# set up data for this question, which is the first
ques, data, date1, date2, middate, min_val, max_val = get_this_question()

# set up blit text surfs
date1surf, date2surf, middatesurf, minsurf, maxsurf, quessurf, namesurf = get_surfs()
score_banner = bigfont.render("SCORES",True,BLUE)
clearsurf = smallfont.render("Hover over plotting and press c to clear all points",True,BLACK)

while not quit:
	# once whole game over
	if which_ques == num_turns:
	    sys.exit()
	old_name = curr_player.name
	# pick player
	done_count = 0
	for i in range(len(players)):
	    p = players[i]
	    if p.done == False:
	        curr_player = p
	        break
	    else:
	        done_count = done_count + 1

	if old_name != curr_player.name:
	    # update if new player
	    date1surf, date2surf, middatesurf, minsurf, maxsurf, quessurf, namesurf = get_surfs()
	    draw_dates()
	
	# check if round over
	if done_count == len(players):
	    # best score: min(round_scores, key=lambda x: (x[1])) )
	    round_scores = []
	    which_ques = which_ques + 1
	    # if the game isnt over, get the next question data
	    if which_ques < num_turns:
	        curr_player = players[0]
	        ques, data, date1, date2, middate, min_val, max_val = get_this_question()
	        date1surf, date2surf, middatesurf, minsurf, maxsurf, quessurf, namesurf = get_surfs()
	        for p in players:
	            p.done = False
	            p.points = []
	        screen.fill(WHITE)
	        draw_dates()
	        # upate score blit
	        draw_scores()

	# if the first turn, set up
	if overall_count == 0:
	    plot_box.clicked = False
	    draw_dates()
	    pg.display.update()

	# now deal with game element interaction
	mouse_pos = pg.mouse.get_pos()
	for event in pg.event.get():
	    if event.type == pg.QUIT:
	        quit = True
	    for box in boxes:
	        if box.rect.collidepoint(mouse_pos):
	            box.handle(event)
	        else:
	            if box.type == "draw" and box.clicked == True:
	                box.handle(event, outside=True)

	points = curr_player.points
	
	if done_box.push_count > 0:
	    curr_player.done = True
	    this_score = score(curr_player.points, min_val, max_val, data)
	    curr_player.score = curr_player.score + this_score
	    round_scores.append([curr_player.name, this_score])
	    plot_box.cover()
	    done_box.push_count = 0
	    #draw_dates()  # WILL CHANGE SINCE REDRAWING OF DATES DEPENDS ON NEXT QUES !!

	# general drawing calls
	pg.draw.rect(screen, done_box.color, done_box.rect)
	pg.draw.rect(screen, plot_box.color, plot_box.rect, 3)
	# now draw current points
	if not curr_player.done:
	    for i in range(len(curr_player.points)):
	        curr_point = curr_player.points[i]
	        # try drawing lines, save for where its too wide
	        if i != len(curr_player.points) - 1:
	            next_point = curr_player.points[i+1]
	            if abs(next_point[0]- curr_point[0]) >= 30 or abs(next_point[1]- curr_point[1]) >= 30:  # MIGHT NEED ADJUSTING!!
	                continue
	            else:
	                pg.draw.line(screen, BLACK, curr_point, next_point, 2)

	pg.display.update()
	clock.tick(120)
	overall_count = overall_count +  1