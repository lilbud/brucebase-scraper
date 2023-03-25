import requests, re, os
from bs4 import BeautifulSoup

# enter the folder to save to here, defaults to your documents folder
folderToSave = os.environ["USERPROFILE"] + "\Documents\BB_Setlists\\"

def fileCreate(show, pageTitle, index):
	date = pageTitle[0:4] + "-" + pageTitle[5:7] + "-" + pageTitle[8:11]
	direct = folderToSave + pageTitle[0:4] + "\\"
	num = 0

	if (pageTitle[5:7] != "00"):
		direct = direct + pageTitle[5:7]

		if len(show) > 0:
			os.makedirs(direct, exist_ok=True)

			fileName = direct + "\\" + date.strip()

			if (os.path.exists(fileName + ".txt")):
				if index == 0:
					index = 1
				
				fileName = fileName + "_" + str(index)

			f = open(fileName + ".txt", "w")

			for song in show:
				f = open(fileName + ".txt", "a")
				f.write(song + "\n")
				f.close()

			print(f.name + " successfully created")

def titleCase(songName):
		return songName.title().replace("'S", "'s").replace("Th ", "th ").replace("Nd", "nd").replace("Ll", "ll").replace("'T", "'t").replace("'M", "'m")
		
def setlistFind(URL, show_find, index, fileAsk, printAsk, headerAsk):
	show = []
	headers = []
	xn = 0

	# getting the setlist itself
	showPage = requests.get(URL + show_find.get("href"))
	get_Setlist = BeautifulSoup(showPage.content, "html.parser")
	setlist = get_Setlist.find(id="wiki-tab-0-1")
	setN = setlist.find_all("ol")[0:]
	pageTitle = get_Setlist.find(id="page-title")

	for p in setlist.find_all("p"):
		for item in p.find_all("strong"):
			if "Soundcheck" not in item.text:
				headers.append(item.text + ":")
	
	# if "Soundcheck:" in headers:
	# 	headers.remove("Soundcheck:")

	if (len(headers) != 0):
		if (headerAsk.upper() == 'Y'):
			if (headers[xn] != "Show:"):
				show.append(headers[xn])
				xn+=1
		
	if (setN is not None):
		for p in setN:
			for song in p.find_all("a"):
				show.append(titleCase(song.text))
			if (xn < len(headers) and headerAsk.upper() == 'Y'):
				show.append("\n")
				show.append(headers[xn])
				xn+=1

	for song in show:
		if (song == "\n"):
			show.remove(song)
		elif (show[-1] == "Show:"):
			show.remove("Show:")

	if printAsk.upper() == "Y":
		print("\n" + pageTitle.text.strip()[0:10] + " - " + pageTitle.text.strip()[11:] + "\n")
		for song in show:
			print(song)

	if (fileAsk.upper() == "Y"):
		fileCreate(show, pageTitle.text.strip(), index)

def processing(URL, show_find):
	fileAsk = input("Output to File? [Y/N]:")
	printAsk = input("Print Setlist? [Y/N]:")
	headerAsk = input("Include Set Headers (Pre-Show, Different Artists, etc)? [Y/N]:")

	for show in show_find:
		if (show.get("href")[-1].isdigit()):
			num = show.get("href")[-1]
		else:
			num = 0

		if "/gig:" in show.get("href"):
			setlistFind(URL, show, num, fileAsk, printAsk, headerAsk)
		else:
			print("show not found")

def main():
	print("Brucebase Setlist Scraper: Gets Setlists From brucebase.wikidot.com")
	print("\n3 Options:\n\tEnter a Specfic Date (YYYY-MM-DD)\n\tA Date and Month (YYYY-MM)\n\tA Year(YYYY)")

	showDate = input("\nEnter Date: ")
	URL = "http://brucebase.wikidot.com"

	# URL and individual show page get
	yearURL = requests.get(URL + "/" + showDate[0:4])
	soup_year = BeautifulSoup(yearURL.content, "html.parser")

	if len(showDate) == 7:  # only a year and month entered
		show_find = soup_year.find_all("a", string=re.compile(showDate[0:7] + ".*"))
		processing(URL, show_find)
	elif len(showDate) == 4:
		show_find = soup_year.find_all("a", string=re.compile(showDate[0:4] + ".*"))
		processing(URL, show_find)
	elif len(showDate) == 10:  # full date entered, just one show
		try:
			show_find = soup_year.find_all("a", string=re.compile(showDate + ".*"))
		except:
			show_find = soup_year.find("a", string=re.compile(showDate + ".*"))

		processing(URL, show_find)

main()