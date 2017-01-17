from flask import Flask, render_template,request,flash,redirect,url_for, Markup
from collections import defaultdict
from datetime import datetime as dt
import mysql.connector as mariadb
import datetime
import random

app = Flask(__name__)

def auto(cursor,mariadb_connection,user,manager,mode,message,today):
	added=0
	density=[]
	tavail=[]
	options=[12,13,11,14,10,15]

	cursor.execute('''SELECT HOUR(StartTime) AS Hour, count(*) AS Density FROM smblinux WHERE DATE(EndTime) = DATE(NOW()) AND Mode = "%s" GROUP BY HOUR(StartTime) HAVING Density > 1 ORDER BY Density ASC;''' % (mode))
	if cursor.rowcount:
		for row in cursor:
			density.append([row[0],row[1]])
			tavail.append(row[0])
		for sOption in options:
			if sOption not in tavail and added != 1:
				added=1
				stime= str(today) + ' ' + str(sOption) + ':00:00'
				etime= str(today) + ' ' + str(sOption+1) + ':00:00'

		if added == 0:
			stime= str(today) + ' ' + str(density[0][0]) + ':00:00'
			etime= str(today) + ' ' + str(density[0][0]+1) + ':00:00'
			
	else:
		seed = random.randrange(11,14)
		stime = str(today) + ' ' + str(seed) + ':00:00'
		etime = str(today) + ' ' + str(seed + 1) + ':00:00'		


	cursor.execute('''INSERT INTO smblinux (Name, Manager, StartTime, EndTime, Mode) VALUES (%s, %s, %s, %s, %s);''', (user, manager, stime, etime, mode))
	mariadb_connection.commit()
	message += 'Racker: ' + user + ' -- Successfully auto-added between ' + stime + ' and ' + etime 


	return dataGet(cursor,message)

def range(tlist):
	masterlist=[]
	tmplist=[]
	rlist=[]

	for row in tlist:
		rlist.append(row[0])
	rset = set(rlist)

	while rset:
		tmplist=[]
		value = rset.pop()
		tmplist.append(value)
		for row in tlist:
        	        if row[0] == value:
                        	tmplist.append(row[1])

	        masterlist.append(tmplist)

	return masterlist


def warnings(cursor):

	#This is messy. I couldn't think of a good way to do this
	times = ['08:00', '08:10', '08:20', '08:30', '08:40' , '08:50', '09:00', '09:10', '09:20', '09:30', '09:40', '09:50', '10:00', '10:10', '10:20', '10:30', '10:40', '10:50', '11:00', '11:10', '11:20', '11:30', '11:40', '11:50', '12:00', '12:10', '12:20', '12:30', '12:40', '12:50', '13:00', '13:10', '13:20', '13:30', '13:40', '13:50', '14:00', '14:10', '14:20', '14:30', '14:40', '14:50', '15:00', '15:10', '15:20', '15:30', '15:40', '15:50', '16:00', '16:10', '16:20', '16:30', '16:40', '16:50', '17:00' ]

	JoeOverlapArray=[]
	SteffenOverlapArray=[]
	StaceyOverlapArray=[]
	ChatOverlapArray=[]

        JoeArray=[]
        SteffenArray=[]
        StaceyArray=[]
	ChatArray=[]

	warningString=''
	

	cursor.execute('''SELECT Name, StartTime, EndTime, Manager FROM smblinux WHERE Mode='phones' and DATE(EndTime) = DATE(NOW()) ORDER BY StartTime;''')
	if cursor.rowcount:
		for row in cursor:
			if row[3] == 'Joe K':
				JoeArray.append([ row[0], row[1], row[2]  ])
			elif row[3] == 'Steffen H':
				SteffenArray.append([ row[0], row[1], row[2] ])
			elif row[3] == 'Stacey F':
				StaceyArray.append([ row[0], row[1], row[2] ])

		for t in times:
			t = dt.strptime( str(datetime.date.today()) + ' ' + t + ':01', "%Y-%m-%d %H:%M:%S")
			JoeCount=0
			SteffenCount=0
			StaceyCount=0
			for row in JoeArray:
				if row[1] <= t <= row[2]:
					JoeCount+=1
			if JoeCount > 2:
				JoeOverlapArray.append([JoeCount,t])

                        for row in SteffenArray:
                                if row[1] <= t <= row[2]:
                                        SteffenCount+=1
			if SteffenCount > 2:
                        	SteffenOverlapArray.append([SteffenCount,t])

                        for row in StaceyArray:
                                if row[1] <= t <= row[2]:
                                	StaceyCount+=1
			if StaceyCount > 2:
                        	StaceyOverlapArray.append([StaceyCount,t])
				

		JoeOverlapArray = range(JoeOverlapArray)
		for row in JoeOverlapArray:	
			n=0
			while n < len(row):
				if n == 0:
					warningString += str(row[n]) + ' <i>Watchdog</i> phone Rackers out at '
				elif n+1 != len(row):
					warningString += str(row[n].strftime('%I:%M %p')) + ', ' 
				else: 
					warningString += 'and ' + str(row[n].strftime('%I:%M %p')) + '</br>'
				n+=1

                SteffenOverlapArray = range(SteffenOverlapArray)    
                for row in SteffenOverlapArray:    
                        n=0 
                        while n < len(row):
                                if n == 0:
                                        warningString += str(row[n]) + ' <i>Spattlecock</i> phone Rackers out at '
                                elif n+1 != len(row):
                                        warningString += str(row[n].strftime('%I:%M %p')) + ', ' 
                                else: 
                                        warningString += 'and ' + str(row[n].strftime('%I:%M %p')) + '</br>'
                                n+=1

                StaceyOverlapArray = range(StaceyOverlapArray)
                for row in StaceyOverlapArray:
                        n=0
                        while n < len(row):
                                if n == 0:
                                        warningString += str(row[n]) + ' <i>Pork Chop Express</i> phone Rackers out at '
                                elif n+1 != len(row):
                                        warningString += str(row[n].strftime('%I:%M %p')) + ', '
                                else:
                                        warningString += 'and ' + str(row[n].strftime('%I:%M %p')) + '</br>'
                                n+=1


	cursor.execute('''SELECT Name, StartTime, EndTime, Manager FROM smblinux WHERE Mode='chats' and DATE(EndTime) = DATE(NOW()) ORDER BY StartTime;''')
	if cursor.rowcount:
		for row in cursor:
			ChatArray.append([ row[0], row[1], row[2] ])
		for t in times:
			ChatCount=0
			t = dt.strptime( str(datetime.date.today()) + ' ' + t + ':01', "%Y-%m-%d %H:%M:%S")	
			for row in ChatArray:
				if row[1] <= t <= row[2]:
					ChatCount+=1
			if ChatCount > 1:
				ChatOverlapArray.append([ChatCount,t])
		if len(ChatOverlapArray) > 0:	
			warningString += "Chat Racker's breaks overlap </br>"

	myFile = open('/var/log/flask.log', 'a')
	myFile.write(str(SteffenOverlapArray))

	return warningString

