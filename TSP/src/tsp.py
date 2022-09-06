import os
import sys 
import itertools
from typing import Union
import concurrent.futures
from tools.tools import Tools

FILE_SAVE:str = "./data/resultados/resultados.csv";

@Tools.benchmarkingFunction
def tsp(matriz:list[list[int]]=[],inicio:int=0,arquivo:str=None) -> tuple[int,Union[str,None]]:
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
        tuple: Nós retornamos uma tupla com o valor do menor e o 
        arquivo.
    """
    try:
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
            
        return menor_caminho,arquivo;
    except Exception as erro:
        print(f"Erro: {erro}");
        return -1 * sys.maxsize,None; 


if __name__ == "__main__":
    try:
        with open(FILE_SAVE,'w') as writer:
            cabecalho:str = "Arquivo,Resultado,Tempo";
            writer.write(f"{cabecalho}\n");
    except Exception as erro:
        print(f"Erro: {erro}")
        sys.exit(0);
    try:
        arquivos = Tools.getFiles(path="./data/matrizes");
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = (
                executor.submit(
                    tsp,
                    matriz=Tools.readFileMatriz(
                        file=os.path.join(
                            "./data/matrizes",
                            arquivo
                        )
                    ),
                    arquivo=arquivo
                )
                for arquivo in Tools.getFiles(path="./data/matrizes")
            );
            
            for result in concurrent.futures.as_completed(tasks):
                resultado = result.result();
                mensagem:str = (
                    f"{resultado['return'][1]},"
                    f"{resultado['return'][0]},"
                    f"{float(resultado['Tempo']):.4f}"
                );
                
                Tools.saveData(
                    file=FILE_SAVE,
                    data=mensagem
                );
    except Exception as erro:
        print(f"Erro: {erro}");