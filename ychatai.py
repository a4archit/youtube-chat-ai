from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings, AzureOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from typing import Self







class YouTubeVideoChatAI:
    """ Main class """




    def __init__(self, video_id: str, verbose: bool = True) -> Self:
        """ Constructor

        Args:
            video_id (str): YouTube video id
            verbose (bool, optional): Defaults to True.

        Returns:
            Self: Class instance
        """

        ## loading secret keys
        load_dotenv()
        if verbose:
            print("Secret Keys Loaded!")

        ## loading modelsif verbose:
        self.embeddings = self._load_embedding_model()
        if verbose:
            print("Embedding model loaded!")
        
        self.llm = self._load_llm()
        if verbose:
            print("LLM loaded!")

        ## fetching transcript
        try:
            self.transcript = self._fetch_transcript(video_id)
            if verbose:
                print("Transcript fetched!")
        except Exception as e:
            print(f"Error occurring while fetching all transcripts: {e}")

        ## processing retriever
        self.retriever = self._load_retriever(self.transcript, self.embeddings)
        if verbose:
            print("Retriver loaded!")

        ## loading template
        self.template = self._load_template()
        if verbose:
            print("Template loaded!")






    def _fetch_transcript(self, video_id: str):    
        try:
            # If you don’t care which language, this returns the “best” one
            transcripter = YouTubeTranscriptApi()
            transcript_list = transcripter.fetch(video_id, languages=["en"])
            # Flatten it to plain text
            transcript = " ".join(chunk.text for chunk in transcript_list.snippets)

        except TranscriptsDisabled:
            print("No captions available for this video.")
            return None 
        
        return transcript
    






    def _load_embedding_model(self):
        """ load and return embedding model """

        embeddings = AzureOpenAIEmbeddings(
            model="text-embedding-3-small", 
            azure_deployment="text-embedding-3-small"
        )

        return embeddings
    







    def _load_llm(self):
        """ load and return llm """

        ## creating object instance
        llm = GoogleGenerativeAI(
            name = 'apcas 1.0.0',
            model = 'gemini-1.5-flash', 
            verbose = False,
            max_tokens = 1000,
            temperature = 0.3
        )

        return llm








    def _load_retriever(self, transcript: str, embeddings: AzureOpenAIEmbeddings):
        """ process and return retriever """

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.create_documents([transcript])

        vector_store = FAISS.from_documents(chunks, embeddings)

        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

        return retriever
    






    

    def _load_template(self) -> PromptTemplate:
        """ create instance of PromptTemplate and return it """

        template = PromptTemplate(
            template="""
            You are a helpful assistant.
            Answer ONLY from the provided transcript context.
            If the context is insufficient, just say you don't know.
            Try to give straight forward responses.

            {context}
            Question: {question}
            """,
            input_variables = ['context', 'question']
        )

        return template









    def _get_prompt(self, query: str, template: PromptTemplate, retriever) -> PromptTemplate:
        """ It will process user query and return appropriate docs """

        retrieved_docs    = retriever.invoke(query)
        context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
        final_prompt = template.invoke({"context": context_text, "question": query})

        return final_prompt
    








    def invoke(self, query: str):
        """ This function will process query """

        # getting prompt
        prompt = self._get_prompt(query, self.template, self.retriever)

        # getting llm response
        response = self.llm.invoke(prompt)

        return response
    



    def run_on_terminal(self) -> None:
        """ Activate Chat AI feature in your terminal """

        print(f"{'-'*50} YouTube videos chatting AI has been activated! Now you can chat with it! {'-'*50}")

        while True:

            query = input("\n\n\033[33m-----(YOU): \033[0m").lower().strip()
            if query == "":
                continue
            if query in ["exit","bye","bye bye"]:
                print("\n\n\tBye Bye!\n\n")
                break

            response = self.invoke(query)

            # displaying ouptut
            print("\n\n\033[32m-----(AI Response)\033[0m\n\t|")
            for line in response.split('\n'):
                print(f"\t| {line}")
            print("\t|")
    
    






if __name__ == "__main__":


    video_id = "TYEqenKrbaM" # only the ID, not full URL

    yt_chat = YouTubeVideoChatAI(video_id)

    yt_chat.run_on_terminal()



