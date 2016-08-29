# -*- coding: utf-8 -*-

from src.dataParsing.macroStateModel.MacroStateMap import MacroStateMap
from src.nodeClass.MicroNode import MicroNode

from src.utils.sqlUtils import sqlWrapper

import json


class DataParser:
    """
    Clase encargada de extraer los datos necesarios para definir nodos, almacenarlos en diccionarios y posteriormente
    generar nodos a partir de cada captura.
    """
    __instance = None

    def __new__(cls):
        """
        Constructor segun patron Singleton para que se carguen los datos una sola vez sobre una unica instancia.
        Returns
        -------

        """
        if DataParser.__instance is None:
            DataParser.__instance = object.__new__(cls)
            DataParser.__instance.userD = DataParser.__instance.__loadUsers()
            DataParser.__instance.macroStatesD = DataParser.__instance.__loadMacroStates()
            DataParser.__instance.macroStateMapper = DataParser.__instance.getMacroMapper()
        return DataParser.__instance

    def __loadUsers(self):
        """
        Carga usuarios de base de datos "parseddata"
        Returns
        -------

        """
        try:
            sqlPD = sqlWrapper(db='PD')
        except:
            raise
        sqlRead = "select id,capture_userid,profile from users"
        rows = sqlPD.read(sqlRead)
        userD = dict()
        for row in rows:
            userD[row[0]] = (row[1],row[2])
        return userD

    def __loadMacroStates(self):
        """
        Carga Macro estados predefinidos a la tabla macrostatemap.
        Returns
        -------
        """
        try:
            # Asigna las bases de datos que se accederan
            sqlPD = sqlWrapper(db='PD')
        except:
            raise
        sqlRead = "SELECT id,name from macrostatemap"
        rows = sqlPD.read(sqlRead)
        assert len(rows) > 0
        macroStatesD = dict()
        for row in rows:
            msMap = MacroStateMap(row[0], row[1])
            macroStatesD[row[0]] = msMap
        return macroStatesD

    def __loadContentElements(self):
        """
        Carga contentElements que definen los distintos microestados.
        Returns
        -------

        """

        try:
            # Asigna las bases de datos que se accederan
            sqlPD = sqlWrapper(db='PD')
        except:
            raise
        sqlRead = "SELECT id,macro_id,TextAreas,InputText,RadioButton,Selects,Checkbox,raw FROM contentElements"
        rows = sqlPD.read(sqlRead)
        microStatesD = dict()
        rawD = dict()
        for row in rows:
            mn = MicroNode(micro_id = row[0],
                             macro_id = row[1],
                             TextAreas = row[2],
                             InputText= row[3],
                             RadioButton = row[4],
                             Selects = row[5],
                             Checkbox = row[6],
                             key="")
            if mn.macro_id not in microStatesD.keys():
                microStatesD[mn.macro_id] = list()
            microStatesD[mn.macro_id].append(mn)
            if row[7] not in rawD.keys():
                rawD[row[7]] = list()
            rawD[row[7]].append(mn.micro_id)
        return microStatesD, rawD

    def getMacroMapper(self):
        """
        Permite obtener el mapeador de macroestados que utiliza las reglas definidas en tabla "macrostaterule"
        Returns
        -------
        MacroStateMapper

        """
        try:
            return self.macroStateMapper
        except AttributeError:

            from src.utils.loadConfig import Config
            from src.dataParsing.macroStateExtractors.URLsMacroStateExtractor import URLsMacroStateExtractor
            from src.dataParsing.macroStateExtractors.CustomMacroStateExtractor import CustomMacroStateExtractor

            macroStateExtractorsD = {"URLs": URLsMacroStateExtractor,
                                     "Custom": CustomMacroStateExtractor}
            mse = Config.getValue("macrostate_extractor")
            macrostateE = macroStateExtractorsD[mse]()
            return macrostateE.getMacroMapper()

    def getUserID(self,variables, captured_ip):
        """
        Obtiene el id entero de un usuario en la base de datos

        Parameters
        ----------
        variables : str
            El json de variables que incluye la id de usuario como str a buscar.
        captured_ip : str
            La ip capturada.
        Returns
        -------
        int
            El id entero del usuario.
        """
        varD = json.loads(variables)
        if not varD or 'id_usuario' not in varD.keys():
            return False
        user_id_str = json.loads(variables)['id_usuario']
        if user_id_str == 'b6589fc6ab0dc82cf12099d1c2d40ab994e8410c':
            user_id_str = captured_ip
        return self.__findUserID(user_id_str)

    def __findUserID(self,user_id_str):
        """
        Permite encontrar id del usuario en el diccionario interno de la clase.
        Parameters
        ----------
        user_id_str

        Returns
        -------
        False si no encuentra el id del usuario.
        int correspondiente al id numerico del usuario.
        """
        for k,v in self.userD.items():
            if v[0] == user_id_str:
                return k
        return False
    def getMacroID(self,data):
        """
        Obtiene el id en la base de datos del macro estado

        Parameters
        ----------
        data: (url,urls,variables)
            La url principal a buscar, el arbol de urls a buscar y las variables de la captura.
        Returns
        -------
        int
            La id del macro estado.
        """
        urlstr = data[0]
        if urlstr.endswith(' undefined'):
            urlstr = urlstr[:-10]
        res = self.macroStateMapper.map((urlstr, data[1], data[2]))
        if res is not False and not isinstance(res, str):
            return res.getId()
        return False

    def getMacroStateMap(self,macrostatemap_id):
        """
        Retorna un MacroStateMap que define un macro estado con sus reglas de mapeo.
        Parameters
        ----------
        macrostatemap_id: int
            el ID del macro estado.

        Returns
        -------
    MacroStateMap
        """
        return self.macroStatesD[macrostatemap_id]

    def getMicroID(self, contentElements, macro_id):
        """
        Obtiene el id en la base de datos de un micro estado

        Parameters
        ----------
        contentElements : str
            El microestado a buscar
        Returns
        -------
        int
            El id del microestado
        """
        try:
            a = len(self.contentElementsD)
        except AttributeError:
            DataParser.__instance.microStatesD, DataParser.__instance.contentElementsD = DataParser.__instance.__loadContentElements()
        microNodesL = self.microStatesD[macro_id] # Encontrar lista de micro nodos para el macro estado indicado.
        if contentElements in self.contentElementsD.keys():
            ids = self.contentElementsD[contentElements]
            for mn in microNodesL:
                if mn.micro_id in ids:
                    return mn.micro_id
        return False

    def getProfileOf(self,user_id):
        """
        Obtiene el perfil del usuario con ID user_id

        Parameters
        ----------
        user_id : int
            El ID del usuario.
        Returns
        -------
        str
            el perfil del usuario.
        """
        if user_id in self.userD.keys():
            return self.userD[user_id][1]
        return False

    def getAllUserIDs(self):
        """
        Obtiene una lista con las id de los usuarios desde la base de datos

        Parameters
        ----------
        Returns
        -------
        list
            list de IDs de usuarios en forma de int
        """
        return list(self.userD.keys())

    def getAllMacroStateIDs(self):
        """
        Obtiene una lista con las id de las urls desde la base de datos

        Parameters
        ----------
        Returns
        -------
        list
            list de IDs de urls en forma de int
        """
        return list(self.macroStatesD.keys())

    def __parseQuery(self,n,bufferSize):
        from src.utils.loadConfig import Config
        capture_table = Config.getValue("capture_table")

        return "SELECT id, url, urls, variables, clickDate, contentElements, IP FROM " + capture_table + " WHERE variables NOT LIKE 'null'" + " LIMIT " + str(
            n) + ", "+ str(bufferSize)

    def parseData(self):
        """Extrae datos desde capture_table y los guarda en nodes en un formato adecuado
        Returns
        -------

        """
        sqlGC = sqlWrapper(db='GC')
        sqlCD = sqlWrapper(db='CD')

        sqlCD.truncateRestricted("nodes")
        sqlWrite = "INSERT INTO nodes (user_id, clickDate, macro_id, profile, micro_id, pageview_id) " \
                   "VALUES (%s,%s,%s,%s,%s,%s)"
        i = 0
        Nnodes = 0
        skipped = {'MacroID not mapped':[],'User data not found':[]}
        bufferSize = 500
        while True:
            info = sqlGC.read(self.__parseQuery(i,bufferSize))
            writeL = list()
            if not info:
                break
            for row in info:
                pageview_id = row[0]
                urlstr = row[1]
                macro = self.getMacroID((urlstr, row[2], row[3]))
                micro = self.getMicroID(row[5], macro)
                captured_ip = row[6]
                if not macro:
                    skipped['MacroID not mapped'].append(pageview_id)
                    continue
                if not micro:
                    micro = None
                usr = self.getUserID(row[3],captured_ip)
                if not usr:
                    skipped['User data not found'].append(pageview_id)
                    continue
                profile = json.loads(row[3])['profile']
                if not profile:
                    profile = None
                click = row[4]
                writeL.append((usr, click, macro, profile, micro,pageview_id))
                Nnodes += 1
            sqlCD.writeMany(sqlWrite,writeL)

            i += bufferSize

        print("Total nodes: " + str(Nnodes))
        print("Skipped nodes:")
        for k,v in skipped.items():
            if len(v) > 0:
                print("\t"+ str(k) + "("+str(len(v))+"): "+str(v))
