#to exec from host: docker-compose exec django python ./import.py
import os
import subprocess
from datetime import datetime
import shutil

directory_to_check = "/usr/src/app/EXTERNALDATA/get_it_aziende/"


def importer(i):
    cwd = os.getcwd()
    nome_azienda = os.path.basename(cwd)
    now = datetime.now()
    startime = now.strftime("%d/%m/%Y %H:%M:%S")
    print ("--- start " + nome_azienda + " ---")
    print ("percorso directory" + " " + i)
    print ("data e ora inizio" + " " + startime) 
    print ("inizio importazione dell'azienda" + " " + nome_azienda)
    importazione = ("bash", "/usr/src/app/manage.sh", "importlayers", "-v 3","-u",nome_azienda,"-p", i)
    returned_value = subprocess.Popen(importazione, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #output = returned_value.communicate()
    stdout, stderr = returned_value.communicate()
    #errore = returned_value.stderr.read()
    #errore = subprocess.check_output(output)
    print (stdout)
    print (stderr)
    #print(returned_value.stderr.read())
    #os.system("bash /usr/src/app/manage.sh importlayers " + "-v 3" + " " + "-u" + " " + str(nome_azienda) + " -p" + " " + i) #deprecato
    for file in os.listdir(i):
        ext = [".zip", ".shp", ".tif", ".sld"]
        if file.endswith(tuple(ext)):
            dataset = (os.path.join(i, file))
            importpath = (os.path.join("/usr/src/app/EXTERNALDATA/imported/", nome_azienda))
            shutil.copy(dataset, importpath) #se voglio muovere i file
            print ("dato archiviato " + importpath + "/" + file)
            os.remove(dataset)
        else:
#           shutil.copy(dataset, importpath)
            print ("dato non archiviato " + i + "/" + file)
    end = datetime.now()
    endtime = end.strftime("%d/%m/%Y %H:%M:%S")
    print ("data e ora fine" + " " + endtime)
    print ("--- end " + nome_azienda + " ---")

directories = [os.path.abspath(x[0]) for x in os.walk(directory_to_check)]
directories.remove(os.path.abspath(directory_to_check)) # per non includere la dir principale

for i in directories:
	os.chdir(i) # Change working Directory
	importer(i)
