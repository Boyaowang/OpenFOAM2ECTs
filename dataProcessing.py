import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
import os
import re
import csv

def readCpRef(path):
    Ub = 0.2
    CpRef = 0.0;
    root = path + '/postProcessing/singleGraph'
    folderNames = [int(folder) for folder in os.listdir(root)]
    folderName = str(max(folderNames))
    path = os.path.join(root, folderName)
    for filename in os.listdir(path):
        data = pd.read_csv(os.path.join(path, filename),
        header=None, names=['value']).values.tolist()
        data_split = [item[0].split(' ') for item in data]
        data_clean = [list(filter(None, item)) for item in data_split]
        dataYbyH = [float(i[0]) for i in data_clean]
        dataP = [float(i[1]) for i in data_clean]
        avgP = sum(dataP) / len(dataP)
        CpRef = avgP/(0.5*pow(Ub, 2))
    return CpRef

def make2DList(col1,col2):
    list2D = []
    for i in range(0,len(col1)):
        singleElm = [col1[i], col2[i]]
        list2D.append(singleElm)
    return list2D

def sortList(sub_li):

    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    sub_li.sort(key = lambda x: x[0])
    return sub_li

def list2Dplot(list2D):
    x = []
    y = []
    for i in range(len(list2D)):
        x.append(list2D[i][0])
        y.append(list2D[i][1])
    return x,y

def readExpData():
    dict_uu = {}
    dict_uv = {}
    dict_vv = {}
    dict_cp = {}
    dict_cf = {}
    dict_U = {}
    variableName = ['uu', 'uv', 'vv', 'cf', 'cp', 'U']
    path = 'DiffuserExperimentalData'
    for filename in os.listdir(path):
        data = pd.read_csv(os.path.join(path, filename),
        header=None, names=['value']).values.tolist()
        data_split = [item[0].split(' ') for item in data]
        data_clean = [list(filter(None, item)) for item in data_split]
        dataX = [float(i[0]) for i in data_clean]
        dataY = [float(i[1]) for i in data_clean]
        # data.drop(columns = 'to_drop', inplace = True)
        filename_split = re.split('__|_|%.x|%.y',filename)
        if filename == 'separation':
            df_sep = data_clean
        elif filename_split[1] == 'uu':
            dict_uu[filename_split[2]] = [dataX, dataY]
        elif filename_split[1] == 'uv':
            dict_uv[filename_split[2]] = [dataX, dataY]
        elif filename_split[1] == 'vv':
            dict_vv[filename_split[2]] = [dataX, dataY]
        elif filename_split[1] == 'cf':
            dict_cf[filename_split[2]] = [dataX, dataY]
        elif filename_split[1] == 'cp':
            dict_cp[filename_split[2]] = [dataX, dataY]
        elif filename_split[1] == 'U':
            dict_U[filename_split[2]] = [dataX, dataY]
    # print(dict_uu)
    # print('1')
    # print(dict_uv)
    # print('2')
    # print(dict_vv)
    # print('3')
    # print(dict_cf)
    # print('4')
    # print(dict_cp)
    # print('5')
    # print(dict_U)
    # for item in dict_U:
    #     for item2 in dict_U[item]:
    #         print(item2)
    # for toPrint in dict_cp:
    #     print(dict_cp[toPrint])
    return df_sep, dict_uu, dict_uv, dict_vv, dict_cf, dict_cp, dict_U

