import re
from piece import Move

def parse():
	char_dict = {
		'a':0,
		'b':1,
		'c':2,
		'd':3,
		'e':4,
		'f':5,
		'g':6,
		'h':7,
	}
	with open("carlsen_games.txt") as f:
	    content = f.readlines()

	long_string = "".join(content).replace("\n"," ")
	long_string = re.split("\d\/?\d?-\d\/?\d?",long_string)
	re_prog = re.compile("[a-z]\d\-[a-z]\d")
	output = []
	for ls in long_string:
	    z = re_prog.findall(ls)
	    output.append(z)

	new_games = [[Move(char_dict[move[0]],int(move[1])-1,char_dict[move[3]],int(move[4])-1) for move in game] for game in output]
	return new_games




