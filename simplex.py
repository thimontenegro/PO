import numpy as np 
import pandas as pd
class Simplex():
    def __init__(self,restricoes, variaveis,objetivo,matrix,is_big_m):
        self.restricoes = restricoes
        self.variaveis = variaveis
        self.objetivo = objetivo
        self.matrix = matrix
        self.big_m = is_big_m
        self.base = {}
        self.tabela = []
        self.v = variaveis
    
    def _mount_table(self):
        variaveis = self.variaveis.tolist()
        for idx, restricao in enumerate(self.restricoes):
            if restricao == '<=':
              variaveis.insert(len(variaveis)-1,"xf"+str(idx+1))
            elif restricao == '>=':
              variaveis.insert(len(variaveis)-1,'s'+str(idx+1))
            else:
              variaveis.insert(len(variaveis)-1,"a"+str(idx+1))
      
        for restricao in self.restricoes:
            if restricao == '>=':
               variaveis.insert(len(variaveis)-1,'s')
        
        self.variaveis = variaveis
       
        tabela = np.zeros((len(self.matrix), len(self.variaveis)))
        
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i]) - 1):
                tabela[i][j] = self.matrix[i][j]
            tabela[i][-1] = self.matrix[i][-1]
         
        identidade = np.identity(len(self.variaveis))
        print('identidade')
        print(identidade)
        tamanho = len(self.matrix[0])- 1
        for i in range(1, len(tabela)):
            for j in range(len(tabela[i]) - 1):
                if j >= tamanho:
                    tabela[i][j] = identidade[i-1][j-tamanho]
        return tabela
    
    def _get_column_pivot(self, tabela):
        funcao_objetivo = tabela[0,:-1]
        coluna_valor_inicial = funcao_objetivo[0]
        index_coluna_pivot = 0
        for i in range(1,len(funcao_objetivo)):
            valor_coluna_atual = funcao_objetivo[i]
            if valor_coluna_atual < coluna_valor_inicial:
                coluna_valor_inicial = valor_coluna_atual
                index_coluna_pivot = i
        return index_coluna_pivot, coluna_valor_inicial

    def get_line_pivot(self, tabela, index_coluna):
        valor_razao = 10
        indice_linha_pivot = 0

        for i in range(1,len(tabela)):
            valor_linha_coluna = tabela[i][index_coluna]
            print("valor linha coluna")
            print(valor_linha_coluna)
            if valor_linha_coluna > 0:
                b_valor_coluna = tabela[i][-1]
                teste_razao = b_valor_coluna / valor_linha_coluna
                
                if teste_razao < valor_razao:
                    valor_razao = teste_razao
                    indice_linha_pivot = i 
        print(f"Teste da Razao é {valor_razao}, e seu índice é {indice_linha_pivot}, logo  {self.variaveis[indice_linha_pivot]} sai da base.")
        linha_escalonada = []

        pivo = tabela[indice_linha_pivot][index_coluna]
       
        for i in tabela[indice_linha_pivot]:
            resultado = i/pivo
            linha_escalonada.append(resultado)
        tabela[indice_linha_pivot] = linha_escalonada
        return tabela, indice_linha_pivot, linha_escalonada
    
    def escalona_matrix(self, linha_tabela, linha_pivot, index_coluna_pivot):
        nova_linha = []
        pivot = linha_tabela[index_coluna_pivot] * (-1)
        for i in range(len(linha_tabela)):
            calculo = (linha_pivot[i] * pivot)
            calculo += linha_tabela[i]
            nova_linha.append(calculo)
        return nova_linha
    
    def is_solved(self,tabela):
        funcao_objetivo = tabela[0,:-1]
  
        resultado =  True if min(funcao_objetivo) >= 0 else False 
        return resultado

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
    
    def show_table(self,tabela):
        _tabela = tabela.tolist()
        for linha in range(len(_tabela)):
          for coluna in range(len(_tabela[linha])):
            _tabela[linha][coluna] = "{:.1f}".format(_tabela[linha][coluna])
        
        _tabela.insert(0,self.variaveis)
 
        for l in range(len(_tabela)):
            for c in range(len(_tabela[l])):
              print(f'{_tabela[l][c]:^5}',end='')
            print()     
    
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

    def _show_dual(self):
      w = []
      s = []
      r = []
      matriz = self.matrix
      for i in range(1,len(matriz)):
          for j in range(len(matriz[i])):
              if(j == len(matriz[i])-1):
                  w.append(matriz[i][j])
      inequacoes = self.restricoes
      for i in range(len(inequacoes)):
          if(inequacoes[i] == "<="):
              s.append(">=")
          elif(inequacoes[i] == ">="):
              s.append("<=")
      quant = len(matriz[1])-1
      rascunho = matriz[1:len(matriz)]
      tamanho = len(rascunho[1])-1
      for c in range(tamanho):
          a = []
          for i in range(len(rascunho)):
              for j in range(len(rascunho[i])-1):
                  if(j == c):
                      a.append(rascunho[i][j])
          r.append(a)
      for i in range(len(matriz[0])-1):
          r[i].insert(len(r)+1,matriz[0][i]*-1)
          
      print("w=", w)
      print("sinais=", s)
      for i in range(len(r)):
          print("r="+str(i+1), r[i])
      print()
      print("-----------")
      print("DUAL")


      w = self.matrix[1:,-1]
      
      #invertendo as inequacoes
      nova_tabela = self.matrix[1:]
      if self.objetivo == 'max':
        tabela_transposta = nova_tabela[:,:-1].T
        
        nova_tabela = np.insert(tabela_transposta,len(nova_tabela), values= (self.matrix[0,:-1]),axis = 1)
      else:
        for idx, restricoes in enumerate(self.restricoes):
          if restricoes == '<=':
            for _ in range(len(nova_tabela[idx])):
              nova_tabela[idx] = nova_tabela[idx] * (-1)
        
        tabela_transposta = nova_tabela[:,:-1].T
        
        nova_tabela = np.insert(tabela_transposta,len(nova_tabela), values= (self.matrix[0,:-1]),axis = 1)
           
        
      variaveis_w = []
      
      restricoes = ['<=' if restricao == '>=' else '>=' for restricao in self.restricoes]
      for i in range(len(restricoes)):
        nova_var = f"y_{i}"
        variaveis_w.append(nova_var)

    
      variaveis_w.append('b')
      self.variaveis = variaveis_w
    
      self.show_table(nova_tabela)

      print()
      if self.objetivo == 'max':
        max = 'Min Zy = '
        tamanho = len(variaveis_w) - 1
        for w_value, variavel_w in zip(w, variaveis_w):
          tamanho -= 1
          
          if tamanho <= 0:
            max+= f"{w_value}{variavel_w}"
          else: 
            max+= f"{w_value}{variavel_w} + "
       
       
        print(max)
        aux_2 = 0
     
     
        for coluna in range(len(nova_tabela)):
          s = ""
          aux = 0
          helper = len(nova_tabela[coluna])
        
          for linha in range(len(nova_tabela[coluna])):
        
            if aux == helper - 1:
             
              s+= f"{restricoes[0]} {nova_tabela[coluna][linha]}"
              aux_2 += 1
            else:
              if aux < helper - 2:
               
                s+= f' {nova_tabela[coluna][linha]}{variaveis_w[aux]} +'
              else:
            

                s+= f' {nova_tabela[coluna][linha]}{variaveis_w[aux]} '
            aux += 1
          print(s)
      else:
        
        min = "MAX Zy = "
        tamanho = len(variaveis_w) - 1
        for w_value, variavel_w in zip(w, variaveis_w):
          tamanho -= 1
            
          if tamanho <= 0:
            min+= f"{w_value}{variavel_w}"
          else: 
            min+= f"{w_value}{variavel_w} + "
        print(min)
        aux_2 = 0
        
        for coluna in range(len(nova_tabela)):
          s = ""
          aux = 0
          helper = len(nova_tabela[coluna])
        
          for linha in range(len(nova_tabela[coluna])):
        
            if aux == helper - 1:
             
              s+= f"<= {nova_tabela[coluna][linha]}"
              aux_2 += 1
            else:
              
              if aux < helper - 2:
                s+= f' {nova_tabela[coluna][linha]}{variaveis_w[aux]} +'
              else:
                s+= f' {nova_tabela[coluna][linha]}{variaveis_w[aux]} '
            aux += 1
          print(s)
      
    def run(self):
        tabela = self._mount_table()
        
        if self.big_m == True:
          
           tabela = self.add_dummy_variables(tabela)
           
           tabela = self._big_m_solver(tabela)
    
        if self.objetivo == 'max':
            tabela[0] = tabela[0] * (-1)
        
        is_solved = False 
        iter = 1

        print(f"Iteração - {iter}")
        print("------------------")
        self.show_table(tabela)
        print()

        while is_solved != True:
            
            index_pivot_column,coluna_valor_pivot = self._get_column_pivot(tabela)
            print(f"O menor valor da coluna é {coluna_valor_pivot} e seu índice {index_pivot_column}, logo {self.variaveis[index_pivot_column]} entra na base.")
            self.base[self.variaveis[index_pivot_column]] = coluna_valor_pivot
            tabela, indice_linha_pivot, linha_escalonada = self.get_line_pivot(tabela, index_pivot_column)
            for i in range(len(tabela)):
                if i != indice_linha_pivot:
                    tabela[i] = self.escalona_matrix(tabela[i], linha_escalonada, index_pivot_column)
            print()
            is_solved = self.is_solved(tabela)
            self.show_table(tabela)
            iter += 1
            print("---------------------")
            print(f"Iteração - {iter}")
        
        z = tabela[0][-1]
        if self.objetivo == 'min':
            print('Z = ',z * -(1))
        else:
            print("Z = ",z)

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
        self._show_dual()

