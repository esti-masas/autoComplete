import os

sentences={}
for i in range(1,7):
    sentences[i]=[]
def initialize(path):
    #path=r"C:\Users\הודיה\PycharmProjects\GoogleProject\2021-archive\2021-archive\python-3.8.4-docs-text\c-api\abstract.txt"
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            initialize(os.path.join(path, item))
        else:
            f=open(os.path.join(path, item),encoding="utf8")
            file=f.readlines()
            for line in file:
                words1=line.split()
                sentences[1].append({(os.path.join(path, item), file.index(line)+1): words1})
                words2=[]
                for i in range(len(words1)-1):
                    words2.append(words1[i]+" "+words1[i+1])
                sentences[2].append({(os.path.join(path, item), file.index(line)+1): words2})
                words3=[]
                for i in range(len(words1)-2):
                    words3.append(words1[i]+" "+words1[i+1]+" "+words1[i+2])
                sentences[3].append({(os.path.join(path, item), file.index(line)+1): words3})
                words4=[]
                for i in range(len(words1)-3):
                    words4.append(words1[i] + " " + words1[i + 1] + " " + words1[i + 2]+" "+words1[i+3])
                sentences[4].append({(os.path.join(path, item), file.index(line)+1): words4})
                words5 = []
                for i in range(len(words1)-4):
                    words5.append(words1[i] + " " + words1[i + 1] + " " + words1[i + 2] + " " + words1[i + 3]+" " + words1[i +4])
                sentences[5].append({(os.path.join(path, item), file.index(line)+1): words5})
                words6=[]
                for i in range(len(words1)-5):
                    words6.append(words1[i] + " " + words1[i + 1] + " " + words1[i + 2] + " " + words1[i + 3]+" " + words1[i +4]+" " + words1[i +5])
                sentences[6].append({(os.path.join(path, item), file.index(line)+1): words6})

    return sentences












