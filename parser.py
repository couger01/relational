# coding=UTF-8
# Relation
# Copyright (C) 2008  Salvo "LtWorf" Tomaselli
# 
# Relation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>
def parse(expr):
	'''This function parses a relational algebra expression, converting it into python, 
	executable by eval function to get the result of the expression.'''
	symbols=("σ","π","ρ")
	
	expr=expr.strip()
	
	
	start=-1
	#Parses the string from end to begin
	for i in range(len(expr),-1,-1):
		if expr[i:i+1]=="(":
			start=i+1
			break
	
	if start==-1: #No complex operators
		return parse_op(expr)
	end=expr.find(")",start)
	
	internal=parse(expr[start:end])
	print "Internal: %s" % (internal)
	
	endp=start-1
	start=-1
	symbol=""
	for i in range(endp,-1,-1):
		if expr[i:i+2] in symbols:
			symbol=expr[i:i+2]
			start=i+2
			break
	parameters=parse(expr[start:endp])
	print "Parameters: %s"% ( parameters)
	
	res=""
	if symbol=="π":#Projection
		params=""
		count=0
		for i in parameters.split(","):
			if count!=0:
				params+=","
			else:
				count=1
			params+="\"%s\"" % (i.strip())
			
		res="%s.projection(%s)" % (internal,params)
	elif symbol== "σ": #Selection
		res="%s.selection(\"%s\")" % (internal,parameters)
	elif symbol=="ρ": #Rename
		params=parameters.replace(",","\",\"").replace("➡","\",\"")
		res="%s.rename(\"%s\")" % (internal,params)
	print res
	res= ("%s%s%s") % (expr[0:start-2],res.replace(" ",""),expr[end+1:])
	print res
	return parse_op(res)
	#Selection σage > 25 Λ rank = weight(A)
	#Projection Q ᐅᐊ π a,b(A) ᐅᐊ B
	#Rename ρid➡i,name➡n(A)
	#ρid➡i,name➡n(π a,b(A))
	#A ᐅᐊ B
	
	
	
def parse_op(expr):
	'''This function parses a relational algebra expression including only operators 
	(not functions) and no parenthesis, converting it into python, 
	executable by eval function to get the result of the expression.'''
	
	result=""
	symbols={}
	symbols["*"]=".product(%s)"
	symbols["-"]=".difference(%s)"
	symbols["ᑌ"]=".union(%s)"
	symbols["ᑎ"]=".intersection(%s)"
	symbols["ᐅᐊ"]=".join(%s)"
	symbols["ᐅᐊLEFT"]=".outer_left(%s)"
	symbols["ᐅᐊRIGHT"]=".outer_right(%s)"
	symbols["ᐅᐊFULL"]=".outer(%s)"
	
	tokens=expr.split(" ")
	
	i=0;
	tk_l=len(tokens)
	while i<tk_l:
		if tokens[i] not in symbols:
			result+=tokens[i]
		else:
			
			result+=symbols[tokens[i]] % (tokens[i+1])
			i+=1
		i+=1
	return result
		
if __name__=="__main__":
	while True:
		e=raw_input("Expression: ")
		print parse(e)
	