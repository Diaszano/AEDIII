import gurobipy as gp
from tools.tools import Tools

path = "./data/";

matriz = Tools.readFileMatriz(
    f"{path}{next(Tools.getFiles(path=path))}"
);

quantidade_pontos = len(matriz);
origens = [i + 1 for i in range(quantidade_pontos)];
destinos = [i + 1 for i in range(quantidade_pontos)];

print(f"Matriz:\n{matriz}\nQuantidade de Pontos: {quantidade_pontos}");
print(f"Origem:\n{matriz}\nQuantidade de Pontos: {quantidade_pontos}");
