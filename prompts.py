class Prompt:

    topic = "computer architecture"


    prompt_system = """ You are assistant that helps users with their questions about uploaded files. Be brief in your answers.
                        Answer ONLY with the facts listed in the list of sources below. If there isn't enough information below, say you don't know. 
                        Do not generate answers that don't use the sources below. If asking a clarifying question to the user would help, ask the question.
                        For tabular information return it as an html table. Do not return markdown format.
                        ALWAYS return a "SOURCES" part in your answer.
                        """



    query_prompt_template = """ A new question asked by the user that needs to be answered by searching in a knowledge base.
                                Generate a search query based on the conversation and the new question. 
                                Do not include cited source filenames and document names e.g info.txt or doc.pdf in the search query terms.
                                Do not include any text inside [] or <<>> in the search query terms.
                                If the question is not in English, translate the question to English before generating the search query.

                                Question:
                                {question}

                                Search query:
    """

    def __init__(self) -> None:
        self.history = []
        self.history.append({"role": "system", "content": self.prompt_system})
    
    def add_message_to_history(self, role, message):
        self.history.append({"role": role, "content": message})

    def get_history(self):
        return self.history
