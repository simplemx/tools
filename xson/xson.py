#! /usr/bin/env python
#coding=utf-8

symbol_colon = 1
symbol_comma = 0
symbol_open_bracket = 2
symbol_close_bracket = 3
symbol_double_quote = 4
symbol_single_quote = 5
symbol_array = [',',':','[',']','"','\'']

class Token():
	def __init__(self, b, e):
		self.begin = b
		self.end = e
	def printContent(self, content):
		print content[self.begin : self.end]
	def getContent(self, content):
		return content[self.begin : self.end]
	
class TextToken(Token):
	pass

class SymbolToken(Token):
	def __init__(self, b, e, t):
		Token.__init__(self, b, e)
		self.type = t

class XSon():
	def parse(self, str):
		self.content = str
		self.cursor = 0
		self.tokens = []
		self.parseToken()
		return self.generate()

	def parseToken(self):
		self.is_text = False
		self.text_begin = -1
		for c in self.content:
			if c in symbol_array:
				"find a symbol"
				index = symbol_array.index(c)
				if self.is_text:
					self.appendTextToken(self.text_begin, self.cursor)
				self.appendSymbolToken(self.cursor, self.cursor + 1, index)
			else :
				"text"
				if not self.is_text:
					self.is_text = True
					self.text_begin = self.cursor
			self.cursor = self.cursor + 1
		if self.is_text:
			self.appendTextToken(self.text_begin, self.cursor - 1)
		self.printToken()

	def printToken(self):
		for e in self.tokens:
			e.printContent(self.content)	

	def appendTextToken(self, b, e):
		text = TextToken(b, e)
		self.tokens.append(text)
		self.is_text = False
		self.text_begin = -1

	def appendSymbolToken(self, b, e, t):
		symbol = SymbolToken(b, e, t)
		self.tokens.append(symbol)
	
	def generate(self):
		if len(self.tokens) < 1:
			return None
		print type(self.tokens[0])
		print type(TextToken)
		if isinstance(self.tokens[0], TextToken):
			return self.generateObj(self.tokens)
		elif isinstance(self.tokens[0], SymbolToken) and self.tokens[0].type == symbol_open_bracket:
			return self.generateArray(self.tokens)
		else:
			print "input text format error! below is the input text:"
			print self.content
			raise 

	def generateObj(self, toks):
		obj = {}
		key = None
		for i, token in enumerate(toks):
			if isinstance(token, TextToken):
				if not key:
					key = token
				else:
					obj[self.generateKey(key)] = token.getContent(self.content)
					key = None
			else:
				if token.type == symbol_colon:
					pass
				elif token.type == symbol_comma:
					pass	
				elif token.type == symbol_open_bracket:
					if key:
						obj[self.generateKey(key)] = generateArray(toks[i:])
					else:
						key = generateArray(toks[i:])
				elif token.type == symbol_double_quote or token.type == symbol_single_quote:
					pass
		
	def generateArray(self, toks):
		arr = []
		elem_begin = 0
		for i, token in enumerate(toks):
			if isinstance(token, SymbolToken):
				if token.type == symbol_close_bracket:
					return arr
				elif token.type == symbol_open_bracket:
					arr.append(self.generateArray(toks[i:]))
				elif token.type == symbol_comma:
					obj = self.generateElem(toks[elem_begin:i])
					if obj:
						arr.append(obj)
					elem_begin = i + 1
		return arr

	def generateElem(self, toks):
		l = len(toks)
		if l < 1:
			return None
		elif l == 1 and isinstance(toks[0], TextToken):
			return toks[0].getContent(self.content)
		elif l > 1:
			return self.generateObj(toks)
		else:
			print "generate elem in array error because there is 1 elem and not a texttoken!below is the input text:"
			print content
			raise
		
	def generateKey(self, key):
		if isinstance(token, TextToken):
			return key.getContent(self.content)
		else:
			return key

if __name__ == "__main__":
	str = "title:1,list:[t:2,f:3]"
	t = XSon()
	t.parse(str)
