import requests, re, os, sys
from bs4 import BeautifulSoup as bs4, SoupStrainer as strainer

global saveDir, URL, show, incHeaders, incSoundcheck, months, index
saveDir = os.environ["USERPROFILE"] + "\Documents\BB_Setlists\\"
URL = "http://brucebase.wikidot.com"
show = []
incHeaders = incSoundcheck = ""
months = ['_None', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

print("Brucebase Setlist Scraper: Gets Setlists From brucebase.wikidot.com")

try:
	showDate = sys.argv[1]
except:
	print("\nTwo Options:\n\tEnter a Specfic Date (YYYY-MM-DD)\n\tA Date and Month (YYYY-MM)")
	showDate = input("\nEnter Date: ")

incHeaders = input("Include Headers (Soundcheck, Different Artists, etc.)? [Y/N]: ")
while incHeaders == "":
	incHeaders = input("Include Headers (Soundcheck, Different Artists, etc.)? [Y/N]: ")

incSoundcheck = input("Include Soundcheck? [Y/N]: ")
while incSoundcheck == "":
	incSoundcheck = input("Include Soundcheck? [Y/N]: ")

def dateCheck(showDate):
	if (1965 <= int(showDate[0:4]) <= 2023):
		match len(showDate):
			case 10:
				if ((int(showDate[5:7]) / 12 <= 1)
					and (int(showDate[8:11]) / 31 <= 1) ):
						return True
			case 7:
				if ( int(showDate[5:7]) / 12 <= 1):
					return True

def titleCase(songName):
	return songName.title().replace("'S", "'s").replace("Th ", "th ").replace("Nd", "nd").replace("Ll", "ll").replace("'T", "'t").replace("'M", "'m").replace("'D", "'d").replace("'Ve", "'ve")

if not dateCheck(showDate):
	print("ERROR: Invalid Date")
	sys.exit()

yearURL = requests.get(URL + "/" + showDate[0:4])
soupYear = bs4(yearURL.content, "lxml")

def fileOutput(show, pageTitle, index):
	dir = saveDir + pageTitle[0:4] + "\\" + pageTitle[5:7] + "_" + months[int(pageTitle[5:7])] + "\\"
	fName = dir + pageTitle[0:11].strip()
	
	os.makedirs(dir, exist_ok=True)

	if len(show) > 0:
		if index == 0:
			f = open(fName + ".txt", "w")
		else:
			f = open(fName + "_" + str(index) + ".txt", "w")

		if incHeaders.upper() == "Y":
			f.write(pageTitle + "\n")

		for song in show:
			if index == 0:
				f = open(fName + ".txt", "a")
			else:
				f = open(fName + "_" + str(index) + ".txt", "a")

			if ":" in song:
				f.write("\n" + song + "\n")
			else:
				f.write(song + "\n")
			f.close()

		print("\n" + f.name + " successfully created")
		print("-" * 20 + "\n")

def showPrint(show, pageTitle):
	print(pageTitle[0:10] + " - " + pageTitle[11:] + "\n")

	for i, item in enumerate(show):
		if ":" in item:
			print("\n" + item)
		else:
			print(item)

def processing(item, index):
	showPage = requests.get(URL + item.get("href"))
	getSetlist = bs4(showPage.content, "lxml")
	setlist = getSetlist.find(id="wiki-tab-0-1")
	pageTitle = getSetlist.find(id="page-title").text.strip()

	for i, item in enumerate(setlist.find_all(True)):
		if item.name == "strong" and item.find_parent().name != "li" and incHeaders.upper() == 'Y':
			show.append(item.text.strip() + ":")
		if item.find_parent().name == 'ol':
			show.append(titleCase(item.text.strip()))
		if item.find_parent().name == "ul" and incSoundcheck.upper() == 'Y':
			if incHeaders.upper() == "N":
				show.append(titleCase(item.text.strip()) + " #")
			else:
				show.append(titleCase(item.text.strip()))

	if len(show) == 0:
		show.append("Setlist Not Found")
	
	showPrint(show, pageTitle)
	fileOutput(show, pageTitle, index)

match len(showDate):
	case 10:
		try:
			showFind = soupYear.find_all("a", string=re.compile(showDate + ".*"))
		except:
			showFind = soupYear.find("a", string=re.compile(showDate + ".*"))
	case 7:
		showFind = soupYear.find_all("a", string=re.compile(showDate[0:7] + ".*"))

index = 0
for item in showFind:
	if "/gig:" in item.get("href"):
		processing(item, index)
		show = []
		index += 1