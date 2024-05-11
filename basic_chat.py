import google.generativeai as genai
from rich import print
from rich.panel import Panel

# --- CONFIGURAÇÃO DA CHAVE DE ACESSO E ESCOLHA DO MODELO ---

# Define a chave de API do Google Generative AI e a instrução do sistema para a IA.
genai.configure(api_key="SUA_API_KEY_AQUI")

# DEFINE A INSTRUÇÃO DO SISTEMA
system_instruction = """Agora você é uma assistente chamada Tyna que ajuda mulheres ou homens com suspeita de câncer de mama. 
Seu objetivo é auxiliar essas pessoas e caso haja suspeitas de câncer você deve auxiliar a procurar um médico. 
Você foi desenvolvido por um profissional especialista em criação de modelos de IA fornecendo somente respostas 
confiáveis de sites e instituições renomadas."""


# CRIAÇÃO DOS DATAFRAMES
IDADE = {
    "Titulo": "Idade",
    "Conteudo": [
        "Até os 49 anos: 1 caso a cada 51 mulheres",
        "Entre 50 e 59 anos: 1 caso a cada 43 mulheres.",
        "Entre 60 a 69 anos: 1 caso a cada 23 mulheres",
        "Acima dos 70 anos: 1 caso a cada 15 mulheres.",
    ],
}
SINTOMAS = {
    "Titulo": "Sintomas",
    "Conteudo": [
        "Dor no peito",
        "Retrações de pele",
        "Aspecto de casca de laranja",
        "Secreção mamilar",
        "Nódulo",
        "Massa",
        "Inchaço",
        "Vermelhidão",
        "Coceira",
        "Endurecimento",
        "Dor",
        "Secreção aquosa ou Sanguinolanta",
        "Inversão do mamilo",
        "Irratação na pele",
        "Bordas da Auréola irregulares",
        "Linfodo aumentado",
    ],
}
CUIDADOS = {
    "Titulo": "Cuidados",
    "Conteudo": [
        "Evitar alimentos gordurosos",
        "Mantenha uma alimentação saudável",
        "Pratique atividades físicas",
        "Evite o consumo de álcool",
        "Evite o consumo de tabaco",
        "Evite alimentos gordurosos",
        "Evite alimentos industrializados",
        "Evite alimentos processados",
        "Evite alimentos com agrotóxicos",
        "Evite alimentos com conservantes",
        "Evite alimentos com corantes",
        "Evite alimentos com sódio",
        "Evite alimentos com açúcar",
        "Evite alimentos com gordura saturada",
        "Evite alimentos com gordura",
    ],
}
HISTORICO_FAMILIAR = {
    "Titulo": "Histórico Familiar",
    "Conteudo": [
        "Mãe com câncer de mama",
        "A história familiar, principalmente em parentes de primeiro grau, é considerada um importante fator de risco para o câncer de mama antes dos 50 anos",
        "história familiar de câncer de mama em parente de primeiro grau antes dos 50 anos ou de câncer bilateral ou de ovário em qualquer idade"
        "história familiar de câncer de mama masculino, é diagnóstico histopatológico de lesão mamária proliferativa com atipia ou neoplasia lobular",
    ],
}
EXAMES = {
    "Titulo": "Exames",
    "Conteudo": ["Mamografia", "Biópsias", "Ultrassonografia", "Ressonância Magnética"],
}
SOLUCAO = {
    "Titulo": "Solução",
    "Conteudo": [
        "Procure um médico especialista",
        "Faça exames regularmente",
        "Realize uma Mamografia",
    ],
}
documents = [IDADE, SINTOMAS, CUIDADOS, HISTORICO_FAMILIAR, EXAMES, SOLUCAO]

# --- VARIÁVEL GLOBAL documents ---

# Armazena todos os documentos em uma lista.
documents = [IDADE, SINTOMAS, CUIDADOS, HISTORICO_FAMILIAR, EXAMES, SOLUCAO]


# --- FUNÇÃO PARA BUSCAR DOCUMENTO RELEVANTE ---


# Busca no título e conteúdo dos documentos por palavras-chave presentes na consulta do usuário.
def buscar_documento_relevante(consulta, documents):
    for doc in documents:
        # Verifica se alguma palavra do título ou do conteúdo do documento está presente na consulta
        for palavra in doc["Titulo"].lower().split():
            if palavra in consulta.lower():
                return doc
        for frase in doc["Conteudo"]:
            if frase.lower() in consulta.lower():
                return doc
    return None


# --- LOOP PRINCIPAL ---

if __name__ == "__main__":
    while True:

        # Pede a consulta do usuário
        consulta = input("Digite sua pergunta: (Digite 'desligar' para sair): ")
        if consulta.lower() == "desligar":
            print("Até mais! Espero ter ajudado. 😊")
            break

        # Busca o documento relevante
        documento_relevante = buscar_documento_relevante(consulta, documents)

        # Gera resposta com base no documento relevante
        if documento_relevante:
            prompt = f"{system_instruction} {consulta} Aqui estão algumas informações sobre {documento_relevante['Titulo']}: {', '.join(documento_relevante['Conteudo'])}"
        else:
            prompt = f"{system_instruction} {consulta}"

        # Gera a resposta usando o modelo 'gemini-pro'
        model_2 = genai.GenerativeModel("gemini-pro")
        response = model_2.generate_content(prompt)

        # Formata a saída da resposta usando a biblioteca "rich", exibindo a pergunta e a resposta em painéis.
        print(Panel(f"[bold blue]Pergunta:[/] {consulta}"))
        print(Panel(response.text, title="Resposta", expand=False))
