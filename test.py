from docx import Document
from os.path import basename
import re
file_name = "D:\\work\\project\\ResumeClassification\\rc\\resume\\neha.docx"
doc = Document(file_name)
a = list()
pattern = re.compile('rId\d+')
for graph in doc.paragraphs:
    b = list()
    for run in graph.runs:
        if run.text != '':
            print(run.text.encode("utf-8"))
            b.append(run.text)
        else:
            # b.append(pattern.search(run.element.xml))
            #print(run.element.xml)
            fmtre=pattern.search(run.element.xml)
            if fmtre is None:
                continue
            contentID = fmtre.group(0)
            try:
                contentType = doc.part.related_parts[contentID].content_type
            except KeyError as e:
                print(e)
                continue
            if not contentType.startswith('image'):
                continue
            imgName = basename(doc.part.related_parts[contentID].partname)
            imgData = doc.part.related_parts[contentID].blob
            b.append(imgData.encode("utf-8"))
    a.append(b)

