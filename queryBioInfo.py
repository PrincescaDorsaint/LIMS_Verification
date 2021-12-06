#!/usr/bin/env python3

import sys
import os
import requests

apiTokenFile = sys.argv[1]
URL = sys.argv[2]

if not os.path.isfile(apiTokenFile):
    print("File {} does not exist. Exiting...".format(apiTokenFile))
    sys.exit()

def main():
    infile = open(apiTokenFile, 'r')
    myToken = infile.read().replace('\n', '')
    headers = {'Authorization': myToken,
    }
    response = requests.get(URL, headers=headers)
    data = response.json()
    
    queried = open('queriedBioInfo.csv', 'w', newline='\n')
    queried.write("Filepath,UUID\n")

    for key in data['resultList']:
        if key['fields']['Source'] == "SCU":
            create_queried_csv(queried, key['fields']['Filepath'], key['fields']['UUID'])
    queried.close()

def create_queried_csv(csv, Filepath, UUID):
    csv.write(f"{Filepath},{UUID}\n")
    
               
if __name__ == '__main__':
    main()
