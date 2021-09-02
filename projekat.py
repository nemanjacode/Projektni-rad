
import os
import sys
import psutil
import win32serviceutil
import subprocess
import urllib.request
import getpass


# Definisanje funkcije koja vrsi download instalacionog java fajla sa zvanicnog sajta

def download (url, filename):
    opener=urllib.request.build_opener()
    download_fajl=opener.open(url)
    with open (filename, 'wb+') as save:
        save.write(download_fajl.read())


# Definisanje funkcije za pronalazenje windows servisa u services.msc

def getService(name): 
        service = None 
        try: 
            service = psutil.win_service_get(name) 
            service = service.as_dict() 
        except Exception as ex: 
            print (str(ex))
        return service 

# Otvaranje i citanje tekstualnog dokumenta sa korisnickim kredencijalima

with open('user.txt', 'r') as admin_korisnici:
    user = admin_korisnici.readline().strip()
    password = admin_korisnici.readline().strip()

# Provera da li se uneti korisnicki kredencijali podudaraju sa unapred sacuvanim kredencijalima

if input("Korisnicko ime: ") == user and getpass.getpass("Password: ") == password:

# Proverava spisak instaliranih programa i upisuje ih u apps.txt dokument

    fajl_apps = open('C:\\apps.txt', 'w')
    Data = subprocess.check_output(['wmic', 'product', 'get', 'name',',','IdentifyingNumber'])
    a = str(Data)

    try:
        for i in range(len(a)):
            print(a.split("\\r\\r\\n")[6:][i], file=fajl_apps)
    except IndexError as e:
        print()
    fajl_apps.close()


# Proverava da li se u spisku instaliranih programa nalazi Java

    with open('C:\\apps.txt', 'r') as f:
        if 'Java' in f.read():
            print("Vas racunar ima javu")
            n=input (f"\nUkoliko zelite da nastavite sa instalacijom pritisnite taster Y \nU suprotnom pritisnite bilo koji taster: ")
            if n=="Y" or n=="y":
                print("\nNastavljamo sa procesom update-ovanja Jave. \nMolimo za malo strpljenja.\n\n")
            else:
                print("\nZao nam je sto ste odustali od procesa update-ovanja Jave. \nMolimo Vas da u skorijoj buducnosti update-ujete Javu.\n\n")
                exit(1)
        else:
            print ("\nVas racunar nema Javu. Proces update-ovanja Jave se prekida.")
            exit(2)

# Otvaranje log fajla 

    log_fajl= open('C:\\log_fajl.txt','w')

# Stopiranje windows servisa u services.msc
# Provera da li Tomcat servis postoji na hostu

    service = getService('Themes')  
    print (service) 
    if service: 
            print ("Tomcat service found",file=log_fajl) 
    else: 
            print ("Tomcat service not found",file=log_fajl) 
    
# Provera da li je Tomcat servis u running statusu i stopiranje samog servira ukoliko jeste

    if service and service['status'] == 'running' : 
            serviceName = "Themes"
            win32serviceutil.StopService(serviceName)
            print ("Tomcat service was running",file=log_fajl) 
    else : 
            print ("Tomcat service is not running",file=log_fajl)

# Provera da li Jenkins servis postoji na hostu

    service = getService('Jenkins') 
    print (service) 
    if service: 
            print ("Jenkins service found",file=log_fajl) 
    else: 
        print ("Jenkins service not found",file=log_fajl) 
    
# Provera da li je Jenkins servis u running statusu i stopiranje samog servira ukoliko jeste

    if service and service['status'] == 'running': 
            serviceName = "Jenkins"
            win32serviceutil.StopService(serviceName)
            print ("Jenkins service was running",file=log_fajl) 
    else : 
            print ("Jenkins service is not running",file=log_fajl)

# Provera da li je instalirana najnovija verzija Jave update 301
    
    with open('C:\\apps.txt', 'r') as f:
        if 'Update 301' in f.read():
            print("\nVas racunar ima najnoviju verziju jave instaliranu\n")

        else:
# Pozivanje download fukncije zbog downloadovanja instalacionog fajla 
 
            url='https://javadl.oracle.com/webapps/download/AutoDL?BundleId=245060_d3c52aa6bfa54d3ca74e617f18309292'
            filename='jre-8u301-windows-x64.exe'
            download(url,filename)

# Instaliranje jave
            os.system ('jre-8u301-windows-x64.exe /s')      

# Provera i upis u java_apps fajl svih verzija Jave i njenih odgovarajucih ID-eva, sa izuzetkom najnovije verzije Jave update 301

    with open('C:\\apps.txt', 'r') as f:
        with open('C:\\java_apps.txt', 'w') as fja:
            for line in f:
                if 'Java' in line and 'Update 301' not in line:
                    fja.write(line)

# Kreiranje liste ids

    ids = []
    with open('C:\\java_apps.txt', 'r') as f:
        for line in f:
            ids.append(line.split(' '))

    ids_true = []
    for clan in ids:
        ids_true.append(clan[0])

# Upisivanje samo ID-eva koji imaju stariju verziju jave

    with open ('C:\\ids.txt', 'w') as f:
        for clan in ids_true:
            f.write(clan)
            f.write('\n')

# Citanje ID-eva iz liste i pozivanje uninstalacije na osnovu ID-a jave

    fajl_ids = open('C:\\ids.txt', 'r')
    Lines = fajl_ids.readlines()
    for line in Lines:
        subprocess.call (f"msiexec.exe /quiet /x {line.strip()}")
    fajl_ids.close()

# Ponovno pokretanje Tomcat servisa

    service = getService('Themes')
    if service and service['status'] == 'stopped': 
            win32serviceutil.StartService('Themes')

# Ponovno pokretanje Jenkins servisa

    service = getService('Jenkins') 
    if service and service['status'] == 'stopped': 
            win32serviceutil.StartService('Jenkins')


    log_fajl.close()
   
    
    
    print ("\nUspesno ste update-ovali Vasu Javu!\nVase okruzenje je bezbedno i nema ranjivosti vezane za Java release update.\n")
    

    
else:
    print ("\nPogresno uneti kredencijali! \nSamo autorizovani korisnici mogu da izvrse ove promene na racunaru!")




















