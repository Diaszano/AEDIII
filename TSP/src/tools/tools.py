import os
import re
import time
from typing import Generator, Union


class Tools():
    """Tools
    
    Está classe tem como seu intuito fazer todas as coias
    triviais que usaremos neste exercício. 
    """
    
    def __init__(self) -> None:
        super().__init__();
        
    def generateFilesPythonMatriz(self,path:str="./") -> None:
        """Generate Files Python
        
        Neste método criamos os arquivos python que contém uma 
        matriz.

        Args:
            path (str, optional): Caminho da pasta aonde tem esses arquivos. Defaults to "./".
        """
        try:
            for file in self.getFiles(path=path):
                local_file = os.path.join(path,file);
                matriz = self.readFileMatriz(file=local_file);
                [status,_] = self.createFilePythonMatriz(
                    matriz=matriz,
                    file_name=os.path.splitext(file)[0],
                    path=path
                );
                
                if(status):
                    print(f"Foi criado o arquivo {os.path.splitext(file)[0]}.py");
                else:
                    print(f"Tivemos erro com o arquivo {file}");
                
        except Exception as erro:
            print(f"Erro: {erro}");
            return;
    
    
    @staticmethod
    def getFiles(path:str="./",type_file:str=".txt") -> Generator[str,None,None]:
        """Get Files
        
        Neste método iremos pegar todos so arquivos com a extensão 
        envida e retornaremos a lista com todos os arquivos
        encontrados na pasta enviada.

        Args:
            path (str, optional): Pasta aonde se quer procurar os arquivos. Defaults to "./".
            type_file (str, optional): Tipo de arquivo a ser procurado. Defaults to ".txt".

        Returns:
            Generator[str,None,None]: A lista com todos os arquivos solicitados.
        """
        if(not "." in type_file):
            type_file = f".{type_file}";
        
        try:
            arquivos = (
                arquivo
                for _, _, arquivos in os.walk(path)
                    for arquivo in arquivos
                        if type_file.lower() == os.path.splitext(arquivo)[1].lower()
            );
            return arquivos;
        except Exception as erro:
            print(f"Erro: {erro}");
            return [];
    
    @staticmethod
    def readFileMatriz(file:str='arq.txt') -> list[list[int]]:
        """Read File Matriz
        
        Neste método nós lemos um arquivo que contém uma matriz de
        n x n posições e colocamos ela em uma variável. 

        Args:
            file (str, optional): caminho do arquivo a ser lido. Defaults to 'arq.txt'.

        Returns:
            list[list[int]]: retornamos a matriz de inteiros.
        """
        try:
            with open(file, encoding="ISO-8859-1") as ficheiro:
                reader = ficheiro.readlines();
                
                data:list[list[int]] = [];
                for line in reader:
                    line = re.findall(r"(?P<Number>[0-9]+)+",line);
                    data.append(
                        [int(valor) for valor in line]
                    );
            return data;
        except Exception as erro:
            print(f"Erro: {erro}");
            return [];
    
    @staticmethod
    def createFilePythonMatriz(matriz:list[list[int]]=[],file_name:str="dzn",path:str="./") -> tuple[bool,Union[str,None]]:
        """Create File Python
        
        Neste método fazemos a criação do arquivo python com a matriz de valores inteiros.

        Args:
            matriz (list[list[int]], optional): Matriz de valores inteiros. Defaults to [].
            file_name (str, optional): Nome do arquivo python. Defaults to "dzn".
            path (str, optional): caminho para ser salvo o aquivo. Defaults to "./".

        Returns:
            tuple[bool,Union[str,None]]: Retorna o se foi feito com sucesso e seu caminho completo.
        """
        try:
            file = os.path.join(path,f"{file_name}.py");
            with open(file,'w') as writer:
                matriz = str(matriz).replace('], ','],\n');

                texto:str = (
                    f"{file_name} = {matriz}"
                );
                
                writer.write(texto);
                
                return (True,file);
                
        except Exception as erro:
            print(f"Erro: {erro}");
            return (False,None);
    
    @staticmethod
    def benchmarkingFunction(func):
        """Benchmarking de Função
        
        Neste método temos um decorador de função, que tem como
        seu proposito fazer o cálculo do tempo que uma função 
        demora para ser executada.

        Args:
            func (function): Função a ser testada.
        """
        def run_function(*args, **kwargs):
            inicio = time.time();
            resultado = func(*args, **kwargs);
            fim = time.time();
            
            tempo:float = fim-inicio;
            
            print(f'Função[{func.__name__!r}] executada em {(tempo):.4f}s');
            
            retorno:dict = {
                "return":resultado,
                "Tempo":tempo
            };
            
            return retorno;
        
        return run_function;
    
    @staticmethod
    def saveData(file:str="",data:str=""):
        try:
            with open(file,'a') as writer:
                writer.write(f"{data}\n");
        except Exception as erro:
            print(f"Erro: {erro}");


if __name__ == "__main__":
    pass;