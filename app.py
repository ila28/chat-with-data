from dotenv import load_dotenv
import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback


from data_processing import parse_pdf, create_embeddings
from prompts import Prompt


load_dotenv()
# create Prompt instance
if 'prompt' not in st.session_state:
    # Initialize the variable if it doesn't exist in session_state
    st.session_state['prompt'] = Prompt()
# create llm instance
if 'llm' not in st.session_state:
    # Initialize the variable if it doesn't exist in session_state
    st.session_state['llm'] = ChatOpenAI(model_name="gpt-3.5-turbo")
# create qa chain with sources
if 'chain' not in st.session_state:
    # Initialize the variable if it doesn't exist in session_state
    st.session_state['chain'] = load_qa_chain(st.session_state['llm'], chain_type="stuff")

st.set_page_config(page_title="Ask your PDF")
st.header("Ask your PDF 💬")

# upload file
pdf = st.file_uploader("Upload your PDF", type="pdf")


if pdf is not None:
  # extract the text
  text = parse_pdf(pdf)

  # retrieve embeddings  
  knowledge_base = create_embeddings(text)

  # show user input
  user_question = st.text_input("Ask a question about your PDF:")

  if user_question:

    st.session_state['prompt'].add_message_to_history(role="user", message=user_question)
    docs = knowledge_base.similarity_search(user_question)

    with get_openai_callback() as cb:
      with st.spinner(
                    "Generating Answer to your Query : `{}` ".format(user_question)
                ):
                    chain_message = st.session_state['prompt'].get_history()
                    response = st.session_state['chain'].run(input_documents= docs, question= chain_message)
      st.session_state['prompt'].add_message_to_history(role="assistant", message=response)
      print(cb)

    st.info(response, icon="🤖")
    


