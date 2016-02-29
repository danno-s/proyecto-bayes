from src.userempathetic.utils.sqlUtils import sqlWrapper
from src.userempathetic.utils.loadConfig import Config
from src.userempathetic.dataParsing.MicroStateVectorExtractor import MicroStateVectorExtractor
from src.userempathetic.nodeClass.MicroNode import MicroNode

sessionFeaturesL = Config().getArray("session_features")
elementTypes = MicroStateVectorExtractor().getElementTypes()


def getFeatureOfSession(session_id, feature):
    assert feature in sessionFeaturesL
    sqlFT = sqlWrapper('FT')
    sqlRead = "SELECT vector FROM " + feature.lower() + "features WHERE session_id =" + str(session_id)
    row = sqlFT.read(sqlRead)
    return [int(x) for x in row[0][0].split(' ')]


def getMSS(s1,s2):
    a = s1.sequence
    b = s2.sequence
    if len(s1.sequence) >= len(s2.sequence):
        minor = s2.sequence
        mayor = s1.sequence
    else:
        minor = s1.sequence
        mayor = s2.sequence

    v1 = list()
    v2 = list()
    c = list() # Cuenta los nodos saltados para identificar una equivalencia de macroestado.

    ind1 = 0
    ind2 = 0
    count = 0
    for i in minor:
        for j in mayor[ind2:]:
            #print(str(i)+"|"+str(j))
            if i[0] == j[0]:
                v1.append(i)
                v2.append(j)
                c.append(count)
                ind2 += 1
                count = 0
                break
            else:
                count +=1
            ind2 += 1
        if len(v1) == 0:
            ind1 += 1
            ind2 = 0
            count = ind1

    return v1,v2, c

def getMicroNode(micro_id):
    sqlPD = sqlWrapper('PD')
    sqlRead = "SELECT * FROM contentElements WHERE id = "+str(micro_id)
   # print(sqlRead)
    row = sqlPD.read(sqlRead)
    return MicroNode(row,key="") #TODO: FIND OUT WTF IS key...

if __name__ == '__main__':

    print(getMicroNode(12).toDict())