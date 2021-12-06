#!/usr/bin/env python3

import sys
import paramiko
import importlib.util
import config
import requests

apiTokenFile = sys.argv[1]
configFile = sys.argv[2]
queriedFile = sys.argv[3]
URL = sys.argv[4]

spec = importlib.util.spec_from_file_location("config", configFile)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

hostname = config.CONFIG_PATHS['hostname']
username = config.CONFIG_PATHS['username']
password = config.CONFIG_PATHS['password']
port = config.CONFIG_PATHS['port']

def main():
    transport = paramiko.Transport((hostname,port))
    transport.connect(username = username, password = password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    infile = open(queriedFile, 'r')
    lines = infile.readlines()
    for line in lines[1:]:
        sline = line.strip()
        sline = line.strip('\t')
        sline = line.split(',')
        sline[-1]  =  sline[-1].strip()
        filePath = sline[0]
        UUID = sline[1]
        try:
            fileattr = sftp.lstat(filePath)
            size = str(fileattr.st_size)
            Update_LIMS(UUID,size)
        except FileNotFoundError:
            print("File path:", filePath, "does not exist.")
    
def Update_LIMS(UUID,size):
    putURL = '{}/{}'.format(URL,UUID)
    infile = open(apiTokenFile, 'r')
    myToken = infile.read().replace('\n', '')
    headers = {'Authorization': myToken,
    }
    data = {'FileSize':size}
    #data = {'FileSize':'Test'}
    requests.put(putURL, headers=headers, data=data)
  
if __name__ == '__main__':
    main()
