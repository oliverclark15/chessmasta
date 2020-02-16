import re
from chess import Move

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
	int_dict = {
		'8':0,
		'7':1,
		'6':2,
		'5':3,
		'4':4,
		'3':5,
		'2':6,
		'1':7
	}
	with open("Adams.txt") as f:
	    content = f.readlines()

	long_string = "".join(content).replace("\n"," ")
	long_string = re.split("\d\/?\d?-\d\/?\d?",long_string)
	re_prog = re.compile("[a-z]\d\-[a-z]\d")
	output = []
	for ls in long_string:
	    z = re_prog.findall(ls)
	    output.append(z)
	print(len(output))
	new_games = [[Move(int_dict[move[1]],char_dict[move[0]],int_dict[move[4]],char_dict[move[3]]) for move in game] for game in output]
	return new_games