def dataGet(cursor,message):

       #Data Structures
	defaultList=['', '']
	dataSet=defaultdict(lambda: defaultList )
	modeArray=[]
	iteration=0

        #Get available Modes to determine interation count
        cursor.execute('''select DISTINCT(Mode) from smblinux WHERE DATE(EndTime) = DATE(NOW()) ORDER BY Mode;''')
        for row in cursor:
                modeArray.append(str(row[0]))

	while iteration <= len(modeArray):

	        timesArray=[]
		dataArray=[]
	
 	        if iteration == len(modeArray):
        		cursor.execute('''SELECT * FROM smblinux WHERE DATE(EndTime) = DATE(NOW()) ORDER BY StartTime,Manager;''')
			if not cursor.rowcount:
				categories=""
			else:
				categories="categories: ["
	        		for row in cursor:
       	        			timesArray.append([ row[0], row[1], row[2], row [3], row[4] ])
			key="composit"
		else:
                        cursor.execute('''SELECT * FROM smblinux WHERE DATE(EndTime) = DATE(NOW()) and Mode = "%s" ORDER BY StartTime,Manager;''' % (modeArray[iteration]))
			if not cursor.rowcount:
				categories=""
			else:
				categories="categories: ["
                        	for row in cursor:
                                	timesArray.append([ row[0], row[1], row[2], row [3], row[4] ])
			key=str(modeArray[iteration])


		count=0
	        data=""
		for rackerArray in timesArray:
			lowT = str(rackerArray[2]).split()[1].split(':')
                	highT = str(rackerArray[3]).split()[1].split(':')
                	lowD = str(rackerArray[2]).split()[0].split('-')
                	highD = str(rackerArray[3]).split()[0].split('-')

			#Colors
			if rackerArray[1] == "Joe K":

# Joe's Color Scheme
#				color = "#5d6d7e"
#				if iteration == len(modeArray):
#					if rackerArray[4] == "chats":
#						color = "#7e5d6d"
#					if rackerArray[4] == "tickets":
#						color = "#5d7e6e"
#					if rackerArray[4] == "alerts":
#						color = "#7e6e5d"
#End Joe'S Color Scheme
#Campfire Color Scheme
                                color = "#588C7E"
                                if iteration == len(modeArray):
                                        if rackerArray[4] == "chats":
                                                color = "#F2AE72"
                                        if rackerArray[4] == "tickets":
                                                color = "#F2E394"
                                        if rackerArray[4] == "alerts":
                                                color = "#8C4646"
					if rackerArray[4] == "other":
						color = "#081B2D"
