# Log Extractor
- This utility takes 3 files 
1) Input file where logs are present
2) JSON file where the information about what fields to be extracted.
3) Output file name


Example:
i/p is:
	•	/var/log/syslog
	•	Json file is as follows
	•	filtered_op.log

Jason file:
{ “Error” : {“before”: 5, “after”: 10}, “Warning”: {“before”: 1, “after” : 1}}

Output file:
The o/p filtered_op.log  should look like below

Before Line1
Before Line2
…
Before Line5
Error : Somethinge something
After Line1
After Line2
…
After Line10


To run this utility:
python3 log_extractor_grep.py inputFile.txt extract_log.json output.txt
