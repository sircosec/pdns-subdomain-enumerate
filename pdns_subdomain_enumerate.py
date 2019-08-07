#!/usr/bin/python

import argparse
import pypdns
from sys import exit

parser =  argparse.ArgumentParser()
parser.add_argument("-d", "--domain", help="pass in a single domain")
parser.add_argument("-if", "--input_file", help="accept file input")
parser.add_argument("-of", "--output_file", help="pass results to output file")
parser.add_argument("--debug", help="debug mode", action='store_true')
args = parser.parse_args()

#DEBUG: print(args)

# add your username and api key/password
# request an api key from: info [ at ] circl [ dot ] lu
username = ""
password = ""

def query(domain):
    x = pypdns.PyPDNS(basic_auth=(username,password))
    #print(x.query(domain))
    return x.query(domain)

def infile_no_outfile():
    infile = args.input_file
    with open(infile) as infile:
        for line in infile:
            domain = str.strip(line)
            print("[*] root domain: " + domain)
            results = query(domain)
            for result in results:
                timestamp = result['time_last']
                print('     ' + str(timestamp.year) + '-' + str(timestamp.month) + '-' + str(timestamp.day) + '\t' + result['rrtype'] + '\t' + result['rdata'])
            print('')

def infile_and_outfile():
    infile = args.input_file
    outfile = open(args.output_file, 'w')
    with open(infile, 'r') as infile:
        for line in infile:
            domain = str.strip(line)
            print("[*] root domain: " + domain)
            results = query(domain)
            for result in results:
                timestamp = result['time_last']
                outfile.write(str(timestamp.year) + '-' + str(timestamp.month) + '-' + str(timestamp.day) + ',' + result['rrtype'] + ',' + result['rdata'] + '\n')
            print('')

def domain_only():
    domain = args.domain
    print("[*] root domain: " + domain)
    results = query(domain)
    for result in results:
        timestamp = result['time_last']
        print('     ' + str(timestamp.year) + '-' + str(timestamp.month) + '-' + str(timestamp.day) + '\t' + result['rrtype'] + '\t' + result['rdata'])
    print('')

def domain_and_outfile():
    domain = args.domain
    outfile = open(args.output_file, 'w')
    print("[*] root domain: " + domain)
    results = query(domain)
    for result in results:
        timestamp = result['time_last']
        outfile.write(str(timestamp.year) + '-' + str(timestamp.month) + '-' + str(timestamp.day) + ',' + result['rrtype'] + ',' + result['rdata'] + '\n')
    print('')

def intro():
    print('')
    print('+----------------------+')
    print('| subdomain enumerator |')
    print('+----------------------+')
    if not username or not password:
        print('')
        print("you must enter your username and API key/password!")
        print('')
        exit()
    

intro()

if not args.input_file: 
    if not args.domain:
        print("no valid input received!")

print('')

if args.input_file and args.output_file:
    print("input file and output file")
    print('')
    infile_and_outfile()
elif args.input_file:
    print("input file only")
    print('')
    infile_no_outfile()
elif args.domain and args.output_file:
    print("single domain and output file")
    print('')
    domain_and_outfile()
elif args.domain:
    print("single domain only")
    print('')
    domain_only()
else:
    []