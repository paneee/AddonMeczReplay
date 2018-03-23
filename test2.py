import resources.lib.mr_parser

data = resources.lib.mr_parser.meczreplay()

for i in data.links:
    print(i.name)




