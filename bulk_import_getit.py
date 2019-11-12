#to exec from host: docker-compose exec django python ./import.py
import os
from datetime import datetime

directory_to_check = "/usr/src/app/EXTERNALDATA/get_it_aziende/"


def importer(i):
	cwd = os.getcwd()
	nome_azienda = os.path.basename(cwd)
	now = datetime.now()
	startime = now.strftime("%d/%m/%Y %H:%M:%S")
	print ("--- start " + nome_azienda + " ---")
	print ("percorso directory" + " " + i)
	print ("data e ora inizio" + " " + startime) 
#	print ("inizio importazione dell'azienda" + " " + nome_azienda)
	os.system("bash /usr/src/app/manage.sh importlayers " + "-v 3" + " " + "-u" + " " + str(nome_azienda) + " -p" + " " + i)
	end = datetime.now()
	endtime = end.strftime("%d/%m/%Y %H:%M:%S")
	print ("--- end " + nome_azienda + " ---")
	print ("data e ora fine" + " " + endtime)
#	print ("fine importazione dell'azienda" + " " + nome_azienda)

directories = [os.path.abspath(x[0]) for x in os.walk(directory_to_check)]
directories.remove(os.path.abspath(directory_to_check)) # If you don't want your main directory 

for i in directories:
	os.chdir(i) # Change working Directory
	importer(i)
