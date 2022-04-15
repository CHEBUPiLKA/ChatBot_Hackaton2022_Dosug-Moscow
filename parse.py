import json
import requests
from bs4 import BeautifulSoup
import geo

http_proxy  = "http://62.210.119.138:3128"
proxies = { 
              "http"  : http_proxy
            }

class event:
	def __init__(self, distance, picture, name, price, place, linkk):
		self.distance = distance #расстояние
		self.picture = picture #картинка
		self.name = name #название
		self.price = price #цена
		self.place = place #место
		self.coords = geo.geocode(place) #координаты
		self.link = linkk
		#self.descrpition = descrpition

	def distance(self, adress):
		self.distance = geo.dist(self.place, adress)
def sort(ans):
  for i in range(len(ans)-1):
    for j in range(len(ans)-i-1):
      if ans[j].distance > ans[j+1].distance:
        ans[j], ans[j+1] = ans[j+1], ans[j]
  return ans
def GetJson(url, proxies):
	ans = []
	r = requests.get(url, proxies=proxies)
	soup = BeautifulSoup(r.text, 'html.parser')
	soup = soup.find_all(class_="CHPy6")
	for i in range(20):
		try:
			ans.append(dict(json.loads(str(soup[i]).split(">")[3].replace("</script", " ").replace('"', '\"'))))
		except:
			continue
	return ans

def GetObjects(link):
	mas = GetJson(link, proxies)
	ans = []
	for i in mas:
		try:
			l = i["@id"]
			ans.append(event("", dict(i['image'])['url'], i['name'], dict(i['offers'])['price'], dict(i['location'])['name'], l))
		except:
			continue
	return ans

def PreparationLink(card, range, type, date):
	default = "https://www.culture.ru/afisha/moskva/"
	if card:
		default += "pushkinskaya-karta/"
	if str(type) != "Любые":
		if type == "Встречи":
			default += "vstrechi/"

		elif type == "Выставки":
			default += "vistavki/"

		elif type == "Кино":
			default += "kino/"

		elif type == "Концерты":
			default += "kontserti/"

		elif type == "Обучение":
			default += "obuchenie/"

		elif type == "Праздники":
			default += "prazdniki/"

		elif type == "Прочее":
			default += "prochie/"

		elif type == "Спектакли":
			default += "spektakli/"

		elif type == "Фестивали и праздники":
			default += "festivali-i-prazdniki/"

		elif type == "Экскурсии":
			default += "ekskursii/"

	if str(range) != "-1":
		default += "minPrice-" + range.split("-")[0] + "/"
		default += "maxPrice-" + range.split("-")[1] + "/"

	default += "seanceStartDate-" + date + "/"
	default += "seanceEndDate-" + date + "/"
	return default

'''print(PreparationLink(False, "100-500", "Встречи", ""))
a = GetObjects(PreparationLink(False, "100-500", "Встречи", "2022-04-15"))
print(a[0].distance)
print(a[0].picture)
print(a[0].name)
print(a[0].price)
print(a[0].place)
print(a[0].link)
print(a[0].descrpition)'''
#print(GetObjects(PreparationLink(False, "100-500", "Встречи", ""))[0].place)
#print(GetObjects(PreparationLink(False, "100-500", "Встречи", ""))[0].coords)