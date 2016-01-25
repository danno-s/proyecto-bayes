from src.utils.sqlUtils import sqlWrapper
import yaml

processes = {0:'Filtrar proyectos',
             1:'Otros'}


def getLastDataTime():
    sqlGT = sqlWrapper(db='GT') # Asigna las bases de datos que se accederán
    rows = sqlGT.read("SELECT clickDate FROM pageview ORDER BY id DESC LIMIT 1")
    if len(rows) > 0:
        tdata = rows[0][0]
    else:
        tdata = 0
    return tdata


def getFirstDataTime():
    sqlGT = sqlWrapper(db='GT') # Asigna las bases de datos que se accederán
    rows = sqlGT.read("SELECT clickDate FROM pageview ORDER BY id ASC LIMIT 1")
    if len(rows) > 0:
        tdata = rows[0][0]
    else:
        tdata = 0
    return tdata

def getLastRecID():
    sqlGT = sqlWrapper(db='GT') # Asigna las bases de datos que se accederán
    rows = sqlGT.read("SELECT rec_id FROM pageview ORDER BY id DESC LIMIT 1")
    if len(rows) > 0:
        rec_id = rows[0][0]
    else:
        rec_id = -1
    return rec_id


def labelData(tinit,tend,rec_id,label=''):
    try:
        sqlGT = sqlWrapper(db='GT') # Asigna las bases de datos que se accederán
    except:
        raise
    sqlUpdate = "UPDATE pageview SET process_id=" + str(label) +",rec_id=" + str(rec_id) + " WHERE clickDate BETWEEN "+ str(tinit)+ " and " + str(tend)
    sqlGT.write(sqlUpdate)


def labelGroundTruthProcess():

    tinit = getLastDataTime() +1
    rec_id = getLastRecID() + 1

    pID = eval(input("Ingrese etiqueta (ID) del proceso a realizar:"))

    if pID not in [int(x) for x in processes.keys()]:
        print("Etiqueta no corresponde a un proceso válido...")
        return
    confirmation = input("Está seguro que desea registrar el proceso '"+processes[pID]+"'? (Y/N)")
    if confirmation.upper() != 'Y':
        return

    input("Press ENTER to start recording the process...")

    with open('/home/sebastian/www/guidecapture/config/db.yml','r') as f:
        YML= yaml.safe_load(f)
    dbname = YML['db.options']['dbname']

    with open('/home/sebastian/www/guidecapture/config/db.yml','w') as f:
        YML['db.options']['dbname'] = 'seba_procesos'
        yaml.dump(YML,f,indent=8,default_flow_style=False)

    input("Press ENTER to stop recording when the process is finished...")

    with open('/home/sebastian/www/guidecapture/config/db.yml','w') as f:
        YML['db.options']['dbname'] = dbname
        yaml.dump(YML,f,indent=8,default_flow_style=False)
    if tinit == 1:
        tinit = getFirstDataTime()
    print("Process captured.")
    tend = getLastDataTime()
    print(tend)
    # Label the finished process:
    print("Labeling data from tstamps "+str(tinit)+ " to " + str(tend) +" with process ID ..."+ str(pID))
    labelData(tinit,tend,rec_id,label=pID)
    print("Labeling finished.")

if __name__ == '__main__':
    labelGroundTruthProcess()