#End Campfire Color Scheme
			elif rackerArray[1] == "Steffen H":
				color = "#43566A"
                                if iteration == len(modeArray):
                                        if rackerArray[4] == "chats":
                                                color = "#5C3F4D"
                                        if rackerArray[4] == "tickets":
                                                color = "#436856"
                                        if rackerArray[4] == "alerts":
                                                color = "#4A3F32"

			elif rackerArray[1] == "Stacey F":
				color = "#2B3C4E"
                                if iteration == len(modeArray):
                                        if rackerArray[4] == "chats":
                                                color = "#482335"
                                        if rackerArray[4] == "tickets":
                                                color = "#284939"
                                        if rackerArray[4] == "alerts":
                                                color = "#4A3520"

			else:
				color = "#081B2D"

			data = data + "{x: " + str(count) + ", low: Date.UTC(" + str(lowD[0]) + ", " + str(lowD[1]) + ", " + str(lowD[2]) + ", " + str(lowT[0]) + ", " + str(lowT[1]) + "), high: Date.UTC(" + str(highD[0]) + ", " + str(highD[1]) + ", " + str(highD[2]) + ", " + str(highT[0]) + ", " + str(highT[1]) + "), name: " + '"' + str(rackerArray[0]) + '", color: "' + color + '"}'

                	count+=1
                	if count == len(timesArray):
                        	categories=categories+"'"+str(rackerArray[0])+"']"
                	else:
                        	categories=categories+"'"+str(rackerArray[0])+"',"
                        	data = data + ','

		dataArray.append(data)
		dataArray.append(categories)
		dataSet[key]= dataArray

		iteration+=1
	
	return dataSet, message



def dataSet(cursor,mariadb_connection,user,manager,stime,etime,mode,message):

	#Sanitize some inputs before submitting
	s = dt.strptime( stime , "%Y-%m-%d %H:%M:%S")
	e = dt.strptime( etime , "%Y-%m-%d %H:%M:%S")

	oldSTime=[]
	oldETime=[]

	cursor.execute('''SELECT DISTINCT(Mode), StartTime, EndTime FROM smblinux WHERE DATE(EndTime) = DATE(NOW()) and Name = "%s";''' % (user))

	if not cursor.rowcount:    	
		if e > s:
			cursor.execute('''INSERT INTO smblinux (Name, Manager, StartTime, EndTime, Mode) VALUES (%s, %s, %s, %s, %s);''', (user, manager, stime, etime, mode))
			mariadb_connection.commit()
			if not cursor.rowcount:
				message += 'Unable to add - Honestly I do not know why'
			else:
				message += 'Racker: ' + user + ' -- Successfully added between ' + stime + ' and ' + etime
		else:
			message += 'End time must be after Start time'
	else:
		for row in cursor:
			oldMode=row[0]
			oldSTime.append(row[1])
			oldETime.append(row[2])
		if oldMode != mode:
			message += "You can't add another break using a different mode (phone, chat, ticket, etc.) than the break already submitted"
		elif s in oldSTime and e in oldETime:
			message += "You already have that break slot.."
		elif e < s:
			message += 'End time must be after Start time'
		else:
			cursor.execute('''INSERT INTO smblinux (Name, Manager, StartTime, EndTime, Mode) VALUES (%s, %s, %s, %s, %s);''', (user, manager, stime, etime, mode))
        		mariadb_connection.commit()

       			if not cursor.rowcount:
                		message += 'Unable to add - Honestly I do not know why'
			else:
				message += 'Racker: ' + user + ' -- Successfully added between ' + stime + ' and ' + etime 
			

	return dataGet(cursor,message)

def dataDel(cursor,mariadb_connection,user,manager,stime,etime,mode,message):
	
	if stime == 'auto' or etime == 'auto':
		cursor.execute('''DELETE FROM smblinux WHERE Name = %s and Manager = %s and Mode = %s;''', (user, manager, mode))
		mariadb_connection.commit()
	else:
		cursor.execute('''DELETE FROM smblinux WHERE Name = %s and Manager = %s and StartTime = %s and EndTime = %s and Mode = %s;''', (user, manager, stime, etime, mode))
		mariadb_connection.commit()

	if not cursor.rowcount:
		message += 'Unable to delete - selected entry does not exist'	
	elif stime == 'auto' or etime == 'auto':
		message += 'Racker: ' + user + ' -- Successfully removed all occurances'
	else:
		message += 'Racker: ' + user + ' -- Successfully removed between ' + stime + ' and ' + etime
 
        return dataGet(cursor,message)