print('MAX Z = 3x1 + 5x2 \n' +
     'x1 <= 4 \n' +
     '2x2 <= 12 \n' +
     '3x1 + 2x2 <= 18')

objetivo = "max"
matrix = np.array([[5,5,3,0],
                   [1,3,1,3],
                   [1,0,3,2],
                   [2,-1,2,4],
                   [2,3,-1,2]])

variaveis = np.array(["x1","x2",'x3',"b"])
retricoes = np.array(["<=","<=","<=",'<='])

is_big_m  = False
"""
print('MIN Z = 0.4x1 + 0.5x2 \n' +
     '0.3x1 + 0.1x2 <= 2.7 \n' +
     '0.5x1 + 0.5x2 = 6 \n' +
     '0.6x1 + 0.4x2 >= 6')

variaveis = np.array(["x1","x2","b"])
retricoes = np.array(["<=","=",">="])
matrix = np.array([[0.4,0.5,0], #fo
                  [0.3,0.1,2.7], # restricao 1 
                  [0.5,0.5,6], # restricao 2
                  [0.6,0.4,6]]) # restricao 3

objetivo = "min"
is_big_m = True
"""
simplex = Simplex(restricoes = retricoes,variaveis = variaveis,objetivo=objetivo,matrix=matrix, is_big_m = is_big_m)
simplex.run()

