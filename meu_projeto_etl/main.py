import requests

from src.controller.sheets import SheetsController


def extrair_vendas():
    url = "https://dummyjson.com/carts"
    response = requests.get(url)
    response.raise_for_status()
    dados = response.json()
    return dados["carts"]


def run_etl():
    print("iniciando teste de conexão...")

    # 1. Instancia o controller
    db = SheetsController()

    # 2. Chama o método de teste
    print(db.testar_conexao())

    # 3. Resto do seu código...
    # db.append_data(['Exemplo', 'Dados', '123'])
    vendas = extrair_vendas()
    print(f"Total de registros extraídos: {len(vendas)}")
    print(vendas[0])
    cabecalho =["ID Carrinho", "ID Usuário", "Produto", "Preço", "Quantidade", "Total"]
    db.escrever_cabecalho(cabecalho)
    linhas = []


    for carrinho in vendas:
        for produto in carrinho["products"]:
            linha = [
                carrinho["id"],
                carrinho["userId"],
                produto["title"],
                produto["price"],
                produto["quantity"],
                produto["total"]
            ]
            linhas.append(linha)


if __name__ == "__main__":
    run_etl()