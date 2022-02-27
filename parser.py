import  scotiaParser 
import americianExpressParser

def loadList():
    parsers =[]
    parsers.append(scotiaParser)
    parsers.append(americianExpressParser)
    return parsers


def parse(full_path):
    parsers= loadList()
    for  parse  in parsers:
        if(parse.canParse(full_path)):
            parse.main(full_path)

if __name__ == "__main__":
    parse("/Users/davepierre/Documents/Projects/budgetParser/DjangoRestApisPostgreSQL/media/pcbanking_FDOHvPc.csv")