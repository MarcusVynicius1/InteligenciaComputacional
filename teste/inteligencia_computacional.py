import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definindo as variáveis do universo
preco = ctrl.Antecedent(np.arange(0, 1.1, 0.1), "preco")
produto = ctrl.Antecedent(np.arange(0, 1.1, 0.1), "produto")
mercado = ctrl.Consequent(np.arange(0, 1.1, 0.1), "mercado")

# Definindo as funções de pertinência
preco.automf(number=3, names=["barato", "meio_caro", "caro"])
produto.automf(number=3, names=["feio", "meio_feio", "bonito"])
mercado["nao_comprar"] = fuzz.trimf(mercado.universe, [0, 0, 0.5])
mercado["comprar_medio"] = fuzz.trimf(mercado.universe, [0, 0.5, 1])
mercado["comprar_alto"] = fuzz.trimf(mercado.universe, [0.5, 1, 1])

# Definindo as regras
rule1 = ctrl.Rule(preco["caro"] & produto["bonito"], mercado["comprar_medio"])
rule2 = ctrl.Rule(preco["caro"] & produto["meio_feio"], mercado["nao_comprar"])
rule3 = ctrl.Rule(preco["meio_caro"] & produto["bonito"], mercado["comprar_alto"])
rule4 = ctrl.Rule(preco["meio_caro"] & produto["meio_feio"], mercado["nao_comprar"])

# Adicionando as regras ao sistema de controle
investimento_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])

# Criando o simulador
simulando_investimento = ctrl.ControlSystemSimulation(investimento_ctrl)


# Função para testar o sistema fuzzy
def testar_sistema(preco_input, produto_input):
    # Define os valores de entrada do simulador fuzzy
    simulando_investimento.input["preco"] = preco_input
    simulando_investimento.input["produto"] = produto_input

    # Computa os valores fuzzy
    simulando_investimento.compute()

    # Obtém a saída do sistema fuzzy
    output_mercado = simulando_investimento.output["mercado"]

    # Retorna a resposta fuzzy correspondente
    return output_mercado


# Solicita ao usuário para inserir os valores de teste
preco_input = float(input("Insira o valor para o preço (entre 0 e 1): "))
produto_input = float(input("Insira o valor para o produto (entre 0 e 1): "))

resposta_fuzzy = testar_sistema(preco_input, produto_input)
print(
    "A resposta fuzzy para o preço",
    preco_input,
    "e o produto",
    produto_input,
    "é:",
    resposta_fuzzy,
)

# Plot dos gráficos de entrada e saída
fig, axs = plt.subplots(3, 1, figsize=(10, 18))

preco.view(sim=simulando_investimento, ax=axs[0])
axs[0].set_title("Função de Pertinência - Preço")
axs[0].set_xlabel("Preço")
axs[0].set_ylabel("Pertinência")

produto.view(sim=simulando_investimento, ax=axs[1])
axs[1].set_title("Função de Pertinência - Produto")
axs[1].set_xlabel("Produto")
axs[1].set_ylabel("Pertinência")

mercado.view(sim=simulando_investimento, ax=axs[2])
axs[2].set_title("Função de Pertinência - Mercado")
axs[2].set_xlabel("Mercado")
axs[2].set_ylabel("Pertinência")

plt.tight_layout()
plt.show()
