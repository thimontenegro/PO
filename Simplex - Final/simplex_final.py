from statistics import variance
import pandas as pd 
import numpy as np
from prettytable import PrettyTable
from dual_simplex import DualSimplex 

class Simplex():
    def __init__(self, objetivo, funcao_objetivo,restricoes,is_big_m):
        self.objetivo = objetivo 
        self.funcao_objetivo = funcao_objetivo
        self.restricoes = restricoes
        self.variaveis = []
        self.matrix = []
        self.base ={}
        self.base = {}
        self.big_m = is_big_m
        fo = self.gera_funcao_objetivo()
        self.gera_tabela(fo)
       
    
    def gera_tabela(self,fo):
        restriscoes = []
        tabela = []
        b_valores = []
        variaveis = []
        b_valores.append(0)
        for val in fo:
            tabela.append(val)
        for con in self.restricoes:
            if con.find('<=') != -1:
                inequacao = '<='
            elif con.find(">=") != -1:
                inequacao = '>='
            elif con.find("=") != -1:
                inequacao = '='
            restriscoes.append(inequacao)
            coeficientes = con.split(inequacao)[0].split("+")
            b = con.split(inequacao)[1]
            b_valores.append(float(b))
            for coeficiente in coeficientes:
                variaveis.append(coeficiente.split('*')[1])
                tabela.append(float(coeficiente.split('*')[0]))
        
        variaveis_list = list(set(variaveis))
        variaveis_list.append('b')
        colunas = int(len(tabela) / len(b_valores))
        linhas = len(b_valores)
        tabela = np.array(tabela).reshape(linhas,colunas)
        b_valores = np.array(b_valores).reshape(-1,1)
        matrix = np.concatenate((tabela, b_valores),axis=1)
        self.matrix = np.array(matrix)
        self.restricoes = np.array(restriscoes)
        self.variaveis = np.array(variaveis_list)
        self.v = self.variaveis
        
    def gera_funcao_objetivo(self):
        funcao_objetivo = self.funcao_objetivo
        
        funcao_objetivo = funcao_objetivo.split("+")
        fo = []
        for val in funcao_objetivo:
            fo.append(int(val.split('*')[0]))
        return fo 
    """
    def __init__(self,restricoes, variaveis,objetivo,matrix,is_big_m):
        self.restricoes = restricoes
        self.variaveis = variaveis
        self.objetivo = objetivo
        self.matrix = matrix
        self.big_m = is_big_m
        self.base = {}
        self.tabela = []
        self.v = variaveis
    """
    def desenha_tabela(self,tabela):
        _tabela = tabela.tolist()
        for linha in range(len(_tabela)):
          for coluna in range(len(_tabela[linha])):
            _tabela[linha][coluna] = "{:.1f}".format(_tabela[linha][coluna])
        
        _tabela.insert(0,self.variaveis)
        x = PrettyTable()
        x.field_names = self.variaveis
        _tabela = tabela.tolist()
        for linha in range(len(_tabela)):
            x.add_row(_tabela[linha])
        print(x)
    
    def add_dummy_variables(self,tabela):
       
        coluna = self.variaveis.index('s')
        linhas = []
        for idx, restricao in enumerate(self.restricoes):
            if restricao == '>=':
                linhas.append(idx+1)

        for i in range(len(linhas)):
            tabela[linhas[i]][coluna] = -1

        for z in range(len(tabela[0])):
            if self.variaveis[z][0] == 'a':
                tabela[0][z] = 50
        return tabela
    def _big_m_solver(self, tabela):
        tabela_copy = tabela[1:,:]
     
        aux_dummy = []
        for i in tabela_copy[0]:
            aux_dummy.append(0)

        for i in range(len(tabela_copy)):
            for j in range(len(tabela_copy[i])):
                if self.restricoes[i] != '<=':
                  aux_dummy[j] = aux_dummy[j] + tabela_copy[i][j]
               
                

        for i in range(len(aux_dummy)):
            aux_dummy[i] *= -50
        
        for i in range(len(tabela[0])):
            tabela[0][i] +=  aux_dummy[i]
  
        return tabela  

    def _resolvida(self,tabela) -> bool:
        fo = tabela[0,:-1]
        resultado =  True if min(fo) >= 0 else False 
        return resultado
        
    def _monta_tabela(self):
        
        variaveis = self.variaveis.tolist()
        
        for idx, restricao in enumerate(self.restricoes):
            if restricao == '<=':
                variaveis.insert(len(variaveis)-1,'xf'+str(idx+1))
            elif restricao == '>=':
                variaveis.insert(len(variaveis) -1, 'a'+str(idx+1))
            else:
                variaveis.insert(len(variaveis)-1,"a"+str(idx+1))
        for restricao in self.restricoes:
            if restricao == '>=':
               variaveis.insert(len(variaveis)-1,'s')
        
        self.variaveis = variaveis 
        tabela = np.zeros((len(self.matrix),len(self.variaveis)))
        
        #preenchendo os valores na tabela 
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i]) - 1):
                tabela[i][j] = self.matrix[i][j]
            tabela[i][-1] = self.matrix[i][-1]
       
        identidade = np.identity(len(self.variaveis))
        tamanho = len(self.matrix[0]) - 1
        for i in range(len(tabela)):
            for j in range(len(tabela[i]) - 1):
                if j >= tamanho:
                    tabela[i][j] = identidade[i-1][j-tamanho]
        return tabela

    def _coluna_pivot(self, tabela):
        funcao_objetivo = tabela[0,:-1]
        coluna_valor_inicial = funcao_objetivo[0]
        indice_coluna_pivot = 0
        for i in range(1,len(funcao_objetivo)):
            valor_coluna_atual = funcao_objetivo[i]
            if valor_coluna_atual < coluna_valor_inicial:
                coluna_valor_inicial = valor_coluna_atual
                indice_coluna_pivot = i 
        return indice_coluna_pivot, coluna_valor_inicial
    
    def _linha_pivot(self, tabela, indice_coluna_pivot):
        valor_razao = 10
        indice_linha_pivot = 0 
        for i in range(1,len(tabela)):
            valor_linha_coluna = tabela[i][indice_coluna_pivot]
            if valor_linha_coluna > 0:
                valor_b = tabela[i][-1]
                teste_razao = valor_b / valor_linha_coluna
                
                if teste_razao < valor_razao:
                    valor_razao = teste_razao
                    indice_linha_pivot = i 
        
        print(f"Teste da Razao é {valor_razao}, e seu índice é {indice_linha_pivot}, logo  {self.variaveis[indice_linha_pivot]} sai da base.")
        
        nova_linha = []
        pivot = tabela[indice_linha_pivot][indice_coluna_pivot]
     
        for i in tabela[indice_linha_pivot]:
            resultado = i/pivot
            nova_linha.append(resultado)
        tabela[indice_linha_pivot] = nova_linha
        return tabela, indice_linha_pivot, nova_linha

    def _escalona_matrix(self, linha_tabela, nova_linha, indice_linha_pivot) -> list:
        linha_escalonada = []
       
        pivot = linha_tabela[indice_linha_pivot] * (-1)
        
        for i in range(len(linha_tabela)):
            calculo = nova_linha[i] * pivot 
            calculo += linha_tabela[i] 
            linha_escalonada.append(calculo)
        return linha_escalonada

    def _resolve_dual(self):
        print('-------------------')
        print("DUAL")
        w = self.matrix[1:, -1]
        nova_tabela = self.matrix[1:]
        if self.objetivo == 'max':
            tabela_transposta = nova_tabela[:,:-1].T
        else: 
            tabela_transposta = nova_tabela[:,:-1].T
            
        nova_tabela = np.insert(tabela_transposta,len(nova_tabela), values= (self.matrix[0,:-1]),axis = 1)
        variaveis_w = []
      
        restricoes = ['<=' if restricao == '>=' else '>=' for restricao in self.restricoes]
        
        for i in range(len(restricoes)):
            nova_var = f"y_{i}"
            variaveis_w.append(nova_var)

    
        variaveis_w.append('b')
        
        self.variaveis = variaveis_w
      
        
        dual = DualSimplex(w=w, objetivo=self.objetivo, restricoes=self.restricoes, tabela=nova_tabela,variaveis=self.variaveis)
        dual.resolve_dual()
        
    def run(self):
        print("PRIMAL")
        print("----")
        tabela = self._monta_tabela()
        
        if self.big_m == True:
          
           tabela = self.add_dummy_variables(tabela)
           
           tabela = self._big_m_solver(tabela)
       
        if self.objetivo == 'max':
            tabela[0] = tabela[0] * (-1)
        is_solved = False 
        iter = 1
        
        print(f"Iteração - {iter}")
        print("------------------")
        self.desenha_tabela(tabela)
        print()

        while is_solved != True:
            indice_pivot_coluna, valor_pivot_coluna = self._coluna_pivot(tabela)
            print(f"O menor valor da coluna é {valor_pivot_coluna} e seu índice {indice_pivot_coluna}, logo {self.variaveis[indice_pivot_coluna]} entra na base.")
            self.base[self.variaveis[indice_pivot_coluna]] = valor_pivot_coluna
            tabela, indice_linha_pivot, nova_linha = self._linha_pivot(tabela, indice_pivot_coluna)
            print(f"O indice da linha pivot é de {indice_linha_pivot}")
            for i in range(len(tabela)) :
    
                if i != indice_linha_pivot:
                    tabela[i] = self._escalona_matrix(tabela[i], nova_linha, indice_pivot_coluna)
            is_solved = self._resolvida(tabela)
            iter += 1 
            print(f"Iteração - {iter}")
            print("------------------")
            self.desenha_tabela(tabela)
            print()
        z = tabela[0][-1]
        if self.objetivo == 'min':
            print('Z = ', z * (-1))
        else:
            print('Z = ', z)
        
        indice = {} 
        count = 0
        df = pd.DataFrame(tabela,columns = self.variaveis)
        for variaveis in range(len(self.v) -1):
          count = 0
          for idx, row in df.iterrows():
          
            if row[self.v[variaveis]] != 0:
                indice[self.v[variaveis]] = (idx,count)
                count += 1

        for variaveis in range(len(self.v) - 1):
          for key, value in indice.items():
            index = value[0]
            count = value[1]
            if count == 0:
              if self.v[variaveis] == key:
                  print(f"{self.v[variaveis]} -> {df['b'].iloc[index]}")
            else:
              if self.v[variaveis] == key:
                  print(f"{self.v[variaveis]} -> {0}")
        self.tabela = tabela
        self._resolve_dual()