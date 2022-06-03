import pandas as pd
import numpy as np
from prettytable import PrettyTable
class DualSimplex():
    def __init__(self,restricoes,w,tabela,objetivo,variaveis):
        self.restricoes = restricoes
        self.w = w
        self.objetivo = objetivo
        self.tabela = tabela
        self.matrix = []
        self.variaveis = variaveis
        self.base = []
    
    def monta_tabela_dual(self):
        
        variaveis = self.variaveis
        for idx, restricao in enumerate(self.tabela):
              variaveis.insert(len(variaveis)-1,'s'+str(idx+1))
       
       
        w = self.w
        w = w.tolist()
       
        
        for idx, restricao in enumerate(variaveis):
            if restricao.startswith('s') or restricao == 'b':
                w.insert(len(w), 0)
        w = np.array([w])
        nova_matrix = np.zeros((len(self.tabela), len(self.variaveis)))
        identidade = np.identity(nova_matrix.shape[0])
        tabela = np.array(self.tabela)
        
        if self.objetivo == 'max':
            tabela = tabela * (-1)
        
        tabela_sem_b = tabela[:,:-1]
        b = tabela[:,-1]
        tabela_com_identidade = np.concatenate((tabela_sem_b, identidade),axis = 1)
     
        
        nova_matrix = np.concatenate((tabela_com_identidade,b.reshape(-1,1)),axis = 1)
  
        nova_matrix = np.concatenate((w, nova_matrix))
       
        return nova_matrix
    def _monta_tabela_dual(self):
        print("DUAL")
        variaveis = self.variaveis
        for idx, restricao in enumerate(self.tabela):
              variaveis.insert(len(variaveis)-1,'s'+str(idx+1))
        for restricao in self.restricoes:
            if restricao == '>=':
               variaveis.insert(len(variaveis)-1,'s')

      
        nova_matrix = np.zeros((len(self.tabela), len(self.variaveis)))
        identidade = np.identity(nova_matrix.shape[0])
        tabela = np.array(self.tabela)
        if self.objetivo == 'max':
            tabela = tabela * (-1)
        tabela_sem_b = tabela[:,:-1]
        b = tabela[:,-1]
       
     
        tabela_com_identidade = np.concatenate((tabela_sem_b, identidade),axis = 1)
        
        nova_matrix = np.concatenate((tabela_com_identidade,b.reshape(-1,1)),axis = 1)
        return nova_matrix
    
    def linha_pivot(self, tabela):
     
        menor_valor = tabela[1:,-1][0]
        
        menor_valor_indice = 0
     
        for i in range(1,len(tabela[:,-1])):
            valor_atual = tabela[:,-1][i]
            if valor_atual < menor_valor:
                
                menor_valor = valor_atual
                menor_valor_indice = i
        if menor_valor_indice == 0:
            menor_valor_indice += 1
        return menor_valor, menor_valor_indice

    def coluna_pivot(self,tabela, indice_linha_pivot):
        funcao_objetivo = tabela[0]
       
        linha_pivot = tabela[indice_linha_pivot]
        nova_coluna = []
        menor_valor = 0
        indice_coluna_pivot = 0
        aux = 0 
        for i in range(len(linha_pivot) - 1):
            if (linha_pivot[i] != 0) & (funcao_objetivo[i] != 0):
                
                calculo = funcao_objetivo[i] / linha_pivot[i]
               
                if aux == 0: 
                    menor_valor = calculo 
                    indice_coluna_pivot = i
                else:
                    if calculo > menor_valor:
                        menor_valor = calculo 
                        indice_coluna_pivot = i
                aux += 1
        pivot = tabela[indice_linha_pivot][indice_coluna_pivot]
    
        tabela[indice_linha_pivot,:] = tabela[indice_linha_pivot,:] / pivot
       
     
        coluna_pivot = []
        aux = tabela.copy()
        for linha in range(0,len(tabela)):
            if linha != indice_linha_pivot:
                calculo = (tabela[linha, indice_coluna_pivot] * tabela[indice_linha_pivot, :]) * (-1)
                calculo += tabela[linha,:]
                
                tabela[linha,:] = calculo
      
        return tabela
        #print(tabela[indice_linha_pivot,indice_coluna_pivot])
        #return tabela, indice_coluna_pivot, coluna_escalonada
       
    def is_solved(self, tabela):

        zj_cj = tabela[1:,-1]
        
        resultado =  True if min(zj_cj) >= 0 else False 
        return resultado
    
    def desenha_tabela(self,tabela):
        x = PrettyTable()
        x.field_names = self.variaveis
        _tabela = tabela.tolist()
        for linha in range(len(_tabela)):
          for coluna in range(len(_tabela[linha])):
            _tabela[linha][coluna] = "{:.1f}".format(_tabela[linha][coluna])
        
     
        for linha in range(len(_tabela)):
            x.add_row(_tabela[linha])
        print(x)
     
    def exibe_resultados(self, tabela):
        z = tabela[0,-1]
        if self.objetivo == 'max':
            z *= (-1)
        df = pd.DataFrame(tabela, columns = self.variaveis)
        print(f"Z = {z}")
    
        for base in self.base:
            for idx, row in df.iterrows():
                if row[base] == 1:
                    print(f"{base} -> {tabela[idx,-1]}")
                    
    def resolve_dual(self):
        nova_tabela = self.monta_tabela_dual()
        print("Iteração - 1")
        
        self.desenha_tabela(nova_tabela)
        is_solved = False
        iter = 2
        while is_solved != True:
            print(f"Iteração - {iter}")
            menor_valor_linha, indice_linha_pivot = self.linha_pivot(nova_tabela)
            print(f"O menor valor da linha é {menor_valor_linha} e seu índice {indice_linha_pivot}, logo {self.variaveis[indice_linha_pivot]} entra na base.")
            self.base.append(self.variaveis[indice_linha_pivot])
            nova_tabela = self.coluna_pivot(nova_tabela, indice_linha_pivot)
            is_solved = self.is_solved(nova_tabela)
            self.desenha_tabela(nova_tabela)
            iter += 1
        print()
        self.exibe_resultados(nova_tabela)
     
        
