import os
import sys 
import itertools
import numpy as np
import networkx as nx
import concurrent.futures
from tools.tools import Tools
from pytsp.utils import minimal_spanning_tree
from networkx.algorithms.euler import eulerian_circuit
from networkx.algorithms.matching import max_weight_matching

FILE_SAVE:str = "./data/resultados/resultados_christofides.csv";

@Tools.benchmarkingFunction
def christofides(matriz:list[list[int]]=[],inicio:int=0,arquivo:str=None) -> tuple[int,str,list[str]]:
      def run(matriz:list[list[int]]=[]) -> list[int]:
            """Gera a lista com os caminhos com o algoritmo de christofides.

            Returns:
                  list[int]: Lista dos caminhos passados.
            """
            matriz = np.array(matriz);
            mst = minimal_spanning_tree(
                  matriz, 
                  'Prim', 
                  starting_node=0
            );

            odd_degree_nodes = list(
                  _get_odd_degree_vertices(
                        mst
                  )
            );
            
            odd_degree_nodes_ix = np.ix_(
                  odd_degree_nodes, 
                  odd_degree_nodes
            );
            
            nx_graph = nx.from_numpy_array(
                  -1 * matriz[odd_degree_nodes_ix]
            );
            
            matching:set = max_weight_matching(
                  nx_graph, 
                  maxcardinality=True
            );
            
            euler_multigraph = nx.MultiGraph(mst);
            
            for edge in matching:
                  euler_multigraph.add_edge(
                        odd_degree_nodes[edge[0]], 
                        odd_degree_nodes[edge[1]],
                        weight=matriz[
                              odd_degree_nodes[edge[0]]
                        ][
                              odd_degree_nodes[edge[1]]
                        ]
                  );
                  
            euler_tour = list(
                  eulerian_circuit(
                        euler_multigraph, 
                        source=inicio
                        )
            );
            
            path = list(
                  itertools.chain.from_iterable(
                        euler_tour
                  )
            );
            
            return _remove_repeated_vertices(
                  path, 
                  inicio
            )[:-1];

      def _get_odd_degree_vertices(matriz:np.ndarray=[]) -> set:
            """
            Procura todos os vertices de grau impar na matriz.
            Args:
                  matriz: Recebemos um NDArray 2D.
            Returns:
                  set: Retorna o set com conjunto de vertices
                  ímpar.
            """
            odd_degree_vertices = set();
            for index, row in enumerate(matriz):
                  if len(np.nonzero(row)[0]) % 2 != 0:
                        odd_degree_vertices.add(index);
            return odd_degree_vertices;

      def _remove_repeated_vertices(path:list[int],inicio:int=0) -> list[int]:
            """
            Remove todos os valores repetidos.

            Args:
                  path (list[int]): Lista de valores.
                  inicio (int, optional): Valor de inicio.

            Returns:
                  list[int]: retorna a lista sem repetições.
            """
            path = list(dict.fromkeys(path).keys());
            path.append(inicio);
            return path;
      
      def main() -> tuple[int,list[str]]:
            """
            Gera um retorno mais bonito para o algoritmo.

            Returns:
                  tuple[int,list[str]]: _description_
            """
            caminhos = run(matriz);
            novos_caminhos:list[str] = [];
            i = inicio;
            contador = 0;

            for j in caminhos[1:]:
                  novos_caminhos.append(
                        f"{i} -> {j} = {matriz[i][j]}"
                  );
                  contador += matriz[i][j];
                  i = j;
            novos_caminhos.append(
                  f"{j} -> {inicio} = {matriz[j][inicio]}"
            );
            contador += matriz[j][inicio];

            return (contador, arquivo, novos_caminhos);

      return main();


if __name__ == "__main__":
      print("#"*50);
      print("Programa Iniciado");
      print("#"*50);
      try:
            with open(FILE_SAVE,'w') as writer:
                  cabecalho:str = "Arquivo,Resultado,Tempo,Caminho";
                  writer.write(f"{cabecalho}\n");
      except Exception as erro:
            print(f"Erro: {erro}");
            sys.exit(0);
      try:
            arquivos = Tools.getFiles(path="./data/matrizes");
            for arquivo in arquivos:
                  resultado = christofides(
                        matriz=Tools.readFileMatriz(
                              file=os.path.join(
                              "./data/matrizes",
                              arquivo
                              )
                        ),
                        arquivo=arquivo
                  )
                  mensagem:str = (
                        f"{resultado['return'][1]},"
                        f"{resultado['return'][0]},"
                        f"{float(resultado['Tempo']):.4f},"
                        f"{resultado['return'][2]}"
                  );
                  
                  Tools.saveData(
                        file=FILE_SAVE,
                        data=mensagem
                  );
      except Exception as erro:
            print(f"Erro: {erro}");
      print("#"*50);
      print("Finalizado");
      print("#"*50);
