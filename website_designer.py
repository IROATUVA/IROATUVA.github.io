import sys # An included library with Python install.
from datetime import date # An included library with Python install.
import datetime # An included library with Python install.
import os # An included library with Python install.
import shutil # I believe you have to install this one

months = {1:"Jan", 2:"Feb", 3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
header_list = ["Home","Day-by-Day Data","Extra Charts and Graphs", "Statistics by Branch", "Code Host", "About"]
header_links = ["../","../datapage","../charts","../branch", "https://github.com/IROATUVA/iroatuva.github.io","https://www.iroatuva.org/about"]

active_number = 0 #This is the index of the element in the header_list that is active at a given time

top_banner = '''.barlist {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333;
}

.bar {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

.bar a:hover:not(.active) {
  background-color: #111;
}

.active {
  background-color: #4CAF50;
}
</style>
</head>
<body>
'''
heading = '<!DOCTYPE HTML>\n<html>\n<head><!Content created by Mohit Srivastav. IRO Treasurer term Spring 2020-Fall 2020>\n'

def bulleted_list_maker(obj_list):
	if isinstance(obj_list,list):
		code_text = ''
		code_text += '<ul>\n'
		for i in obj_list:
			code_text += '\t<li><h2> ' + i + ' </h2></li>\n'
		code_text += '</ul>\n'
		return code_text
	else:
		return None

def header(active_number, header_list, header_links): #The header list is the list of things you want ot put in the header
#The active number is the element of the list that is deemed to "active" at that time
	code_text = ''
	code_text += '<ul class = "barlist">\n'
	for i in range(len(header_list)):
		code_text += '\t<li class = "bar"><'
		if i == active_number:
			code_text += 'a class="active">'
		else:
			code_text += 'a href='+header_links[i] + '>'
		code_text += header_list[i] + '</a></li>\n'
	code_text += '</ul>\n'

	return code_text

def make_table_from_csv(filename, columns, title, div_name, column_titles, placeholder = False):
	if not isinstance(column_titles, list):
		raise TypeError("You need a list as the fifth parameter!")
	if not isinstance(columns, int):
		raise TypeError("The second parameter has to be a whole number!")
	if not isinstance(title, str) or not isinstance(div_name, str) or not isinstance(filename, str):
		raise TypeError("The first, third, and fourth parameters have to be strings!")
	if  len(column_titles) != columns:
		raise TypeError("The column title list and the number of columns have to be the same!")
	if ".csv" not in filename:
		raise TypeError("file given must be a .csv file!")

	code_text = ""

	if placeholder:
		return '<div id = "'+div_name+'" style = "display:none;" "text-align:center;"><br><br> not available right now </div>\n'

	with open(filename, encoding='utf-8') as f:
		code_text += '<div id = "'+div_name+'" style="display:none" "width:100%";>\n'
		code_text += '<table style="width:100%";>\n'
		code_text += '<tr>\n' 
		code_text += '\t<th colspan = "'+str(columns)+'"> <h1> '+title+' </h1> </th> \n </tr>\n'

		code_text += '<tr>\n'
		for i in range(len(column_titles)):
			code_text += '\t<th> ' + column_titles[i] + ' </th>\n'
		code_text += '</tr>\n'

		for line in f:
			line = line.strip().split(',')
			code_text += '<tr>\n' + '\t' + '<th> ' + line[0] + ' </th>\n'
			code_text += '\t<th> ' + line[1] + ' </th>\n'
			code_text += '</tr>\n'
	code_text += '</table>\n</div>\n'

	return code_text


def dropdown_displayer(filenames, selection_list, table_title_list, table_column_title_list):
	div_id_list = []

	if not isinstance(filenames, list) or not isinstance(selection_list, list):
		raise TypeError("You need a list as the first and last parameter!")

	for i in range(len(selection_list)):
		div_id_list.append(str(i))

	code_text = ""
	code_text += '''<select class="default" id="data_shower" name="data_shower">
    <option value="" selected>Select the type of data you want to show</option>\n'''

	for i in range(len(selection_list)):
		code_text += '\t<option value="'+str(i)+'">'+selection_list[i]+'</option>\n'
	code_text += '</select>\n'

	for i in range(len(selection_list)):
		if i >= len(filenames): #Adds an extra placeholder for any elements not given filenames
			code_text += make_table_from_csv(".csv", 0,"",div_id_list[i],[],True)
			continue
		code_text += make_table_from_csv(filenames[i], len(table_column_title_list[i]), table_title_list[i], div_id_list[i], table_column_title_list[i])

	code_text += '<script>\n'
	code_text += 'var elem = document.getElementById("data_shower");\n'
	code_text += 'var x = ' + str(div_id_list).replace("'",'"') + ';\n'
	code_text += 'elem.onchange=function(){\n'
	code_text += '''\t if (elem.value == ""){
		for(var i = 0; i < x.length; i++){
			document.getElementById(x[i]).style.display = "none";
		}
	}'''
	for i in div_id_list:
		code_text += '\n\t if (elem.value == "'+str(i)+'''"){
			for(var i = 0; i < x.length; i++){
				document.getElementById(x[i]).style.display = "none";
			}\n'''
		code_text += '\t\tdocument.getElementById("'+i+'''").style.display = "block";
			}\n'''
	code_text += '\t};\n'
	code_text += '</script>\n'

	return code_text

def write_HTML():
	global active_number
	bank_charts = []
	csv_list = []
	mainPageGraph = ""
	for files in os.listdir("."):
		if "Bank_Account_Data_IRO" in files:
			shutil.copy(files, "iroatuva.github.io")
			bank_charts.append(files)
			if mainPageGraph == "":
				mainPageGraph = files
			else:
				date_from = mainPageGraph[22:30].split('_')
				date_from = datetime.datetime(int(date_from[2]),int(date_from[0]),int(date_from[1]))
				date_compared = files[22:30].split('_')
				date_compared = datetime.datetime(int(date_compared[2]),int(date_compared[0]),int(date_compared[1]))
				if date_compared < date_from:
					mainPageGraph = files
		# if ".csv" in files:
		# 	csv_list.append(files)
		# 	shutil.copy(files, "iroatuva.github.io")


	shutil.copy("BoFa.csv","iroatuva.github.io")
	csv_list.append("BoFa.csv") #<- this is a temporary stopgap for right now


	day = str(date.today())
	day = day.split('-')
	day = day[1] + '-' + day[2] + '-' + day[0]

	with open('BoFa.csv') as read:
		x = read.readline().split(',')[1]
		for last_line in read:
			pass
		last_line = last_line.split(',')[0]
	cur_amt = str(format(float(x),','))
	last_line = last_line.split('/')
	with open('BoFa.csv') as min_max:
		money = {}
		for line in min_max:
			line = line.replace('\n','').split(',')
			money[float(line[1])] = line[0]

	code_text = ''
	min_num = str(format(min(money),','))
	max_num = str(format(max(money),','))

	min_date = money[min(money)].split('/')
	min_date = months[int(min_date[0])] + ' ' + min_date[1] + ', ' + min_date[2]
	minimum = 'The minimal amount in the account was $' + min_num + ' on ' + min_date

	max_date = money[max(money)].split('/')
	max_date = months[int(max_date[0])] + ' ' + max_date[1] + ', ' + max_date[2]
	maximum = 'The maximal amount in the account was $' + max_num + ' on ' + max_date

	min_max = [minimum, maximum]

######################################## THE MAIN PAGE #####################################

	code_text += heading
	code_text += '<style>\n'
	code_text += 'img{border-style: double; width:100%;}\n'
	code_text += top_banner
	
	code_text += header(active_number, header_list, header_links)
	active_number += 1

	code_text += '<h1 style = "text-align:center;"> International Relations Organization at UVA\'s Data Webpage</h1>\n'
	code_text += '<h2 style = "background-color:tomato; text-align:center;"> IRO at UVA is not officially affiliated with the university</h2>\n'
	code_text += '<h2 style = "text-align:center;"> Last Updated ' + day + '</h2>\n'
	code_text += '<h2 style = "text-align:center;"> <strong> The IRO bank account has $' + str(cur_amt) + ' as of now </strong></h2>\n'
	code_text += '<h2 style = "text-align:center";> Since ' + months[int(last_line[0])] + ' ' + last_line[1] + ', ' + last_line[2] + ':</h2>\n'
	code_text += bulleted_list_maker(min_max)
	code_text += '<figure>\n'
	code_text += '<img src = "' + mainPageGraph + '" alt = "A graph of the bank account">\n'
	code_text += '<figcaption style = "text-align:center;"> The Bank Account Over Time </figcaption>\n'
	code_text += '</figure>\n'
	code_text +='</body>\n</html>'
	with open('index.html','w+',encoding = 'utf-8') as g:
		g.write(code_text)
		code_text = '' #You are now done with the main page
	shutil.move('index.html','iroatuva.github.io/index.html')
	bank_charts.remove(mainPageGraph)


################################################ THE DAY-BY-DAY DATA PAGE ############################
	selection_list = ["Bank Account Data", "Venmo Data"]
	table_titles = ["IRO Checking Account Day-By-Day Data", "Venmo Account Day-By-Day Data"]

	table_col_titles = []
	for i in range(len(selection_list)):
		table_col_titles.append(["Date", "Amount"])

	code_text += heading
	code_text += '<style>\n'
	code_text += top_banner

	code_text += header(active_number, header_list, header_links)
	active_number += 1

	code_text += '</style>\n</head>\n<body>\n'
	code_text += '<h1 style = "text-align:center;"> Tables of Raw Data</h1>\n'
	code_text += dropdown_displayer(csv_list, selection_list, table_titles, table_col_titles)
	code_text += '</body>\n</html>\n'
	with open('datapage.html','w+',encoding = 'utf-8') as f:
		f.write(code_text)
		code_text = ''
	shutil.move('datapage.html','iroatuva.github.io/datapage.html') #You are now done with the data page

######################### THERE IS NO ABOUT PAGE. TAKE OFF YOUR CLOTHES ###########################


######################## Extra charts and graphs page ##############################################
	code_text += heading
	code_text += '<style>\n'
	code_text += 'img{border-style: double; width:100%;}\n'
	code_text += top_banner
	
	code_text += header(active_number, header_list, header_links)
	active_number += 1

	code_text += '<h1 style = "text-align:center;"> Some Extra Graphs </h1>\n'
	code_text += '<h2 style = "text-align:center;"> Last Updated ' + day + '</h2>\n'
	for i in bank_charts:
		code_text += '<img src = "' + i + '" alt = "Another graph of the bank account">\n'
	code_text += '</body>\n</html>'
	with open('charts.html', 'w+', encoding = 'utf-8') as f:
		f.write(code_text)
		code_text = ''
	shutil.move('charts.html','iroatuva.github.io/charts.html')


################## Branches page ####################################
	code_text += heading
	code_text += '<style>\n'
	code_text += top_banner

	code_text += header(active_number, header_list, header_links)
	active_number += 1

	code_text += '<h1 style="text-align:center";> There is no information specific to a branch of IRO that can be posted right now </h1>\n'
	code_text += '</body>\n</html>'

	with open('branch.html', 'w+', encoding = 'utf-8') as f:
		f.write(code_text)
		code_text = ''
	shutil.move('branch.html','iroatuva.github.io/branch.html')


################# Code hosting part of the website just redirects to the github site ####################



write_HTML()
#print(dropdown_displayer(["BoFa.csv"],["Bank of America Data", "Venmo Data"], ["Bank of America Data", "Venmo Data"], [["Date", "Amount"], ["Date", "Amount"]]))

shutil.copy("website_designer.py", "iroatuva.github.io")