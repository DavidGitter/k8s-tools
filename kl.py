import os
import sys
import configparser

#os.system("cls")

def print_txt_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                print(file_path)

settingsPath = "<my-path-to-kube-config-files>" # enter a folder path for kl to use for kube confs and settings
iniPath = settingsPath + "settings.ini"

config = configparser.ConfigParser() #config file
config.read(iniPath)
currNS = "-n " + config["ns_conf"]["currentNamespace"] + " "

currConf = " --kubeconfig=" + config["kube_conf"]["currentkubeconf"] + " "
first = "kubectl "+currConf

if(len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "help")):
    print("___kubectl shortcut tool 'kl' by Silas Jung___")
    print("{:<10} {:<15} {:<1}".format('COMMAND', ' ', 'USE'))
    print("{:<10} {:<15} {:<1}".format('g <args>', ' ', 'shortcut for get'))
    print("{:<10} {:<15} {:<1}".format('a <args>', ' ', 'shortcut for apply'))
    print("{:<10} {:<15} {:<1}".format('dc <args>', ' ', 'shortcut for describe'))
    print("{:<10} {:<15} {:<1}".format('dl <args>', ' ', 'shortcut for delete'))
    print("{:<10} {:<14} {:<1}".format('kill <args>', ' ', 'shortcut for hard delete'))
    print("{:<10} {:<15} {:<1}".format('ns', ' ', 'shows current namespace scope'))
    print("{:<10} {:<15} {:<1}".format('ns <name>', ' ', 'changes namespace scope to given name'))
    print("{:<10} {:<15} {:<1}".format('conf', ' ', 'shows current kube config file used and all available in the ini folder'))
    print("{:<10} {:<10} {:<1}".format('conf <confPath>', ' ', 'changes conf file to given conf file path'))

elif(sys.argv[1] == "g"):
    os.system(first + " get " + currNS + " ".join(sys.argv[2:len(sys.argv)]))

elif(sys.argv[1] == "dc"):
    os.system(first + " describe " + currNS + " ".join(sys.argv[2:len(sys.argv)]))

elif(sys.argv[1] == "dl"):
    os.system(first + " delete " + currNS + " ".join(sys.argv[2:len(sys.argv)]))

elif(sys.argv[1] == "kill"):
    os.system(first + " delete " + currNS + " ".join(sys.argv[2:len(sys.argv)]) + " --force --grace-period=0")

elif(sys.argv[1] == "a"):
    os.system(first + " apply " + currNS + " ".join(sys.argv[2:len(sys.argv)]))

elif(sys.argv[1] == "ns"):
    if(len(sys.argv) == 2):
        print(config["ns_conf"]["currentNamespace"])
    elif(len(sys.argv) == 3):
        config = configparser.ConfigParser() #config file
        config.read(iniPath)
        config["ns_conf"] = { "currentNamespace": sys.argv[2] }
        with open(iniPath, 'w') as configfile:
            config.write(configfile)
        print("namespace switch: " + sys.argv[2])

elif(sys.argv[1] == "conf"):
    if(len(sys.argv) == 2): #print current conf file and available once at the folder of the ini file
        print("--Currently Used Config--")
        print(config["kube_conf"]["currentkubeconf"])
        print("--Found Available Configs--")
        print_txt_files(settingsPath)
    elif(len(sys.argv) == 3): #change conf to given param
        config = configparser.ConfigParser()
        config.read(iniPath)
        config["kube_conf"] = { "currentkubeconf": sys.argv[2] }
        with open(iniPath, 'w') as configfile:
            config.write(configfile)
        print("kubeconfig switch: " + sys.argv[2])

else:
    os.system(first + currNS + " ".join(sys.argv[1:len(sys.argv)]))
