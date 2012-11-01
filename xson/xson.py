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
		self.is_parse = False
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

class TokenIter(object):
	def __init__(self, ts):
		self.tokens = ts
		self.index = -1

	def next(self):
		self.index += 1
		if self.index >= len(self.tokens):
			raise StopIteration
		else:
			return self.tokens[self.index]
		
	def __iter__(self):
		return self
		
	def remove(self, b, e):
		self.tokens.__delslice__(b, e)
	
	def printToken(self):
		pass

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
			if token.is_parse:
				pass
			elif isinstance(token, TextToken):
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
						obj[self.generateKey(key)] = self.generateArray(toks[i:])
						key = None
					else:
						key = self.generateArray(toks[i:])
				elif token.type == symbol_double_quote or token.type == symbol_single_quote:
					pass
			token.is_parse = True
		return obj
		
	def generateArray(self, toks):
		arr = []
		elem_begin = 0
		toks[0].is_parse = True
		toks = toks[1:]
		for i, token in enumerate(toks):
			if isinstance(token, SymbolToken):
				if token.type == symbol_close_bracket:
					obj = self.generateElem(self.getUnParseElements(toks[elem_begin:i]))
					if obj:
						arr.append(obj)
					for j, each in enumerate(toks):
						if j > i: 
							break
						each.is_parse = True
					return arr
				elif token.type == symbol_open_bracket:
					arrElem = self.generateArray(toks[i:])
					arr.append(arrElem)
				elif token.type == symbol_comma:
					obj = self.generateElem(self.getUnParseElements(toks[elem_begin:i]))
					token.is_parse = True
					if obj:
						arr.append(obj)

		return arr

	def getUnParseElements(self, toks):
		return [tk for tk in toks if not tk.is_parse]

	def generateElem(self, toks):
		l = len(toks)
		print l
		if l < 1:
			return None
		elif l == 1 and isinstance(toks[0], TextToken):
			toks[0].is_parse = True
			return toks[0].getContent(self.content)
		elif l > 1:
			return self.generateObj(toks)
		else:
			print "generate elem in array error because there is 1 elem and not a texttoken!below is the input text:"
			print content
			raise
		
	def generateKey(self, key):
		if isinstance(key, TextToken):
			return key.getContent(self.content)
		else:
			return key

if __name__ == "__main__":
	str = "j:2,f:3,ll:[1,2,3,2:33]"
	t = XSon()
	print t.parse(str)
