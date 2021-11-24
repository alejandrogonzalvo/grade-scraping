from bs4 import BeautifulSoup
import os, argparse


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", help = "Search for a student by position or name")
args = parser.parse_args()

data = {}
meta = ['PUESTO', 'NOMBRE'] 
for filename in os.listdir("data"):
    meta.append(filename.split('.')[0].upper())
    file = open("data/" + filename, "r", encoding='utf8').read()
    soup = BeautifulSoup(file, 'lxml')
    td = soup.find_all('td')
    i = 0
    ant = ""
    for el in td:
        if i == 0:
            student = el.text
            i = 1
            continue
        if i == 1:
            grade = el.text.replace(",", ".")
            try:
                data[student].append(grade)
            except KeyError:
                grades = [grade]
                data[student] = grades
            i = 0

nota_media = 0
filtered_data = {}
for student, grades in data.items():
    if len(grades) == 4:
        filtered_data[student] = grades
for student in filtered_data.keys():
    total = 0
    for grade in filtered_data[student]:
        total += float(grade)
    aver = total / len(filtered_data[student])
    nota_media += aver
    filtered_data[student].insert(0, aver)
sorted_data = {k: v for k, v in sorted(filtered_data.items(), key=lambda item: item[1])}
nota_media_aver = nota_media / len(filtered_data.keys())

msg = "{0:<5}" + ' ' + "{1:<40}"
for i in range(2, len(meta)):
    msg += " {" + str(i) + ":>5}"
print(msg.format(*meta))

i = len(sorted_data.keys())
if args.search:
    for student, grades in sorted_data.items():
        if args.search in student or args.search == str(i):
            msg = f"{str(i) + ' ' + student : <40}{str(grades) : >20}"
            print(msg)
        i -= 1
else:
    with open('notas.txt', 'w') as f:
        for student, grades in sorted_data.items():
            msg = f"{str(i) + ' ' + student : <40}{str(grades) : >20}"
            print(msg)
            i -= 1 
            f.write(msg)

    print(f"\n{'NOTA MEDIA ETSINF UPV : ' + str(nota_media_aver) : ^72}")
