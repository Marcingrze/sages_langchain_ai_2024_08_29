# Instrukcja dla uczestników

W czasie szkolenia będziemy korzystać z Jupyter Notebook oraz lokalnie uruchomionej aplikacji napisanej w Pythonie z użyciem Flask i Streamlit.

W Jupyter Notebooku potrzebujemy następujące zależności: `openai langchain langchain-openai langserve[all] chromadb langchain-chroma langchain-community langgraph`. Proponuję używać Google Colab lub Kaggle.

W przypadku Streamlit i Flask należy zainstalować:

```
openai==1.30.3
Flask==3.0.0
Flask-Cors==4.0.0
langchain==0.2.1
langchainhub==0.1.14
langchain-openai==0.1.7
langchain-community==0.2.1
chromadb==0.5.0
langchain-chroma==0.1.1
langgraph==0.0.60
streamlit==1.35.0
tabulate==0.9.0
streamlit-mic-recorder==0.0.8
```

**W celu sprawdzenia czy Streamlit działa lokalnie, proszę wykonać kroki z punktu "Create your first app" znajdujące się w dokumentacji Streamlit: https://docs.streamlit.io/get-started/tutorials/create-an-app**

