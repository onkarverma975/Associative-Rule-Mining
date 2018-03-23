from itertools import chain, combinations
from collections import defaultdict
import csv

class Apriori:
	def __init__(self,config_file):
		self.configdata={}
		self.largeSet = dict()
		with open(config_file, 'rb') as configfile:
			spamreader = csv.reader(configfile, delimiter=',', quotechar='|')
			for row in spamreader:
				self.configdata[row[0]]=row[1]

	def getinputdata(self):
		self.minSupport = float(self.configdata['support'])
		self.minConfidence = float(self.configdata['confidence'])
		self.inputFile = self.configdata['input']
		self.outputFile = self.configdata['output']
		self.flag = int(self.configdata['flag'])
		# print self.flag
		self.transactionList = list()
		self.itemSet = set()
		with open(self.inputFile, 'rb') as configfile:

			spamreader = csv.reader(configfile, delimiter=',', quotechar='|')

			for row in spamreader:

				for item in row:
					self.itemSet.add(frozenset([item]))

				self.transactionList.append(frozenset(row))

	def findfreqitemset(self):
		oneCSet = self.returnItemsWithMinSupport(self.itemSet)
		k = 2

		currentLSet = oneCSet
		while (currentLSet != set([])):
			self.largeSet[k - 1] = currentLSet
			currentLSet = join(currentLSet, k)
			currentCSet = self.returnItemsWithMinSupport(currentLSet)
			currentLSet = currentCSet
			k = k + 1

	def getSupport(self, item):
		num = float(self.frequency[item])
		den = float(len(self.transactionList))
		return float(num / den)

	def RunApriori(self):


		self.getinputdata()

		self.frequency = defaultdict(int)

		toRetItems = []
		assocRules = dict()
		self.findfreqitemset()


		for key, value in self.largeSet.items():
			toRetItems.extend([(list(item), self.getSupport(item)) for item in value])


		if	self.flag==1:
			toRetRules = []

			for key, value in self.largeSet.items()[1:]:
				# print key, value
				for item in value:
					def subsets(expand_arr):
						return chain(*[combinations(expand_arr, first + 1) for first, second in enumerate(expand_arr)])
					_subsets = map(frozenset, [x for x in subsets(item)])
					for element in _subsets:
						remain = item.difference(element)
						if len(remain) > 0:
							num = float(self.getSupport(item))
							den = float(self.getSupport(element))
							confidence = float(num/den)
							if confidence >= self.minConfidence:
								# print confidence
								toRetRules.append(((list(element), list(remain)), confidence))

			self.write_result(toRetItems,toRetRules)
		else:
			self.write_result(toRetItems)

	def write_result(self, items, rules=[]):

		with open(self.outputFile, 'wb') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',')

			spamwriter.writerow([len(items)])

			for item, support in sorted(items, key=lambda (item, support): support):
				spamwriter.writerow(item)
			if self.flag==1:
				spamwriter.writerow([len(rules)])

				for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
					pre, post = rule
					spamwriter.writerow(pre+['=>']+post)

				# print "Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence)


	def returnItemsWithMinSupport(self, itemSet):
		_itemSet = set()
		localSet = defaultdict(int)

		for item in itemSet:
			for transaction in self.transactionList:
				if item.issubset(transaction):
					self.frequency[item] += 1
					localSet[item] += 1

		for item, count in localSet.items():
			support = float(count)/len(self.transactionList)

			if support >= self.minSupport:
					_itemSet.add(item)

		return _itemSet


def join(itemSet, length):
	ret_set = set()
	for i in itemSet:
		for j in itemSet:
			un = i.union(j)
			if len(un) == length:
				ret_set.add(un)
	return ret_set