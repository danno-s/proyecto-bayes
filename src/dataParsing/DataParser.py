# -*- coding: utf-8 -*-

from src.dataParsing.macroStateModel.MacroStateMap import MacroStateMap
from src.nodeClass.MicroNode import MicroNode

from src.utils.sqlUtils import sqlWrapper

import json


class DataParser:
    __instance = None

    def __new__(cls):
        if DataParser.__instance is None:
            DataParser.__instance = object.__new__(cls)
            DataParser.__instance.userD = DataParser.__instance.__loadUsers()
            DataParser.__instance.macroStatesD= DataParser.__instance.__loadMacroStates()
            DataParser.__instance.microStatesD, DataParser.__instance.contentElementsD = DataParser.__instance.__loadContentElements()
            DataParser.__instance.macroStateMapper = DataParser.__instance.getMacroMapper()
        return DataParser.__instance

    def __loadUsers(self):
        try:
            sqlPD = sqlWrapper(db='PD')
        except:
            raise
        sqlRead = "select id,user_id,profile from users"
        rows = sqlPD.read(sqlRead)
        userD = dict()
        for row in rows:
            userD[row[0]] = (row[1],row[2])
        return userD

    def __loadMacroStates(self):
        """Carga Macro estados predefinidos a la tabla macrostates.

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
            microStatesD[mn.micro_id]=mn
            rawD[mn.micro_id]=row[7]
        return microStatesD, rawD

    def getMacroMapper(self):
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

    def getUserID(self,variables):
        """
        Obtiene el id entero de un usuario en la base de datos

        Parameters
        ----------
        variables : str
            El json de variables que incluye la id de usuario como str a buscar.
        Returns
        -------
        int
            El id entero del usuario.
        """
        varD = json.loads(variables)
        if not varD or 'id_usuario' not in varD.keys():
            return False
        user_id_str = json.loads(variables)['id_usuario']
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
        return self.macroStatesD[macrostatemap_id]

    def getMicroID(self, contentElements):
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
        if contentElements in self.contentElementsD.values():
            return list(self.contentElementsD.keys())[list(self.contentElementsD.values()).index(contentElements)]
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
        sqlPD = sqlWrapper(db='PD')
        if user_id in self.userD.keys():
            return self.userD[user_id]
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

        return "SELECT id, url, urls, variables, clickDate, contentElements FROM " + capture_table + " WHERE variables NOT LIKE 'null'" + " LIMIT " + str(
            n) + ", "+ str(bufferSize)

    def parseData(self):
        """Extrae datos desde capture_table y los guarda en nodes en un formato adecuado
        Returns
        -------

        """
        sqlGC = sqlWrapper(db='GC')
        sqlCD = sqlWrapper(db='CD')

        sqlCD.truncate("nodes")
        sqlWrite = "INSERT INTO nodes (user_id, clickDate, macro_id, profile, micro_id) VALUES (%s,%s,%s,%s,%s)"
        i = 0
        Nnodes = 0
        bufferSize = 500
        while True:
            info = sqlGC.read(self.__parseQuery(i,bufferSize))
            writeL = list()
            if not info:
                break
            for row in info:
                urlstr = row[1]
                macro = self.getMacroID((urlstr, row[2], row[3]))
                micro = self.getMicroID(row[5])
                if not macro:
                    continue
                if not micro:
                    micro = -1
                usr = self.getUserID(row[3])
                if not usr:
                    continue
                profile = json.loads(row[3])['profile']
                if not profile:
                    profile = None
                click = row[4]
                writeL.append((usr, click, macro, profile, micro))
                Nnodes += 1
            sqlCD.writeMany(sqlWrite,writeL)

            i += bufferSize

        print("Total nodes: " + str(Nnodes))
