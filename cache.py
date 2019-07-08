import csv
def write(row):
	with open('cache.csv', 'a', newline='') as csvfile:
	    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
	    print(row)
	    writer.writerow(row)

def read(check):
	with open('cache.csv', newline='') as csvfile:
	     reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	     for row in reader:
	     	if check in row:
	     		return True
	     return False