def readNumData(path):
    dict_UbyUf = {}
    dict_uuByUf2 = {}
    dict_uvByUf2 = {}
    dict_vvByUf2 = {}

    list_cfl = []
    list_cfu = []
    list_cpl = []
    list_cpu = []
    list_cxl = []
    list_cxu = []
    list_cyl = []

    CpRef = readCpRef(path)

    root = path + '/postProcessing/sample'
    folderNames = [int(folder) for folder in os.listdir(root)]
    folderName = str(max(folderNames))
    path = os.path.join(root, folderName)
    print(path)

    for filename in os.listdir(path):
        if filename.startswith("c") or filename.startswith("C"):
            data = pd.read_csv(os.path.join(path, filename),
            header=None, names=['value']).values.tolist()

            dataTrans =  [float(i[0]) for i in data]


            if filename == "Cxl":
                list_cxl = dataTrans
            elif filename == "Cxu":
                list_cxu = dataTrans
            elif filename == "Cyl":
                list_cyl = dataTrans
            elif filename == "cfl":
                list_cfl = dataTrans
            elif filename == "cfu":
                list_cfu = dataTrans
            elif filename == "cpl":
                CpFinal =  [i-CpRef for i in dataTrans]
                list_cpu = CpFinal
            elif filename == "cpu":
                CpFinal =  [i-CpRef for i in dataTrans]
                list_cpl = CpFinal

        if filename.startswith("x"):
            filename_split = re.split('x_by_h_|_|.xy',filename)
            filename_split = [i for i in filename_split if i]
            # print(filename_split)
            data = pd.read_csv(os.path.join(path, filename),
            header=None, names=['value']).values.tolist()
            data_split = [item[0].split(' ') for item in data]
            data_clean = [list(filter(None, item)) for item in data_split]
            dataY = [float(i[0]) for i in data_clean]
            dataUbyUf = [float(i[1]) for i in data_clean]
            datauuByUf2 = [float(i[2]) for i in data_clean]
            datauvByUf2 = [float(i[3]) for i in data_clean]
            datavvByUf2 = [float(i[4]) for i in data_clean]


            dict_UbyUf[filename_split[0]] = [dataY, dataUbyUf]
            dict_uuByUf2[filename_split[0]] = [dataY, datauuByUf2]
            dict_uvByUf2[filename_split[0]] = [dataY, datauvByUf2]
            dict_vvByUf2[filename_split[0]] = [dataY, datavvByUf2]

    cpu2DList = sortList(make2DList(list_cxu, list_cpu))
    cpl2DList = sortList(make2DList(list_cxu, list_cpl))
    cfu2DList = sortList(make2DList(list_cxu, list_cfu))
    cfl2DList = sortList(make2DList(list_cxu, list_cfl))
            # print(dict_UbyUf)
    return dict_UbyUf, dict_uuByUf2, dict_uvByUf2, dict_vvByUf2, cfl2DList, \
    cfu2DList, cpl2DList, cpu2DList, list_cxl, list_cxu, list_cyl

def plotting(dict, title:str, secNo, xbyH, magCoef, marker):
    secNo = [str(item) for item in secNo]
    # xbyH = [str(item) for item in xbyH]
    fig, ax = plt.subplots()
    selected = '-6'
    for key in dict:
        if key in secNo:
            if key == selected:
                myLabel = "Expriment"
            else:
                myLabel = None
            secIndex = secNo.index(key)
            x = [item*magCoef + xbyH[secIndex] for item in dict[key][1]]
            plt.plot(x,dict[key][0], marker, fillstyle = 'none', label = myLabel)
            # plt.legend()
    return plt
    # plt.show()

def plottingNum(dictNum,dicExp,title:str,secNo,xbyH,magCoef,marker,pltInput,label):
    secNo = [str(item) for item in secNo]
    # xbyH = [str(item) for item in xbyH]
    # fig, ax = plt.subplots()
    selected = '-6'
    for key in dictNum:
        if key in dicExp and key in secNo:
            if key == selected:
                myLabel = label
            else:
                myLabel = None
            secIndexNum = secNo.index(key)
            x = [item*magCoef + xbyH[secIndexNum] for item in dictNum[key][1]]
            pltInput.plot(x,dictNum[key][0], marker, fillstyle = 'none', label = myLabel)
            plt.legend()

    # plt.show()
    return pltInput


