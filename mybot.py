# -*- coding: UTF-8 -*-

from fbchat import Client, log
from fbchat.models import *
from pprint import pprint
from datetime import datetime
from threading import Timer
from random import randrange
from dadjokes import dadjokes
import requests, json
import random
import configparser
import config


thread_id = '3433777146642310' #change to correct one
thread_type = ThreadType.GROUP  
botName = 'kole'
botNameCyr = (u"коле").encode('utf-8')
cookies ={}
hora = []
vila_link= "https://vila.bg/house-slanchev-ray-3766.html"
koliDic = {}
birichki = {}
alkohol= config.alkohol

#nicknameTracker = {} # on every nickname change map the ID to the current nickname

stepeni_na_tuppost = ["Да", "Умно момче е", "Не", "spored zavisi", "100%", "https://i.makeagif.com/media/6-09-2015/z9B18E.gif","https://media3.giphy.com/media/NdKVEei95yvIY/giphy.gif"]
#sloji oshte gifcheta


# Subclass fbchat.Client and override required methods
class KoleBot(Client):
	def getWeatherEmoji(self,weatherID):
	    # Openweathermap Weather codes and corressponding emojis
	    thunderstorm = u"⛈"    # Code: 200's, 900, 901, 902, 905
	    drizzle = u"🌫"         # Code: 300's
	    rain = u"🌧"            # Code: 500's
	    snowflake = u"❄"      # Code: 600's snowflake
	    snowman = u"☃"        # Code: 600's snowman, 903, 906
	    atmosphere = u"🌫"      # Code: 700's foogy
	    clearSky = u"☀"      # Code: 800 clear sky
	    fewClouds = u"🌤"      # Code: 801 sun behind clouds
	    clouds = u"☁️"        # Code: 802-803-804 clouds general
	    hot = u"☀"         # Code: 904
	    defaultEmoji = u"🤷"    # default emojis

	    weatherID = str(weatherID)
	    if weatherID[0] == '2' or weatherID == '900' or weatherID == '901' or weatherID == '902' or weatherID == '905':
	        return thunderstorm
	    elif weatherID[0] == '3':
	        return drizzle
	    elif weatherID[0] == '5':
	        return rain
	    elif weatherID[0] == '6' or weatherID == '903' or weatherID == '906':
	        return snowflake + ' ' + snowman
	    elif weatherID[0] == '7':
	        return atmosphere
	    elif weatherID == '800':
	        return clearSky
	    elif weatherID == '801':
	        return fewClouds
	    elif weatherID == '802' or weatherID == '803' or weatherID == '803':
	        return clouds
	    elif weatherID == '904':
	        return hot
	    else:
	        return defaultEmoji
	def get_weather(self,api_key, location):
		url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}&lang=bg".format(location, api_key)
		r = requests.get(url)
		return r.json()
	def formatWeatherData(self,w_data, mesto):
		wData = "Температура за {} : {} °C".format(w_data['name'].encode('utf-8'),w_data['main']['temp'])
		wData += "\nСкорост на вятъра: {} m/s".format(w_data['wind']['speed'])
		emjo =self.getWeatherEmoji(w_data['weather'][0]['id'])
		wData += "\nОписание: {} {}".format(w_data['weather'][0]['description'].encode('utf-8'),emjo.encode('utf-8'))
		return wData
	def loadCars(self):
		try:
			a_file= open("data.json", "r")
			output = a_file.read()
			a_file.close()
		except FileNotFoundError:
			return {}
		return output
	def saveCars(self):
		a_file= open("data.pkl", "w+")
		json.dump(koliDic,a_file)
		a_file.close()
	def sendHelp(self):
		helpStr = "Отговор на вечния въпрос, \"kole, poluchi li?\" "
		helpStr += "\nРазработено от: Митачето 🍺"
		helpStr += "\nЗа списък със всички възможни команди и полезна информация: https://github.com/dpetzev/KoleBot/blob/master/README.md"
		return helpStr
	def pprintKoli(self):
		if(len(koliDic)==0):
			return "Няма нищо за сега, пробвай да добавиш."
		separator = ', '
		koliStr=""
		for key, values in koliDic.items():
			koliStr += key + random.choice([u"🚕",u"🚗",u"🚙",u"🏎",u"🚜"]).encode('utf-8')+": "
			koliStr+=separator.join(values)
			koliStr+= '\n'
		return koliStr
	def birichkiKlasaciq(self):
		sortiraniBirichki=sorted(birichki,key=birichki.get,reverse=True)
		oldVal=-1
		klasaciq = ""
		idx=0
		for chovek in sortiraniBirichki:
			value = birichki[chovek]
			if(value ==0):
				klasaciq+= "👎"
			else:
				if(oldVal==value):
					idx=idx-1
				if(idx+1==1):
					klasaciq+= "🥇"
				elif(idx+1==2):
					klasaciq+= "🥈"
				elif(idx+1==3):
					klasaciq+= "🥉"
				elif(idx==birichki.len() or value==0):
					klasaciq+= "👎"
			klasaciq+= str(idx+1)+ ". "+chovek + ": "
			for x in range(value):
				klasaciq += "🍺"
			klasaciq+="\n"
			oldVal=value;
			idx = idx +1
		return klasaciq
	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		self.markAsDelivered(thread_id, message_object.uid)
		self.markAsRead(thread_id)
		text = message_object.text.lower()
		text = text.encode('utf-8')
		print(message_object.text) #debug

		if author_id == self.uid:
			return
		if text== "kole" or text=="коле":
				self.send(Message(self.sendHelp()),thread_id=thread_id,thread_type=thread_type)
		elif text.startswith(botName) or text.startswith(botNameCyr):
			split_message = text.split(' ',1)
			text=split_message[1] #text bez imeto na bota
			if text.startswith("vreme") or text.startswith("време"):
				split = text.split(' ')
				mesto = split[1]
				api_key=config.apiWeather
				weather = self.get_weather(api_key,mesto)
				self.send(Message(self.formatWeatherData(weather,mesto)),thread_id=thread_id,thread_type=thread_type)
			elif text.startswith("simitli") or text.startswith("симитли"):
				self.send(Message("☀ грее 🌧 вали .."),thread_id=thread_id,thread_type=thread_type)
			elif text.startswith("kak si") or text.startswith("как си"): 
				self.send(Message("biva, ti kak si?"),thread_id=thread_id,thread_type=thread_type)
			elif text.startswith("sfanali") or text.startswith("сфанали"): 
				self.send(Message("Sfanah bate!"),thread_id=thread_id,thread_type=thread_type)
			elif text.startswith("poluchi li"):
				self.send(Message("da"),thread_id=thread_id,thread_type=thread_type)
			elif text.startswith("maikata si e"):
				self.sendRemoteFiles("https://thumbs.gfycat.com/CelebratedUnacceptableAmericansaddlebred-size_restricted.gif", message=None, thread_id=thread_id, thread_type=thread_type)
			elif text.startswith("penata"):
				self.sendRemoteFiles("https://thumbs.gfycat.com/LiquidUnknownKite-mobile.mp4", message=None, thread_id=thread_id, thread_type=thread_type)
			elif text.startswith("mlad merin"):
				self.sendRemoteFiles("https://thumbs.gfycat.com/ChillyHatefulFlyingsquirrel-mobile.mp4", message=None, thread_id=thread_id, thread_type=thread_type)
			elif text.startswith("v nastroenie") or text.startswith("в настроение"): 
				self.sendRemoteFiles("https://haha.bg/wp-content/uploads/2018/10/v-nastroenie-ste-vizhdam-ne.gif", message=None, thread_id=thread_id, thread_type=thread_type)
			elif text=="kak shte si na vilata" or text=="как ще си на вилата": 
				self.sendRemoteFiles("https://thumbs.gfycat.com/FabulousCrispAmericanquarterhorse-small.gif", message=None, thread_id=thread_id, thread_type=thread_type)
			# vila logic
			# vila - link kum obqvata
			# vila koi - koi shte idvat
			# vila kolko - po kolko pari?
			# vila kude - mestonahojdenie na vilata
			# vila koga - koi dati
			elif (text == "vila" or text == "вила"):
				self.send(Message(vila_link),thread_id=thread_id,thread_type=thread_type)
			#if text.startswith(botName + "vila kude"):
			#self.sendPinnedLocation
			elif text.startswith("vila koi") or text.startswith("вила кои"):
				separator = ', '
				self.send(Message(separator.join(hora)),thread_id=thread_id,thread_type=thread_type)
			elif (text.startswith("vila kolko") or text.startswith("вила колко")):
				self.send(Message("После ще говорим."),thread_id=thread_id,thread_type=thread_type)
			elif (text.startswith("vila koga") or text.startswith("вила кога")):
				self.send(Message("20-22 Септември, 2020"),thread_id=thread_id,thread_type=thread_type)	
			# koli logic
			# dobavi kola {imeto na kola}
			# mahni kola {imeto na kola}
			# dobavi {imeto na chovek} kum {imeto na kola}
			# mahni {imeto na chovek} ot {imeto na kola}
			# preimenuvai kola {startoto imeto na kola} na {novoto ime na kola}
			elif text.startswith("dobavi") or text.startswith("добави"):
				split = text.split(' ')
				if(split[1]=="kola" or split[1]=="кола"):
					imetoKola = split[2]
					if imetoKola in koliDic:
						self.send(Message("Вече има такава кола ("+imetoKola+")"),thread_id=thread_id,thread_type=thread_type)
					else:
						koliDic[imetoKola]= []
						self.send(Message("gotov si"),thread_id=thread_id,thread_type=thread_type)
				else:
					imetoChovek = split[1]
					imetoKola = split [3]
					if imetoChovek in koliDic[imetoKola]:
						self.send(Message("Вече е там"),thread_id=thread_id,thread_type=thread_type)
					else:
						koliDic.setdefault(imetoKola,[]).append(imetoChovek)
						self.send(Message("gotov si"),thread_id=thread_id,thread_type=thread_type)
				self.saveCars()
			elif (text.startswith("mahni") or text.startswith("махни")):
				split = text.split(' ')
				if(split[1]=="kola" or split[1] =="кола"):
					imetoKola= split[2]
					if imetoKola in koliDic:
						koliDic.pop(imetoKola,None)
						self.send(Message("gotov si"),thread_id=thread_id,thread_type=thread_type)
					else:
						self.send(Message("Няма такава кола, пробвай да я добавиш първо?"),thread_id=thread_id,thread_type=thread_type)
				else:
					imetoChovek = split[1]
					imetoKola = split[3]
					if imetoChovek in koliDic[imetoKola]:
						koliDic[imetoKola].remove(imetoChovek)
						self.send(Message("gotov si"),thread_id=thread_id,thread_type=thread_type)
					else:
						self.send(Message("Няма такъв човек ("+imetoChovek+ ") към тази кола"),thread_id=thread_id,thread_type=thread_type)
				self.saveCars()
			elif (text.startswith("preimenuvai") or text.startswith("преименувай")):
				split = text.split(' ')
				if(split[1]=="kola" or split[1]== "кола"):
					imetoKola = split[2]
					if imetoKola in koliDic:
						novoIme = split [4] #sled  "na"
						koliDic[novoIme]= koliDic.pop(imetoKola)
						self.send(Message("gotov si"),thread_id=thread_id,thread_type=thread_type)
					else:
						self.send(Message("Не виждам такава кола."),thread_id=thread_id,thread_type=thread_type)
				self.saveCars()
			elif (text.startswith("koli") or text.startswith("коли")):
				self.send(Message(self.pprintKoli()),thread_id=thread_id,thread_type=thread_type)
			elif "tup li e" in text:
				otgovor = random.choice(stepeni_na_tuppost)
				if otgovor.startswith("http"): # takuv li trebva da e url-to? string
					self.sendRemoteFiles(otgovor, message=None, thread_id=thread_id, thread_type=thread_type)
				else:
					self.send(Message(otgovor),thread_id=thread_id,thread_type=thread_type)
			elif (text.startswith("bir") or text.startswith("бир")):
				split = text.split(' ')
				chovek = split[1].decode('utf-8')
				if(chovek not in hora):
					if(split[1]== "klasaciq" or split[1] =="класация"):
						self.send(Message(self.birichkiKlasaciq()),thread_id=thread_id,thread_type=thread_type)
					else:
						self.send(Message("Не намирам "+split[1]),thread_id=thread_id,thread_type=thread_type)
				else:
					birichki[split[1]]=birichki.get(split[1],0)+1
					self.send(Message("🍺"),thread_id=thread_id,thread_type=thread_type)
			elif text.startswith("uzo"):
				self.sendRemoteFiles("https://i.makeagif.com/media/10-11-2014/EgJZeO.gif", message=None, thread_id=thread_id, thread_type=thread_type)
			elif text.startswith("kolko biri") or text.startswith("колко бири"):
				split = text.split(' ')
				chovek = split[2].encode('utf-8')
				if(chovek not in hora):
					self.send(Message("Не намирам "+split[2]),thread_id=thread_id,thread_type=thread_type)
				else:
					self.send(Message(split[2]+ "е на " + birichki[split[2]] + " бири"),thread_id=thread_id,thread_type=thread_type)
			elif (text == "kakvo da piq" or text == "какво да пия"):
				otgovor = random.choice(alkohol)
				self.send(Message(otgovor),thread_id=thread_id,thread_type=thread_type)
			elif (text == "shega" or text == "шега"):
				joke_msg = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'}).json().get('joke')
				self.send(Message(joke_msg),thread_id=thread_id,thread_type=thread_type)
			else:
				self.send(Message("Не разбирам какво точно искаш от мен. Пробвай \"kole\" или \"коле\" за помощ и полезна информация"),thread_id=thread_id,thread_type=thread_type)
	def onListening(self):
		group = client.fetchGroupInfo(thread_id)[thread_id]
		listOfUserObjects = self.fetchAllUsersFromThreads([group])
		for userObj in listOfUserObjects:
			ime = userObj.first_name.lower()
			index = 0;
			while(ime in hora):
				if(index ==0):
					ime = ime + "_"
				if(index==len(userObj.last_name)-1):
					ime = ime + str(randrange(10))
				else:
					ime = ime + userObj.last_name[index]
				index=index+1
			hora.append(ime)
		birichki = dict.fromkeys(hora,0)
	def onPersonRemoved(self,mid,removed_id,author_id,thread_id,ts,msg):
		thread_id_list = [thread_id]
		userInfo = self.fetchUserInfo(removed_id)
		for userObj in userInfo.values():
			self.send(Message("Auf wiedersehn {}".format(userObj.first_name)),thread_id=thread_id,thread_type=thread_type)
			if(userObj.first_name in hora):
				hora.remove(userObj.first_name)
			birichki.pop(userObj.first_name,None)
			#birichki.pop(userObj.nickname,None)  #potential bug if someones nickname is also a first name in the dict
	def onPeopleAdded(self,mid,added_ids,author_id,thread_id,ts,msg):
		thread_id_list = [thread_id]
		usersInfo = self.fetchUserInfo(added_ids[0])
		for userObj in usersInfo.values():
			self.send(Message(u"👋 Нека всички кажем здравей на {}".format(userObj.first_name)),thread_id=thread_id,thread_type=thread_type)
			ime = userObj.first_name
			index = 0
			while (ime in hora):
				if(index ==0):
					ime = ime + "_"
				if(index==len(userObj.last_name)-1):
					ime = ime + str(randrange(10))
				else:
					ime = ime + userObj.last_name[index]
				index=index+1
			birichki[userObj.first_name]= 0
			hora.append(ime)

 #    # it's much better to be called by your nickname than first name
	# def onNicknameChange(self,mid,author_id,changed_for,new_nickname,thread_id,thread_type,ts,metadata,msg):
	# 	#thread_id_list = [thread_id]
	# 	userInfo = self.fetchUserInfo(changed_for)
	# 	for usrId, userObj in userInfo.items():
	# 		oldNickname = nicknameTracker.get(usrId)
	# 		if(oldNickname!=None):
	# 			hora.remove(oldNickname)
	# 			birichki[new_nickname] = birichki.pop(oldNickname)
	# 		else:
	# 			hora.remove(userObj.first_name)
	# 			birichki[new_nickname] = birichki.pop(userObj.first_name)
	# 		hora.add(userObj.new_nickname)
	# 		nicknameTracker[usrId]=new_nickname

