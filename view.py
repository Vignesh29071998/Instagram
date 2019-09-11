from xml.dom import minidom
files = minidom.parse("input.xml")
name = files.getElementsByTagName('name')
print(name)