if __name__ == "__main__":

    readCpRef("kOmegaSST")

    secNo = [-6,3,6,13,14,16,17,19,20,23,24,26,27,29,30,33,34,40,47
    ,53,60,67,74]
    xbyH = [-5.87,2.59,5.98,12.75,13.56,16.14,16.93,19.53,20.32,22.91
    ,23.71,26.3,27.09,29.69,30.48,33.07,33.87,39.85,46.62,53.39,60.17
    ,66.94,73.71]
    # Section for U and uu
    secNoU = [-6, 6, 14, 20, 27, 34, 40, 47]
    xbyHU = [-5.87, 5.98, 13.56, 20.32, 27.09, 33.87, 39.85, 46.62]

    # Section for uv and vv
    secNoV = [-6, 6, 13, 19, 26, 33, 40, 47]
    xbyHV = [-5.87, 5.98, 12.75, 19.53, 26.3, 33.07, 39.85, 46.62]

    df_sep, dict_uu, dict_uv, dict_vv, dict_cf, dict_cp, dict_U = readExpData()
    # Read numerical data from kOmegaSST results

    dict_UbyUfSST, dict_uuByUf2SST, dict_uvByUf2SST, dict_vvByUf2SST, \
    cfl2DListSST, cfu2DListSST,cpl2DListSST, cpu2DListSST,list_cxlSST, \
    list_cxuSST, list_cylSST\
    = readNumData('kOmegaSST')

    dict_UbyUfEps, dict_uuByUf2Eps, dict_uvByUf2Eps, dict_vvByUf2Eps, \
    cfl2DListEps, cfu2DListEps,cpl2DListEps, cpu2DListEps,\
    list_cxlEps, list_cxuEps, list_cylEps\
    = readNumData('kEpsilon')

    dict_UbyUfLSKE, dict_uuByUf2LSKE, dict_uvByUf2LSKE, dict_vvByUf2LSKE, \
    cfl2DListLSKE, cfu2DListLSKE,cpl2DListLSKE, cpu2DListLSKE,\
    list_cxlLSKE, list_cxuLSKE, list_cylLSKE\
    = readNumData('LaunderSharmaKE')

    dict_UbyUfCub, dict_uuByUf2Cub, dict_uvByUf2Cub, dict_vvByUf2Cub, \
    cfl2DListCub, cfu2DListCub,cpl2DListCub, cpu2DListCub,\
    list_cxlCub, list_cxuCub, list_cylCub\
    = readNumData('LienCubicKE')

    dict_UbyUfSA, dict_uuByUf2SA, dict_uvByUf2SA, dict_vvByUf2SA, \
    cfl2DListSA, cfu2DListSA,cpl2DListSA, cpu2DListSA,\
    list_cxlSA, list_cxuSA, list_cylSA\
    = readNumData('SpalartAllmaras')

    dict_UbyUfKEPT, dict_uuByUf2KEPT, dict_uvByUf2KEPT, dict_vvByUf2KEPT, \
    cfl2DListKEPT, cfu2DListKEPT,cpl2DListKEPT, cpu2DListKEPT,\
    list_cxlKEPT, list_cxuKEPT, list_cylKEPT\
    = readNumData('kEpsilonPhitF')

    # # postProcessing lower wall cp
    # cplExp = dict_cp['00']
    # plt.plot(cplExp[0],cplExp[1],"o",fillstyle = 'none')
    # plt.plot(list2Dplot(cpl2DListSST)[0],list2Dplot(cpl2DListSST)[1],label="kOmegaSST")
    # plt.plot(list2Dplot(cpl2DListEps)[0],list2Dplot(cpl2DListEps)[1],label="kEpsilon")
    # plt.plot(list2Dplot(cpl2DListSA)[0],list2Dplot(cpl2DListSA)[1],label="SpalartAllmaras")
    # plt.plot(list2Dplot(cpl2DListKEPT)[0],list2Dplot(cpl2DListKEPT)[1],label="kEpsilonPhitF")
    # plt.plot(list2Dplot(cpl2DListLSKE)[0],list2Dplot(cpl2DListLSKE)[1],label="LaunderSharmaKE")
    # plt.plot(list2Dplot(cpl2DListCub)[0],list2Dplot(cpl2DListCub)[1],label="LienCubicKE")
    # plt.xlim([-20, 70])
    # plt.ylim([-0.2, 1])
    # plt.xlabel("x/H")
    # plt.ylabel("Cp")
    # plt.title("lower wall Cp")
    # plt.legend()
    # plt.show()
    #
    # # postProcessing upper wall cp
    # cpuExp = dict_cp['10']
    # plt.plot(cpuExp[0],cpuExp[1],"o",fillstyle = 'none')
    # plt.plot(list2Dplot(cpu2DListSST)[0],list2Dplot(cpu2DListSST)[1],label="kOmegaSST")
    # plt.plot(list2Dplot(cpu2DListEps)[0],list2Dplot(cpu2DListEps)[1],label="kEpsilon")
    # plt.plot(list2Dplot(cpu2DListSA)[0],list2Dplot(cpu2DListSA)[1],label="SpalartAllmaras")
    # plt.plot(list2Dplot(cpu2DListKEPT)[0],list2Dplot(cpu2DListKEPT)[1],label="kEpsilonPhitF")
    # plt.plot(list2Dplot(cpu2DListLSKE)[0],list2Dplot(cpu2DListLSKE)[1],label="LaunderSharmaKE")
    # plt.plot(list2Dplot(cpu2DListCub)[0],list2Dplot(cpu2DListCub)[1],label="LienCubicKE")
    # plt.xlim([-20, 70])
    # plt.ylim([-0.2, 1])
    # plt.xlabel("x/H")
    # plt.ylabel("Cp")
    # plt.title("upper wall Cp")
    # plt.legend()
    # plt.show()
    #
    # # postProcessing lower wall cf
    # cflExp = dict_cf['00']
    # plt.plot(cflExp[0],cflExp[1],"o",fillstyle = 'none')
    # plt.plot(list2Dplot(cfl2DListSST)[0],list2Dplot(cfl2DListSST)[1],label="kOmegaSST")
    # plt.plot(list2Dplot(cfl2DListEps)[0],list2Dplot(cfl2DListEps)[1],label="kEpsilon")
    # plt.plot(list2Dplot(cfl2DListSA)[0],list2Dplot(cfl2DListSA)[1],label="SpalartAllmaras")
    # plt.plot(list2Dplot(cfl2DListKEPT)[0],list2Dplot(cfl2DListKEPT)[1],label="kEpsilonPhitF")
    # plt.plot(list2Dplot(cfl2DListLSKE)[0],list2Dplot(cfl2DListLSKE)[1],label="LaunderSharmaKE")
    # plt.plot(list2Dplot(cfl2DListCub)[0],list2Dplot(cfl2DListCub)[1],label="LienCubicKE")
    # plt.xlim([-10, 60])
    # plt.ylim([-0.002, 0.02])
    # plt.xlabel("x/H")
    # plt.ylabel("Cf")
    # plt.title("lower wall Cf")
    # plt.legend()
    # plt.show()
    #
    # # postProcessing upper wall cf
    # cfuExp = dict_cf['10']
    # plt.plot(cfuExp[0],cfuExp[1],"o",fillstyle = 'none')
    # plt.plot(list2Dplot(cfu2DListSST)[0],list2Dplot(cfu2DListSST)[1],label="kOmegaSST")
    # plt.plot(list2Dplot(cfu2DListEps)[0],list2Dplot(cfu2DListEps)[1],label="kEpsilon")
    # plt.plot(list2Dplot(cfu2DListSA)[0],list2Dplot(cfu2DListSA)[1],label="SpalartAllmaras")
    # plt.plot(list2Dplot(cfu2DListKEPT)[0],list2Dplot(cfu2DListKEPT)[1],label="kEpsilonPhitF")
    # plt.plot(list2Dplot(cfu2DListLSKE)[0],list2Dplot(cfu2DListLSKE)[1],label="LaunderSharmaKE")
    # plt.plot(list2Dplot(cfu2DListCub)[0],list2Dplot(cfu2DListCub)[1],label="LienCubicKE")
    # plt.xlim([-10, 60])
    # plt.ylim([-0.002, 0.02])
    # plt.xlabel("x/H")
    # plt.ylabel("Cf")
    # plt.title("upper wall Cf")
    # plt.legend()
    # plt.show()


    # postProcessing U/Uf
    pltExp = plotting(dict_U, '1', secNoU, xbyHU, 10, 'bo')
    pltSST = plottingNum(dict_UbyUfSST,dict_uu,'1',secNoU,xbyHU,10,'m--',pltExp,"kOmegaSST")
    pltEps = plottingNum(dict_UbyUfEps,dict_uu,'1',secNoU,xbyHU,10,'c--',pltExp,"kEpsilon")
    pltLSKE = plottingNum(dict_UbyUfLSKE,dict_uu,'1',secNoU,xbyHU,10,'g--',pltExp,"LaunderSharmaKE")
    plt.plot(list_cxlSST,list_cylSST,"k")
    plt.fill_between(list_cxlSST,list_cylSST,alpha=0.30)
    plt.xlim([-10, 50])
    plt.ylim([0, 4.7])
    plt.show()

    # postProcessing uu/Uf^2
    pltExp = plotting(dict_uu, '1', secNoU, xbyHU, 500, 'bo')
    # pltSST = plottingNum(dict_uuByUf2SST,dict_uu,'1',secNoU,xbyHU,500,'b--',pltExp,"kOmegaSST")
    pltEps = plottingNum(dict_uuByUf2Eps,dict_uu,'1',secNoU,xbyHU,500,'c--',pltExp,"kEpsilon")
    pltLSKE = plottingNum(dict_uuByUf2LSKE,dict_uu,'1',secNoU,xbyHU,500,'g--.',pltExp,"LaunderSharmaKE")

    plt.plot(list_cxlSST,list_cylSST,"k")
    plt.fill_between(list_cxlSST,list_cylSST,alpha=0.30)
    plt.xlim([-10, 50])
    plt.ylim([0, 4.7])
    plt.show()

    # postProcessing uv/Uf^2
    pltExp = plotting(dict_uv, '1', secNoV, xbyHV, 500, 'bo')
    pltSST = plottingNum(dict_uvByUf2SST,dict_uv,'1',secNoV,xbyHV,500,'-',pltExp)
    pltEps = plottingNum(dict_uvByUf2Eps,dict_uv,'1',secNoV,xbyHV,500,'--',pltExp)
    pltLSKE = plottingNum(dict_uvByUf2LSKE,dict_uv,'1',secNoV,xbyHV,500,'-.',pltExp)

    plt.plot(list_cxlSST,list_cylSST,"k")
    plt.fill_between(list_cxlSST,list_cylSST,alpha=0.30)
    plt.xlim([-10, 50])
    plt.ylim([0, 4.7])
    plt.show()

    # postProcessing uv/Uf^2
    pltExp = plotting(dict_vv, '1', secNoV, xbyHV, 500, 'bo')
    pltSST = plottingNum(dict_vvByUf2SST,dict_uv,'1',secNoV,xbyHV,500,'-',pltExp)
    pltEps = plottingNum(dict_vvByUf2Eps,dict_uv,'1',secNoV,xbyHV,500,'--',pltExp)
    pltLSKE = plottingNum(dict_vvByUf2LSKE,dict_uv,'1',secNoV,xbyHV,500,'-.',pltExp)

    plt.plot(list_cxlSST,list_cylSST,"k")
    plt.fill_between(list_cxlSST,list_cylSST,alpha=0.30)
    plt.xlim([-10, 50])
    plt.ylim([0, 4.7])
    plt.show()
