import requests
from bs4 import BeautifulSoup
import card_num_generator as card
from random import randint
import random
import string
import csv
from pprint import pprint

class Person:
	def __init__ (self):
		self.name1 = first_names[randint(0,len(first_names)-1)]
		self.name2 = last_names[randint(0,len(last_names)-1)]
		self.d1 = str(randint(1,30))
		self.d2 = str(randint(1,12))
		self.d3 = str(randint(1900,1999))
		self.a1 = street_names[randint(0,len(street_names)-1)]
		self.a2 = street_names[randint(0,len(street_names)-1)]
		self.town = town_names[randint(0,len(town_names)-1)]
		self.postcode = postcodes[randint(0,len(postcodes)-1)]
		self.phone = "0"+str(randint(1000000000, 9999999999))
		self.mom = last_names[randint(0,len(last_names)-1)]

		card_types = ["discover", "mastercard", "americanexpress", "visa13", "visa16"]
		card_type = randint(0,4)
		self.cn = card.generate_card(card_types[card_type])
		self.em = str(randint(1,12))
		self.ey = str(randint(2019, 2030))
		cvv_gen = random.random()
		if cvv_gen < 1/3:
			cvv_gen = random.random()
			if cvv_gen < 1/2:
				self.cvv = "00"+str(randint(0,9))
			self.cvv = "0"+str(randint(10, 99))
		else:
			self.cvv = randint(100,999)

		self.ac = randint(10000000,99999999)
		self.sc = randint(100000,999999)

first_names = list()
last_names = list()
street_names = list()
town_names = list()
postcodes = list()
with open("names.csv") as f:
	for line in f.readlines():
		try:
			line = line.split(",")
			first_names.append(line[0])
			last_names.append(line[1][:-1])
		except:
			print()

with open("street_names.csv") as f:
	for line in f.readlines():
		try:
			line = line.split(",")
			street_names.append(line[1])
		except:
			print()

with open("town_names.csv") as f:
	for line in f.readlines():
		try:
			line = line.split(",")
			town_names.append(line[0])
		except:
			print()

with open("postcodes.csv") as f:
	for line in f.readlines():
		try:
			line = line.split(",")
			postcodes.append(line[0])
		except:
			print()

url = "https://sec.tx.access.dep.ref.on.cchasports.com/.kerpna/nvuqiosn/"

def submit():
	s = requests.session()

	first_page = BeautifulSoup(s.post(url).text, 'html.parser').meta
	first_page_part = str(first_page)[15:]
	first_claim_id = first_page_part[40:first_page_part.find("\"")]

	s.post("https://sec.tx.access.dep.ref.on.cchasports.com/.kerpna/nvuqiosn/start-process.php?claim_return_id=%s"%(first_claim_id))
	s.post("https://sec.tx.access.dep.ref.on.cchasports.com/.kerpna/nvuqiosn/personal-details-claim.php?claim_return_id=%s&step=personal_details"%(first_claim_id), data="commit=Continue")

	second_claim_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(randint(10,20)))
	second_url = "https://sec.tx.access.dep.ref.on.cchasports.com/.kerpna/nvuqiosn/payment-details-claim.php?claim_return_id=%s&step=payment_details"%(second_claim_id)
	person = Person()

	second_headers = {
	    'content-type': "application/x-www-form-urlencoded; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
	    'authorization': "Basic wwwwwww",
	    'cache-control': "max-age=0",
	    'connection': "keep-alive",
	    'referer' : "https://sec.tx.access.dep.ref.on.cchasports.com/.kerpna/nvuqiosn/personal-details-claim.php?claim_return_id=%s&step=personal_details"%(second_claim_id)
	    }
	second_data = "name1=%s&name2=%s&d1=%s&d2=%s&d3=%s&a1=%s&a2=%s&town=%s&postcode=%s&phone=%s&mom=%s"%(person.name1, person.name2, person.d1, person.d2, person.d3, person.a1, person.a2, person.town, person.postcode, person.phone, person.mom)

	s.post(second_url, data=second_data, headers=second_headers)

	third_claim_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(randint(10,20)))
	third_url = "https://sec.tx.access.dep.ref.on.cchasports.com/.kerpna/nvuqiosn/confirmation.php?claim_return_id_success=%s&step=confirmation"%(third_claim_id)
	third_headers = {
	    'content-type': "application/x-www-form-urlencoded; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
	    'authorization': "Basic wwwwwww",
	    'cache-control': "max-age=0",
	    'connection': "keep-alive",
	    'referer' : "https://sec.tx.access.dep.ref.on.cchasports.com/.kerpna/nvuqiosn/payment-details-claim.php?claim_return_id=%s&step=payment_details"%(third_claim_id)
	    }
	third_data = "nc=%s&cn=%s&em=%s&ey=%s&cvv=%s&ac=%s&sc=%s&PreventChromeAutocomplete="%((person.name1+" "+person.name2), person.cn, person.em, person.ey, person.cvv, person.ac, person.sc)

	return s.post(third_url, data=third_data, headers=third_headers), person.name1, person.postcode

count = 0

while count < 1000:
	try:
		out = submit()
		if str(out[0]) == "<Response [200]>":
			count+=1
			print("So far %s submitted with name %s and post code %s"%(count, out[1], out[2]), end='\r')
		else:
			print("Error: "+str(out))
	except:
		print("Error")
		
print("Done! %s submissions made"%(count))