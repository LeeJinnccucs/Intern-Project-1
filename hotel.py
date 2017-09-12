#-*- coding: utf8 -*-
# coding = utf8

from __future__ import division #always use float when dividing
import numpy as np
import pandas as pd
import math
import jieba
import copy #to copy data structure
jieba.load_userdict('../Intern/user.dict.utf8')
import chardet
from opencc import OpenCC


class hotel_data:

	def __init__(self, data):
		self.data = data  # basic data
		self.jieba_data = list() # after jieba
		self.exac_data = list() 
		self.keyword_table = None
		


		self.rest_data = list()
		self.final_text = list()
		self.clean_title = list()
		self.another_data = list()
#		self.exactly_match(self.data)
#		print self.exac_data

	def exactly_match(self, text): #目前作為jieba function
		for index, t in enumerate(text):
			words = list()
			words = jieba.cut(t[2], cut_all = False)
			self.jieba_data.append(list(words))

	def remove_symbol(self, input_str):  # remove useless symbol
#		print len(input_str)
		for i in input_str:
			if (i < '一'.decode('utf8') or i > u'\u9fcc'):
				if not ((i >= 'A' and i <= 'Z') or (i >= 'a' and i <= 'z') or  (i >= '0' and i <= '9')):
					input_str = input_str.replace(i, '')
			else:
				continue
#		print input_str
		return input_str

	def getVectorKeywordIndex(self, keyword_text):  #make keyword dict
		
		vectorIndex = {}
		freq = 1
		big_text = list()
#		english_text = list()

		for wordlist in keyword_text:
			for i in wordlist:
				try:
					big_text.append(i.encode('utf8'))  #prevent iterating per letter(need per word)
				except:
					continue
		
#		print big_text
		KeywordIndex = set(big_text) #set using needs to be a single list
#		print KeywordIndex
		for word in KeywordIndex:
			vectorIndex[word] = freq
		return vectorIndex
	
	def unigram_model(self, vectorIndex):
		total_words = sum(vectorIndex.values())
		uni_dict = {key: num/total_words for key, num in vectorIndex.iteritem()}
		return uni_dict

	def laplace_smoothing(self, num):
		return ((num+1)/(num+len(self.keyword_table)))

	def cal_KeywordTable(self, keywordtext, vectorTable):
		result = copy.deepcopy(vectorTable) #ensure copying all layer of dict
		count = 0
		for vectors in keywordtext:
			for sss in vectors:
#			print len(list(vectors))
#				print type(sss)
#				if ''.join(sss) == '夏都沙灘酒店'.decode('utf8'):
#					print ('ereerer')
#					print type('夏都沙灘酒店')
#					count += 1
#					result[''.join(sss.encode('utf8'))]
				if sss.encode('utf8') in result:
					try:
						result[''.join(sss.encode('utf8'))] = result[''.join(sss.encode('utf8'))] + 1  # 如果要調用dict的key，要確保型態是一致的
					except:
						continue
		print result['夏都沙灘酒店']		
		result = {j: self.laplace_smoothing(v) for j,v in result.iteritems()}
		return result

def compare_nan(x, y):
	if x == 1:
		return 1
	elif y == 1:
		return -1

def main():
	data = pd.read_csv('../Intern/data1.csv')
	raw_data = data.values[:, :]
	ss = hotel_data(raw_data)
	for index, jjj in enumerate(ss.data):
#		print index
#		print jjj[2]
		try:
			jjj[2] = ss.remove_symbol(jjj[2].decode('big5'))
		except:
			continue
#		print jjj[2]
	ss.exactly_match(ss.data)
#	for wordlist in ss.jieba_data:
#		for word in wordlist:
#			print word
#			print type(word)
#			print word.encode('utf8')
#			print type(word.encode('utf8'))
	for lines in ss.jieba_data:
		lines = list(lines)  #prevent iterating over generator
#	print type(ss.jieba_data[0])


	temp_jieba = ss.jieba_data[:] #copy new list prevent same reference

	kk = ss.getVectorKeywordIndex(temp_jieba)

	ss.keyword_table = copy.deepcopy(kk)
#for key, value in kk.iteritems():
#	        print key, value

#	print kk

	temp2_jieba = ss.jieba_data[:]




#	for iiii in ss.jieba_data:
#		for ccc in iiii:
#			print ccc


#	print jj


	jj = ss.cal_KeywordTable(temp2_jieba, kk) 
#	print [i for i in kk.keys()]

	for key, value in jj.iteritems(): #print lm
		print key, value

	print '東京' + str(jj['東京'])

#	print jj

#	print ss
#	print ss.another_data
	ss.final_text.append(ss.exac_data)
	ss.final_text.append(ss.rest_data)
#	print type(ss.final_text)
#	print ss.final_text[0]
"""  #output to csv
	#make output file
	output = list()
#	output = np.asarray(ss.final_text).reshape((7,2))
	for index, i in enumerate(ss.exac_data):
		print index
		print i
		output.append(np.asarray(i))
	columns = ['name_en', 'name-tw', 'title', 'city', 'country', 'exactly_match', 'Correctness']
	outputDf = pd.DataFrame(ss.exac_data, columns = columns)
	outputDf.to_csv('ff-results-20170821-182734.csv', index = False)
"""
if __name__ == "__main__":
	main()
