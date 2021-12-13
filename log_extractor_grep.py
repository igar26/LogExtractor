#!/usr/bin/python3

# Not interested to use print statement for printing info so trying to use python's logging feature
import logging
import os
import argparse
import json
import subprocess
# This file is written to take a input file where syslogs are present form the user as first argument, 
# the second argument passed by the user will be a JSON file containg information about information  
# of messages we are filtering from the log file and the number of lines before 
# and after each log level we are searching

# construct the argument parse and parse the arguments - using python utilities 
ap = argparse.ArgumentParser()
ap.add_argument("input_file", help="name of the input file", type=argparse.FileType('r'))
ap.add_argument("JSON_file", help="name of the JSON file for processing logs", type=argparse.FileType('r'))
# NOTE: We dont need the users input for filtering the logs, we can create a 
# file if the user has not given - this can be optional, as its mentioned in the assement forcing it to be a input from user
ap.add_argument("output_file", help="name of the output to add logs after processing", type=argparse.FileType('w'))
args = ap.parse_args()
logging.info("Check file is present in the given path.")
if not os.path.exists(args.input_file.name):
    logging.fatal("Input log processing file is not present in the user specified location")
    raise FileNotFoundError("Need input log file to further process the logs")

logging.info("Check JSON file is present in the given path.")
if not os.path.exists(args.JSON_file.name):
    logging.fatal("JSON file is not present in the user specified location")
    raise FileNotFoundError("Need JSON file to process the logs")

logging.info("Ouput file need not to be present as we have to create one")
if os.path.exists(args.output_file.name):
    logging.warning("Output file already present will over-write")

# Processing the json file in python
message = open(args.JSON_file.name)
data = json.load(message)
message_type = [x for x in data]

# NOTE: Using grep utility

logging.info("Open output file in write mode before processing the input file")
output_file = open(args.output_file.name, 'w+')

def process_log_file(message_type):
    command = "grep {} -B {} -A {} {}".format(message_type, data[message_type]["before"], data[message_type]["after"], args.input_file.name)
    out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_bytes, stderr_bytes = out.communicate()
    stdout_str = stdout_bytes.decode()
    if stderr_bytes.decode():
        logging.fatal(stderr_bytes.decode())
        raise RuntimeError
    print("out", stdout_str)
            
logging.info("For every message in JSON file we are going to process the file twice")
for message in message_type:
    process_log_file(message_type=message)

output_file.close()