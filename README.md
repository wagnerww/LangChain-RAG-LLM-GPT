# PDF Search Tool

Este projeto é uma ferramenta que permite realizar buscas em documentos PDF armazenados localmente. Ele utiliza LangChain, OpenAI GPT e vetores de embeddings para processar as informações contidas nos arquivos PDF e responder perguntas ou termos pesquisados.

---

## Requisitos

Antes de começar, certifique-se de ter os seguintes itens instalados no seu sistema:

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

Ou

```bash
pip install langchain langchain-openai openai faiss-cpu PyMuPDF tiktoken chromadb
```

---

## Configuração

### Variáveis Necessárias
Antes de executar o programa, configure as variáveis de ambiente:

- `API_KEY`: Sua chave de API da OpenAI (você pode gerá-la [aqui](https://platform.openai.com/account/api-keys)).
- `GPT_MODEL`: O modelo GPT a ser utilizado (ex.: `gpt-3.5-turbo` ou `gpt-4`).
- `FOLDER_PATH`: O caminho absoluto da pasta onde estão armazenados os PDFs no seu sistema.

Exemplo de configuração no terminal:
```bash
export API_KEY="sua-chave-openai"
export GPT_MODEL="gpt-3.5-turbo"
export FOLDER_PATH="/home/wagnerwagner/Downloads"
```

Para sistemas Windows (PowerShell):
```powershell
$env:API_KEY="sua-chave-openai"
$env:GPT_MODEL="gpt-3.5-turbo"
$env:FOLDER_PATH="C:\\Users\\wagnerwagner\\Downloads"
```


---

## Execução

### 1. Execute o script principal
```bash
python main.py
```

### 2. Digite a pergunta ou termo para busca
O programa solicitará que você insira uma consulta. Exemplo:
```
Digite o termo ou pergunta a ser pesquisado nos PDFs: O que é LangChain?
```

### 3. Saída esperada
A resposta incluirá:
- Uma resposta direta à pergunta.
- Lista dos PDFs relevantes onde a informação foi encontrada.
- Referências de páginas/seções (se disponíveis).

Exemplo:
```
Resposta: LangChain é uma biblioteca para integrar modelos de linguagem com fontes externas de dados.
PDFs relevantes encontrados:
- /home/user/Downloads/doc1.pdf (Página 3)
- /home/user/Downloads/doc2.pdf (Seção 2.3)
```