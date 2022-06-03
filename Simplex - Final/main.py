import simplex_final as simplex

funcao_objetivo = 'max'
funcao_objeto_valores = '5*x1 + 5*x2 + 3*x3'
restricoes = ['1*x1 + 3*x2 + 1*x3 <= 3','1*x1 + 3*x3  <= 2', '2*x1 - 1*x2 + 2*x3 <= 4', '2*x1 + 3*x2 - 1*x3 <= 2']
big_M = False
#funcao_objetivo = 'min'
#funcao_objeto_valores = '10*x1 + 7*x2'
#restricoes = ['2*x1 + 2*x2 >= 10', '3*x1 + 1*x2 = 5']
#big_M = True

simplex = simplex.Simplex(objetivo=funcao_objetivo, funcao_objetivo=funcao_objeto_valores, restricoes=restricoes, is_big_m=big_M)
simplex.run()
#simplex = simplex.Simplex(restricoes = retricoes,variaveis = variaveis,objetivo=objetivo,matrix=matrix, is_big_m = is_big_m)
