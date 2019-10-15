import os

directory_to_check = "/usr/src/app/EXTERNALDATA/get_it_aziende/"

def importer(i):
	cwd = os.getcwd()
	nome_azienda = os.path.basename(cwd)
	os.system("bash /usr/src/app/manage.sh importlayers " + "-u" + " " + str(nome_azienda) + " -p" + " " + i)
	print (i)
	print (nome_azienda)
	
directories = [os.path.abspath(x[0]) for x in os.walk(directory_to_check)]
directories.remove(os.path.abspath(directory_to_check)) # If you don't want your main directory 

for i in directories:
	os.chdir(i) # Change working Directory
	importer(i)
