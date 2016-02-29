from src.userempathetic.metrics.Metric import NodeMetric


class MicroDistance(NodeMetric):
    def __init__(self):
        NodeMetric.__init__(self)

    def distance(self, n1, n2):
        iT_d= self.__inputTextDistance(n1.inputText,n2.inputText)
        sel_d = self.__selectsDistance(n1.selects,n2.selects)
        #ch_d = self.__checkboxDistance(n1.checkbox,n2.checkbox)
        tA_d = self.__textAreaDistance(n1.textArea,n2.textArea)
        rB_d = self.__radioButtonDistance(n1.radioButton, n2.radioButton)
        print("INPUTTEXT DISTANCE="+str(iT_d))
        print("SELECTS DISTANCE="+str(sel_d))
        print("TEXTAREAS DISTANCE="+str(tA_d))
        print("RADIOBUTTONS DISTANCE="+str(tA_d))
        #print("CHECKBOXS DISTANCE="+str(ch_d))
        return sel_d+iT_d+tA_d+rB_d

    def __inputTextDistance(self,t1,t2):
        print("inputTexts:" +"\t"+str(t1)+"\t"+str(t2))
        return sum([abs(x - y) for x, y in zip(t1, t2)])

    def __selectsDistance(self,sel1,sel2):
        print("selects:" +"\t"+str(sel1)+"\t"+str(sel2))
        res = 0
        if any(isinstance(i, list) for i in sel1) and any(isinstance(i, list) for i in sel2):
            for selGroup1,selGroup2 in zip(sel1,sel2):
                res += sum([int(x != y) for x, y in zip(selGroup1, selGroup2)])
        else:
            res= sum([int(x != y) for x, y in zip(sel1, sel2)])
        return res

    #TODO: MODIFICAR CAPTURA DE CHECKBOXES PARA NORMALIZAR VECTORES... ACTUALMENTE LOS
    def __checkboxDistance(self,ch1,ch2):
        print("checkboxs:" +"\t"+str(ch1)+"\t"+str(ch2))
        res = 0
        for chGroup1,chGroup2 in zip(ch1,ch2):
            res += sum([int(x != y) for x, y in zip(chGroup1, chGroup2)])
        return res

    def __textAreaDistance(self,t1,t2):
        print("textAreas:" +"\t"+str(t1)+"\t"+str(t2))
        return sum([abs(x - y) for x, y in zip(t1, t2)])

    def __radioButtonDistance(self,r1,r2):
        print("radioButtons:" +"\t"+str(r1)+"\t"+str(r2))
        return sum([abs(x - y) for x, y in zip(r1, r2)])