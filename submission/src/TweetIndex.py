class TweetIndex:
	def __init__(self):
		self.index 				= {}
		self.tweets 			= []
		self.ops 					= []
		self.stack 				= []
		self.and_result 	= []
		self.or_result 		= []
		self.not_result 	= []
		self.result				= []
		self.found_param	= False

	# O(M * N) 
	# M = number of tweets
	# N = number of words in the tweet
	def process_tweets(self, list_of_tweets):
		self.tweets = list_of_tweets
		for tweets in list_of_tweets: # O(n)
			for word in tweets['tweet'].lower().split(' '): # O(m)
				if word not in self.index:
					self.index[word] = [int(tweets['timestamp'])]
				else:
					self.index[word].append(int(tweets['timestamp']))

	def search(self,query):
		self.refresh()
		search = query.lower().split()
		self.search_parser(search)
		if self.validate() == False:
			return 'Invalid Query'
		while len(self.stack) > 0:
			self.query_remaining()
		return self.get_results()

	def search_parser(self, search):
		for word in search:
			if word == '&':
				self.ops.append(word)
			elif word == '|':
				self.ops.append(word)
			elif word[0] == '(':
				self.stack.append(word[2:]) if word[1] == '(' else self.stack.append(word[1:])
			elif word[-1] == ')':
				self.stack.append(word[:-2])  if word[-2] == ')' else self.stack.append(word[:-1])
				self.query_parenthesis()
				if word[-2] == ')':
					self.query_parenthesis()
			else:
				self.stack.append(word)

	def validate(self):
		if '|' in self.ops and '&' in self.ops:
			if self.found_param == False:
				return False
		return True

	def query_remaining(self):  
		# print('AT ENTRY')
		# print('stack: ', self.stack)
		# print('ops: ', self.ops)

		op = self.ops.pop(0) if len(self.ops) > 0 else None
		word1 = self.stack.pop(0) 
		word2 = self.stack.pop(0) if len(self.stack) > 0 else None
		
		# print('AFTER POP')
		# print('word1: ', word1)
		# print('word2: ', word2) 
		# print('op: ', op)
		# print('stack: ', self.stack)

		if type(word1) == str and type(word2) == str:
			self.both_pops_str(word1, word2, op)
		elif type(word1) == str and word2 == None:
			self.first_str_sec_none(word1, word2, op)
		elif type(word1) == list and type(word2) == str:
			self.first_list_sec_str(word1, word2, op)
		elif type(word1) == str and type(word2) == list:
			self.first_str_sec_list(word1, word2, op)
		elif type(word1) == list and type(word2) == list:
			self.both_list(word1, word2, op)
		elif type(word1) == list and word2 == None:
			self.result = word1

	def query_parenthesis(self):
		self.found_param = True
		op = self.ops.pop()
		if op == '&':
			self.query_parenthesis_and(op)
		elif op == '|':
			self.query_parenthesis_or(op)

	# ----------------------------------------------------------------
	# query_parenthesis() helper methods
	# ----------------------------------------------------------------
	
	def query_parenthesis_and(self, op):
		word1 = self.stack.pop()
		word2 = self.stack.pop()
		if type(word1) == list and type(word2) == list:
			self.stack.append(list(set(word1) & set(word2)))
		elif type(word1) == list and type(word2) == str:
			self.query_and(word2)
			self.stack.append(list(set(self.and_result) & set(word1)))	
		else:
			self.query_and(word1)
			self.query_and(word2)
			self.stack.append(self.and_result)
			self.and_result = []

	def query_parenthesis_or(self,op):
		word1 = self.stack.pop()
		word2 = self.stack.pop()
		if type(word1) == list and type(word2) == list:
			self.stack.append(list(set(word1) | set(word2)))
		elif type(word1) == list and type(word2) == str:
			self.query_or(word2)
			self.stack.append(list(set(self.or_result) | set(word1)))
		else:
			self.query_or(word1)
			self.query_or(word2)
			self.stack.append(self.or_result)
			self.or_result = []

	# ----------------------------------------------------------------
	# print results
	# ----------------------------------------------------------------


	def get_results(self):
		result = []
		self.result.sort() # O(n log n)
		self.result = self.result[:5] if len(self.result) >= 5 else self.result
		for timestamp in self.result:
			for tweet in self.tweets:
				if int(tweet['timestamp']) == timestamp:
					result.append((tweet['timestamp'], tweet['tweet']))
		return result if len(result) > 0 else "No results found"


	# ----------------------------------------------------------------
	# query_remaining() helper methods
	# ----------------------------------------------------------------

	def both_list(self, word1, word2, op):
		if op == '&':
			self.stack.append(list(set(word1) & set(word2)))
		elif op == '|':
			self.stack.append(list(set(word1) | set(word2)))

	def first_str_sec_list(self, word1, word2, op):
		if word1[0] == '!':
			self.query_not(word1[1:])
			self.stack.append(list(set(word2) - set(self.not_result)))
		if op == '&' and word1[0] != '!':
			self.query_and(word1)
			self.stack.append(self.and_result)
		elif op == '|':
			self.query_or(word1)
			self.stack.append(self.or_result)

	def first_list_sec_str(self, word1, word2, op):
		if word2[0] == '!':
			self.query_not(word2[1:])
			self.stack.append(list(set(word1) - set(self.not_result)))
		if op == '&' and word2[0] != '!':
			self.query_and(word2)
			self.stack.append(self.and_result)
		elif op == '|':
			self.query_or(word2)
			self.stack.append(self.or_result)

	def first_str_sec_none(self, word1, word2, op):	
		if word1 in self.index:
			self.stack.append(self.index[word1])
		else:
			self.stack.append([])

	def both_pops_str(self, word1, word2, op):
		if word1[0] == '!':
			self.query_not(word1[1:])
			self.query_and(word2)
			self.stack.append(list(set(self.and_result) - set(self.not_result)))
		if word2[0] == '!':
			self.query_not(word2[1:])
			self.query_and(word1)
			self.stack.append(list(set(self.and_result) - set(self.not_result)))
		if op == '&' and (word1[0] != '!' and word2[0] != '!'):
			self.query_and(word1)
			self.query_and(word2)
			self.stack.append(self.and_result)
		elif op == '|':
			self.query_or(word1)
			self.query_or(word2)
			self.stack.append(self.or_result)	

	# ----------------------------------------------------------------
	# Operator query helper methods
	# ----------------------------------------------------------------

	def query_and(self, word):
		if len(self.and_result) == 0:
			if word in self.index:
				self.and_result = self.index[word]
		else:
			if word in self.index:
				self.and_result = list(set(self.and_result) & set(self.index[word]))
			else:
				self.and_result = list(set(self.and_result) | set([]))
		

	def query_or(self, word):
		if len(self.or_result) == 0:
			if word in self.index:
				self.or_result = self.index[word]
		else:
			if word in self.index:
				self.or_result = list(set(self.or_result) | set(self.index[word]))
			else:
				self.or_result = list(set(self.or_result) | set([]))
			

	def query_not(self, word):
		if len(self.not_result) == 0:
			if word in self.index:
				self.not_result = self.index[word]
		else:
			if word in self.index:
				self.not_result = list(set(self.not_result) | set(self.index[word]))
			else:
				self.not_result = list(set(self.not_result) - set([]))

	def refresh(self):
		self.ops 					= []
		self.stack 				= []
		self.and_result 	= []
		self.or_result 		= []
		self.not_result 	= []
		self.result				= []
		self.found_param	= False