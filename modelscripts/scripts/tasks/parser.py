# coding=utf-8
import xml.etree.ElementTree as ET
tree=ET.parse('tm1.kxml')
root=tree.getroot()
for child in root.iter('task'):
    print child.tag, child.find('task-name').text
