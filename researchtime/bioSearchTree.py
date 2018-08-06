import re
from flask import url_for
dic={}
def addWord(word):
	tDic=dic
	for n in range(len(word)+1):
		prtW=word[:n] 
		if(prtW in tDic.keys()):
			tDic=tDic[prtW]
		else:
			tDic[prtW]={}
			tDic=tDic[prtW]

testArr=[]
lines=open(url_for("static", filename="biology_terms.txt")).readlines()
for i in range(len(lines)):
	lines[i]=lines[i].strip()

for i in range(len(lines)):
	if i==0:
		addWord(lines[i])
		testArr.append(lines[i])
	elif lines[i-1]=="":
		a=re.search(r"\(.*\)",lines[i])
		if a is not None:
			word1=lines[i][:a.start()-1]
			word2=lines[i][a.start()+1:a.end()-1]
			addWord(word1)
			addWord(word2)
			testArr.append(word1)
			testArr.append(word2)
		else:
			b=re.search(r"pl\.",lines[i])
			if b is not None:
				word1=lines[i][:b.start()-1]
				word2=lines[i][b.end()+1:]
				addWord(word1)
				addWord(word2)
				testArr.append(word1)
				testArr.append(word2)
			else:
				addWord(lines[i])
				testArr.append(lines[i])

dic=dic[""]
#print(testArr)

def wordMatch(word):
	tDic=dic
	for n in range(1,len(word)+1):
		if word[:n] in tDic.keys():
			tDic=tDic[word[:n]]
		else:
			return False
	return True

def retList():
	global testArr
	plurals=[]
	for term in testArr:
		plurals.append(term+"s")
		plurals.append(term+"es")
	testArr=testArr+plurals
	return testArr
	
'''
print(wordMatch("al;skdfj;l"))
print(wordMatch("abscission"))
print(wordMatch("independent variable"))
print(wordMatch("bless"))
print(wordMatch("AMP"))
'''