try:
    # Load the session cookies
    with open('session.json', 'r') as f:
        cookies = json.load(f)
except:
    # If it fails, never mind, we'll just login again
    pass

# Attempt a login with the session, and if it fails, just use the email & password
client = KoleBot(config.username,config.password,session_cookies = cookies)

#koliDic= client.loadCars()

x=datetime.today()
# Save the session again
with open('session.json', 'w') as f:
    json.dump(client.getSession(), f)
if not client.isLoggedIn():
    client.login()

client.listen()


# bira za ili samo da ima  "bir", ime + kolko + "bit"?, da se resetnat primerno u 9 sutrinta
# playlist - moq spotifi ILI toq v youtube
	# grucko - grucki playlist ili random song ot playlist
	# radio????
	# srubsko
	# rumunsko
	# mazno
	# azis
	# rap
# help function? - add the link to the github and add a read me ?!?! maybe in English as well?
# "pretty" the code formatiing
# kak  da vurvi postoqnno bez da trqbva da mi e otvoren laptopa? - herouko
# make koli dic save somewhere periodacally if program ends unexpectably
# mojite 🥇, 🥈, 🥉, 👎, 🍺
# test saving/loading cars
# test nickname stuff
# reading hore populates it with first names not nicknames, stay on just first names?, what to do when two people with same name
# inpersonremoved the persons name could be more than just his/her first name
