import sys 
import itertools
from tools.tools import Tools

path  :str             = "./data/";
matriz:list[list[int]] = Tools.readFileMatriz(
    f"/home/diaszano/Programas/Python/AEDIII/TSP/tsp/data/tsp1_253.txt"
);

def tsp(matriz:list[list[int]]=[],inicio:int=0) -> int:
    """Problema do Caixeiro Viajante (TSP)
    
    Dado um conjunto de cidades e distâncias entre cada par de cidades, 
    o problema é encontrar a rota mais curta possível que visite cada 
    cidade exatamente uma vez e retorne ao ponto de partida.
    
    Args:
        matriz (list[list[int]]): Temos como nosso primeiro argumento 
        a matriz que contem os valores das distâncias as 
        quais devemos encontrar o menor valor. 
        inicio (int, optional): Temos como nosso segundo argumento e sendo totalmente
        opcional o local de início da busca da menor rota.

    Returns:
        int: Nós retornamos o menor valor encontrado pelo algorítimo.
    """
    vertex:list[int] = (
        i
        for i in range(len(matriz))
            if i != inicio
    );
    menor_caminho:int = sys.maxsize;
    
    for i in itertools.permutations(vertex):
        caminho_atual:int = 0;
        k            :int = inicio;
        
        for j in i:
            caminho_atual += matriz[k][j];
            k = j;
            
        caminho_atual += matriz[k][inicio];
        menor_caminho = min(menor_caminho, caminho_atual);
        
    return menor_caminho;


if __name__ == "__main__":
    print(tsp(matriz))
