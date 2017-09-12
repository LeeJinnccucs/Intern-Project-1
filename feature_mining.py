#-*- coding: utf8 -*-
# coding = utf8

import numpy as np
import pandas as pd
import math
import jieba
jieba.load_userdict('../Intern/user.dict.utf8')


from hotel import hotel_data

city_stopword = [u'市', u'縣', u'島']




class features_data:

	def __init__(self, data):
		self.hotelData = hotel_data(data)
		self.english_match = list()
		

	def eng_match(self):
		for i in self.hotelData.data:
#			print type(i[2])
			if i[0] in i[2]:
				self.english_match.append(100000)
			else:
				self.english_match.append(0)

	def city_match(self):
		cityName = [d[3].decode('big5') for d in self.hotelData.data]
		for i in cityName:
#			print type(i)
#			print i
			for single in i:
				if single in city_stopword:
					i.replace(single, '')


#			print i
#			print type(i)
#			for s in i[3].decode('big5'):
#				print s
#			print type(i[3])
			words = jieba.cut(i, cut_all = False)
#			print words
#			for c in words:
#				print type(c)
#				print c


def main():
	data = pd.read_csv('../Intern/data1.csv')
	raw_data = data.values[:, :]
	tt = features_data(raw_data)
#	tt.eng_match()
	tt.city_match()
	print type(city_stopword[0])
#	print tt.english_match

if __name__ == "__main__":
	main()