@app.route("/", methods=['GET','POST'])
def lunch():

	#Defining Static Data
	#Teams	
	JoeK = ['Joe S', 'Matt V', 'Grace T', 'Pam L', 'Marcos T', 'Carlos S', 'Jim C', 'Lee N', 'Tim M', 'Uwe N']
	SteffenH = ['Anthony D', 'Brandon B', 'Jessica W', 'Mike Herrera', 'Mike Hernandez', 'Pete E', 'Rebecca S', 'Travis H']
	StaceyF = ['Eddie D', 'Aubrey M', 'Chris H', 'Joe A', 'Josh H', 'Mallory H', 'Mohammed A', 'Tom H']
	#Dates
	today =	datetime.date.today()

	#MySQL connection
	mariadb_connection = mariadb.connect(user='smblinux', password='OTlmYTM3ZmY1MmY', database='lunch_schedule')
	cursor = mariadb_connection.cursor(buffered=True)
	#Messages and Warnings
	message=''
	errorOut=''



	if request.method == 'POST':
		#Grab user
        	user = str(request.form.getlist('Name')[0])
		#Sanitize user
		if (user not in JoeK) and (user not in SteffenH) and (user not in StaceyF):
			errorOut+=" Error: Did not find Manager"

		if str(request.form.getlist('Start Time')[0]) == 'auto':
			stime='auto'
		else:			
			stime = str(today) + ' ' + str(request.form.getlist('Start Time')[0])

		if str(request.form.getlist('End Time')[0]) == 'auto':
			etime='auto'
		else:
			etime = str(today) + ' ' + str(request.form.getlist('End Time')[0])

                #Sanitize times
                times = ['8:00:00', '8:30:00', '9:00:00', '9:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00', '16:30:00', '17:00:00', '17:30:00', '18:00:00', 'auto']
                if (str(request.form.getlist('Start Time')[0]) not in times) or (str(request.form.getlist('End Time')[0]) not in times):
                        errorOut+=" Error: Times did not pass validity check "

		mode = str(request.form.getlist('Mode')[0])
		
		#Sanitize mode
		modes=['phones','chats','tickets','alerts','other']
		if mode not in modes:
			errorOut+="Error: Mode not found"

		action = str(request.form.getlist('Action')[0])

		#Sanitize action
		actions=['add','remove']
		if action not in actions:
			errorOut+=" Error: Mode not found"

		if user in JoeK:
			manager="Joe K"
		elif user in SteffenH:
			manager="Steffen H"
		elif user in StaceyF:
			manager="Stacey F"
		else:
			manager="null"

		if action == 'add' and len(errorOut) == 0:
			if stime == 'auto' or etime == 'auto':
				alldata, message = auto(cursor,mariadb_connection,user,manager,mode,message,today)
			else:
				alldata, message = dataSet(cursor,mariadb_connection,user,manager,stime,etime,mode,message)
		elif action == 'remove' and len(errorOut) == 0:
			alldata, message  = dataDel(cursor,mariadb_connection,user,manager,stime,etime,mode,message)
		else:
			message = "Data did not pass validity check. We received - Name: " + str(user) + " Start Time: " + str(stime) + " End Time: " + str(etime) + " Mode : " + str(mode) + " Action: " + str(action) + "Errors -- " + errorOut
			alldata, message = dataGet(cursor,message)
		
		return render_template('lunch.html', compData=alldata['composit'][0], compCategories=alldata['composit'][1], phoneData=alldata['phones'][0], phoneCategories=alldata['phones'][1], chatData=alldata['chats'][0], chatCategories=alldata['chats'][1], ticketData=alldata['tickets'][0], ticketCategories=alldata['tickets'][1], alertData=alldata['alerts'][0], alertCategories=alldata['alerts'][1], otherData=alldata['other'][0], otherCategories=alldata['other'][1], message=message, warning=warnings(cursor))
	else:
		alldata, message = dataGet(cursor,message)
		return render_template('lunch.html', compData=alldata['composit'][0], compCategories=alldata['composit'][1], phoneData=alldata['phones'][0], phoneCategories=alldata['phones'][1], chatData=alldata['chats'][0], chatCategories=alldata['chats'][1], ticketData=alldata['tickets'][0], ticketCategories=alldata['tickets'][1], alertData=alldata['alerts'][0], alertCategories=alldata['alerts'][1], otherData=alldata['other'][0], otherCategories=alldata['other'][1], message=message, warning=warnings(cursor))


@app.route("/about", methods=['GET'])
def about():
	return render_template('about.html')


if __name__ == "__main__":
	app.run(debug=True)
	app.run()
