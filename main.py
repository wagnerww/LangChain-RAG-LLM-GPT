import os
import langchain
from langchain.document_loaders import PyMuPDFLoader
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import logging

logging.basicConfig(level=logging.ERROR)
API_KEY =  os.environ.get("API_KEY")
GPT_MODEL = os.environ.get("GPT_MODEL")
folder_path = os.environ.get("FOLDER_PATH")

if not API_KEY:
    raise ValueError("API_KEY não foi definida.")

if not GPT_MODEL:
    raise ValueError("GPT_MODEL não foi definida.")

if not folder_path:
    raise ValueError("FOLDER_PATH não foi definida.")

def search_pdf_documents(query):

    # Lista para armazenar os documentos carregados
    documents = []

    # Carregar arquivos PDF da pasta especificada
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            try:
                loader = PyMuPDFLoader(file_path)
                documents.extend(loader.load())
            except Exception as e:
                print(f"Erro ao carregar {filename}: {e}")
            
    if not documents:
        raise ValueError("Nenhum documento válido foi carregado.")

    # Criar embeddings e indexar os documentos
    embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
    vector_store = Chroma.from_documents(documents, embeddings)
    retriever = vector_store.as_retriever()
    llm = ChatOpenAI(model=GPT_MODEL, openai_api_key=API_KEY)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

    # Obter resposta para a consulta
    objective_prompt = (
        f"Você é um assistente que analisa documentos PDF. Para cada pergunta, siga as instruções abaixo:\n\n"
        f"- Responda diretamente à pergunta do usuário.\n"
        f"- Liste os PDFs relevantes onde a informação foi encontrada.\n"
        f"- Inclua referências específicas como seções ou páginas, se possível.\n"
        f"- Se não encontrar a resposta, informe claramente que a informação não está nos PDFs analisados.\n\n"
        f"Pergunta: {query}"
    )

    result = qa_chain({"query": objective_prompt}) 

    if result['source_documents']:
        pdfs_found = set([doc.metadata['source'] for doc in result['source_documents']])
        return {
            "found": True,
            "answer": result['result'],
            "pdfs": list(pdfs_found)
        }
    else:
        return {
            "found": False,
            "answer": "Não foi possível encontrar informações relacionadas à sua consulta nos PDFs analisados.",
            "pdfs": []
        }

if __name__ == "__main__":
    
    # Entrada do usuário para o termo ou pergunta
    query = input("Digite o termo ou pergunta a ser pesquisado nos PDFs: ")

    # Realizar a busca e exibir o resultado
    try:
        result = search_pdf_documents(query)
        
        # Exibir a resposta
        if result['found']:
            print("\nResposta:", result['answer'])
            print("PDFs relevantes encontrados:")
            for pdf in result['pdfs']:
                print(f"- {pdf}")
        else:
            print("\nResposta:", result['answer'])
            print("Nenhum PDF relevante foi encontrado.")
    except Exception as e:
        print("Ocorreu um erro:", str(e))
