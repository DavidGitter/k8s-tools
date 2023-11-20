#short alias for "helm ...."

import sys
import os
import configparser

os.system("cls")

iniPath = "<path/to/settings.ini>" # enter a folder path for kl to use for kube confs and settings

config = configparser.ConfigParser() #config file
config.read(iniPath)
currConf = " --kubeconfig=" + config["kube_conf"]["currentkubeconf"] + " "

if(sys.argv[1] == "u"): #uninstall
    os.system("helm uninstall " + " ".join(sys.argv[2:len(sys.argv)]) + currConf)
elif(sys.argv[1] == "i"): #install
    os.system("helm install " + " ".join(sys.argv[2:len(sys.argv)]) + currConf)
elif(sys.argv[1] == "conf"):
    if(len(sys.argv) == 2):
        print(config["kube_conf"]["currentkubeconf"])
    elif(len(sys.argv) == 3):
        config = configparser.ConfigParser() #config file
        config.read(iniPath)
        config["kube_conf"] = { "currentkubeconf": sys.argv[2] }
        with open(iniPath, 'w') as configfile:
            config.write(configfile)
        print("kubeconfig switch: " + sys.argv[2])
else:
    os.system("helm " + " ".join(sys.argv[1:len(sys.argv)]) + currConf)

