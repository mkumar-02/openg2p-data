import sys
import random
import csv
import string

def random_token(length):
    return ''.join(random.choice(string.digits) for i in range(length))

csv_content = []
with open(sys.argv[1], 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for i, line in enumerate(csv_reader):
        if i!=0:
            line[-1] = random_token(36)
            line.append(random.choices(["Male", "Female"])[0])
        if i==0:
            line.append("Gender")
        csv_content.append(line)
with open(sys.argv[1], 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    for line in csv_content:
        csv_writer.writerow(line)
