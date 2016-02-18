from pssh import ParallelSSHClient
import configparser
import paramiko
import argparse

"""
Author - Greg McCoy

Date - Feburary 18th 2016

Description - Runs commands through shh on  mulitple clients provided
in the hosts file.
"""
config = configparser.ConfigParser()

def connect(cmd):
    hosts = None
    try:
        with open(readConf('host_file')) as f:
            hosts = f.read().splitlines()
    except IOError as e:
        print("Can't open host file:" + str(e))
        return
    f.close()
    print("Excuting on servers:\n")
    for host in hosts:
        print(host)
    option = raw_input("\ncontinue? y/n: ")
    if option == "y":
        client_key = paramiko.RSAKey.from_private_key_file(readConf('key'))
        client = ParallelSSHClient(hosts, user="ubuntu", pkey=client_key)
        command(client,cmd)
    else:
        print("Aborting")


def command(client, cmd):
    output = client.run_command(cmd)
    for host in output:
        for line in output[host]['stdout']:
            print("Host: %s - Output: %s" % (host, line))


def readConf(option):
	config.read("gfa-pssh.conf")
	value = config['GENERAL'][option]
	return(value)


parser = argparse.ArgumentParser()
parser.add_argument(dest='input', help="Enter command to execute")
args = parser.parse_args()
if args.input == None:
    parser.print_help()
else:
    connect(args.input)
