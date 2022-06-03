def inverter_z(z):
    nvz = []
    for i in z:
        nvz.append(i*-1)
    return nvz

def desenhar_tabela(variaveis,matriz):
    tabela = []
    for i in range(len(matriz)):
        aux =[]
        for j in range(len(variaveis)):
            aux.append(0)
        tabela.append(aux)
    return tabela   
   

def adicionar_variaveis_base(matriz,tabela):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])-1):
            tabela[i][j] = matriz[i][j]
        tabela[i][len(tabela[i])-1] = matriz[i][len(matriz[i])-1]
    return tabela
       
def criar_matriz_identidade(inequacoes):   
    matriz = []
    for i in range(len(inequacoes)):
        aux = []
        for j in range(len(inequacoes)):
            if(i == j):
                aux.append(1)
            else:
                aux.append(0)           
        matriz.append(aux)
                
    return matriz 
                       
def criar_tabela_completa(tabela,identidade,matriz):
    tamanho = len(matriz[1])-1
    for i in range(1,len(tabela)):
        for j in range(len(tabela[i])-2):
            if(j >= tamanho):
                tabela[i][j] = identidade[i-1][j-tamanho]
    return tabela            
    
def coluna_pivo(tabela):
    funcaoObjetivo = tabela[0]
    funcaoObjetivo = funcaoObjetivo[0:len(funcaoObjetivo)-1]
    valor = funcaoObjetivo[0]
    for i in funcaoObjetivo:
        if(i < valor):
            valor = i
    return tabela[0].index(valor)        
    

def linha_pivo(tabela,colunaPivo):
    menorValor = 10**100
    menorIndice = 0
    for i in range(1,len(tabela)):
        if(tabela[i][colunaPivo] > 0):
           divisao = tabela[i][len(tabela[i])-1]/tabela[i][colunaPivo]
           if(divisao < menorValor):
               menorValor = divisao
               menorIndice = i
    return menorIndice
           

def nova_linha_pivo(tabela,linha,coluna):
    pivo = tabela[linha][coluna]
    novaLinhaPivo = []
    for i in tabela[linha]:
        resultado = i/pivo
        novaLinhaPivo.append(resultado)
    return novaLinhaPivo

def nova_linha(linha,colunaPivo,novaLinhaPivo):
    novaLinha = []
    pivo = linha[colunaPivo] *-1
    for i in range(len(linha)):
        multi = pivo*novaLinhaPivo[i]
        novaLinha.append(multi+linha[i])
    return novaLinha   
    

def solucao(tabela):
    fo = tabela[0]
    fo = fo[0:len(fo)-1]
    valor = min(fo)
    if(valor >= 0):    
        return True
    return False        
               
def reduzir_casas(tabela):  
    for i in range(len(tabela)):
        for j in range(len(tabela[i])):
            tabela[i][j] = "%.1f"%tabela[i][j]
    return tabela

def gerar_variaveis(simbolos,variaveis):  
    for i in range(len(simbolos)):        
        if(simbolos[i]=="<="):
            variaveis.insert(len(variaveis)-1,"xf"+str(i+1))
        elif(simbolos[i]==">="):            
            variaveis.insert(len(variaveis)-1,"a"+str(i+1))
                        
        else:
            variaveis.insert(len(variaveis)-1,"a"+str(i+1))
            
    return variaveis

def adicionar_s(inequacoes,variaveis):
    for i in inequacoes:
        if(i == ">="):
            variaveis.insert(len(variaveis)-1,"s")
    return variaveis

def adicionar_sobras(tabela,variaveis,inequacoes):
    coluna = variaveis.index("s")
    linhas = []
    for i in range(len(inequacoes)):
        if(inequacoes[i] == ">="):
            linhas.append(i+1)
    
    for i in range(len(linhas)):
        tabela[linhas[i]][coluna] = -1
    return tabela       
        
        

def mostrar_tabela(variaveis,tabela):
    tabela = reduzir_casas(tabela)
    tabela.insert(0,variaveis)
    for l in range(len(tabela)):
        for c in range(len(tabela[l])):
            print(f'[{tabela[l][c]:^5}]',end='')
        print()

def mostrar_z(tabela,variaveis):
    return tabela[1][len(variaveis)-1]

def adicionar_M(z,variaveis):
    for i in range(len(z)):
        if(variaveis[i][0]=="a"):
            z[i] = 100000
    return z    

       
def mao_direita(s,db,b):
    soma = 0
    for i in range(len(s)):
        for j in range(len(db)):
            if(i==j):
                soma+=(s[i]*db[j])
    if(soma == 0):
        return "infinito"
    return b/-soma

