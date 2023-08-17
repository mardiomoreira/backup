from usuario import listar_diretorios_usuario

def lst_valores_BARRA(t_lst):
    pass
    num_itens = t_lst
    ultimo_valor_desejado = 400

    incremento = (ultimo_valor_desejado - num_itens) / (num_itens - 1)

    valores = [i * incremento for i in range(num_itens)] + [ultimo_valor_desejado]
    lst_valores=[]
    for num in valores:
        v=int(num)
        lst_valores.append(v)
    return lst_valores
# tamanho=6
# valores=lst_valores_BARRA(t_lst=7)
# print(valores)
# for valor in valores:
#     print(int(valor))
# for v,num in enumerate(valores):
#     print(valores[v])