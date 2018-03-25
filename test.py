import resources.lib.meczreplay


parser = resources.lib.meczreplay.webParser()
data = parser.getData()

for i in data: 
    print(i.name)