def cria_big_M(tabela,inequacoes):
    rascunho = tabela[1:len(tabela)]
    aux = []
    for i in rascunho[0]:
        aux.append(0)
    for i in range(len(rascunho)):
        for j in range(len(rascunho[i])):
            if(inequacoes[i]!="<="):
                aux[j] = aux[j]+rascunho[i][j]
    for i in range(len(aux)):
        aux[i]*=-100000
    for i in range(len(tabela[0])):
        tabela[0][i] = tabela[0][i] + aux[i]
    return tabela
    
def mostrar_dual(matriz,inequacoes):
    w = []
    s = []
    r = []
    for i in range(1,len(matriz)):
        for j in range(len(matriz[i])):
            if(j == len(matriz[i])-1):
                w.append(matriz[i][j])
    
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
            
    continua = False
big_M = False

"""#Ex 1
print("Max 3x1 + 5x2")
print("x1 <=4")
print("2x2 <=12")
print("3x1 + 2x2 <=18")
z = [3,5,0]
r1 = [1,0,4]
r2 = [0,2,12]
r3 = [3,2,18]
objetivo = "max"
matriz = [z,r1,r2,r3]
inequacoes = ["<=","<=","<="]
v = ["x1","x2","b"]"""

"""#Ex 2
print("Max z = 4x1 + x2")
print("2x1 + x2 <=8")
print("2x1 + 3x2 <=12")
objetivo = "max"
z = [4,1,0]
r1 = [2,1,8]
r2 = [2,3,12]
v = ["x1","x2","b"]
inequacoes = ["<=","<="]
matriz = [z,r1,r2]"""

"""
#Ex 3
print("Min 10x1 + 7x2")
print("2x1 + 2x2 >= 10")
print("3x1 + x2 = 5")
objetivo = "min"
z = [10,7,0]
r1 = [2.0,2.0,10.0]
r2 = [3.0,1.0,5.0]
v = ["x1","x2","b"]
inequacoes = [">=","="]
matriz = [z,r1,r2]
big_M = True"""


"""#Ex 4
print("Min 1700x1 + 750x2 + 800x3")
print("2x1+2x2+5x3>=20")
print("3x1+x2+5x3=10")
inequacoes = [">=","="]
v = ["x1","x2","x3","b"]
objetivo = "min"
z = [1700,750,800,0]
r1 = [2,2,5,20]
r2 = [3,1,5,10]
matriz = [z,r1,r2]
big_M = True"""

#Ex 5
print("Min z = 0,4x1 + 0,5x2")
print("0,3x1 + 0,1x2 <= 2,7")
print("0,5x1 + 0,5x2 = 6")
print("0,6x1+0,4x2 >=6")
z = [0.4,0.5,0]
r1 = [0.3,0.1,2.7]
r2 = [0.5,0.5,6]
r3 = [0.6,0.4,6]

matriz = [z,r1,r2,r3]
v = ["x1","x2","b"]
inequacoes = ["<=","=",">="]
objetivo = "min"
big_M = True




variaveis =gerar_variaveis(inequacoes,v)
variaveis = adicionar_s(inequacoes,variaveis)
base = desenhar_tabela(variaveis,matriz)
tabela = adicionar_variaveis_base(matriz,base)
identidade = criar_matriz_identidade(inequacoes)
tabela = criar_tabela_completa(tabela,identidade,matriz)

    
if(big_M == True):
    tabela = adicionar_sobras(tabela,variaveis,inequacoes)
    tabela[0] = adicionar_M(tabela[0],variaveis)
    tabela = cria_big_M(tabela,inequacoes)

if(objetivo == "max"):
    tabela[0] =inverter_z(tabela[0])

cont = 0
continua = False
while(continua!=True):
    colunaPivo = coluna_pivo(tabela)          
    linhaPivo =linha_pivo(tabela,colunaPivo)
    novaLinhaPivo = nova_linha_pivo(tabela,linhaPivo,colunaPivo)
    tabela[linhaPivo] = novaLinhaPivo    
    for i in range(len(tabela)):
        if(i!=linhaPivo):
            tabela[i] =nova_linha(tabela[i],colunaPivo,novaLinhaPivo)               
    continua = solucao(tabela)
    cont+=1
    
        
so = mostrar_tabela(variaveis,tabela)
z = float(mostrar_z(tabela,variaveis))
if(objetivo == "min"):
    print("z = ",z*-1)
else:    
    print("z = ",z)
print("Número de iterações:",cont)



 
       
      
               
           
        

