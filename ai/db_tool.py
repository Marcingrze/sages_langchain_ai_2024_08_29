from dotenv import load_dotenv

load_dotenv()

import os
from ai import DB_DESCRIPTION, COLUMN_NAME_MAPPING
import pandas as pd
import sqlite3

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate


from typing_extensions import TypedDict

class WorkflowState(TypedDict):
    question: str
    plan: str
    can_answer: bool
    sql_query: str
    sql_result: str
    answer: str

class DBTool:
    def __init__(self):
        self.__model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")

        df = pd.read_csv("telco.csv")
        df = df.rename(columns=COLUMN_NAME_MAPPING)

        con = sqlite3.connect("customers.db")
        df.to_sql("customers", con, index=False, if_exists="replace")
        con.close()

        workflow = StateGraph(WorkflowState)

        workflow.add_node("check_if_can_answer_question", self.__check_if_can_answer_question)
        workflow.add_node("write_query", self.__write_query)
        workflow.add_node("execute_query", self.__execute_query)
        workflow.add_node("write_answer", self.__write_answer)
        workflow.add_node("explain_no_answer", self.__explain_no_answer)

        workflow.set_entry_point("check_if_can_answer_question")

        workflow.add_conditional_edges("check_if_can_answer_question", self.check_if_can_answer, {
            True: "write_query",
            False: "explain_no_answer"
        })

        workflow.add_edge("write_query", "execute_query")
        workflow.add_edge("execute_query", "write_answer")

        workflow.add_edge("explain_no_answer", END)
        workflow.add_edge("write_answer", END)

        self.__app = workflow.compile()

    def __call__(self, question):
        inputs = {"question": question}
        result = self.__app.invoke(inputs)
        return result["answer"]

    def __check_if_can_answer_question(self, state):
        can_answer_prompt = PromptTemplate(template="""You are a database reading bot that can answer users' questions using information from a database. \n

    {data_description} \n\n

    Given the user's question, decide whether the question can be answered using the information in the database. \n\n

    Return a JSON with two keys, 'reasoning' and 'can_answer', and no preamble or explanation.
    Return one of the following JSON:

    Examples:
    {{"reasoning": "I can filter the data by the 'Senior Citizen' column where the value is 'Yes' and count the number of rows.", "can_answer": true}}
    {{"reasoning": "I can group the data by the 'State' column and count the number of customers in each state to find the highest.", "can_answer": true}}
    {{"reasoning": "I can filter the data by the 'Contract' column for 'Month-to-Month', then calculate the percentage using the 'Churn Value' column.", "can_answer": true}}
    {{"reasoning": "The data description provides information about reasons for leaving (Churn Reason), but does not include reasons for joining.", "can_answer": false}}
    {{"reasoning": "The data description does not include information about upgrades or changes to service plans over time.", "can_answer": false}}
    {{"reasoning": "The data provides latitude and longitude, but not the location of the company headquarters, which is needed to calculate the distance.", "can_answer": false}}

    Question: {question} \n
    """,
    input_variables=["data_description", "question"]
)

        can_answer_chain = can_answer_prompt | self.__model  | JsonOutputParser()

        result = can_answer_chain.invoke({"question": state["question"], "data_description": DB_DESCRIPTION})

        return {"plan": result["reasoning"], "can_answer": result["can_answer"]}

    def __write_query(self, state):
        write_query_prompt = PromptTemplate(
        template="""You are a database reading bot that can answer users' questions using information from a database. \n

        {data_description} \n\n

        In the previous step, you have prepared the following plan: {plan}

        Return an SQL query with no preamble or explanation. Don't include any markdown characters or quotation marks around the query.

        Question: {question} \n""",
        input_variables=["data_description", "question", "plan"],
    )

        write_query_chain = write_query_prompt | self.__model | StrOutputParser()

        result = write_query_chain.invoke({
            "data_description": DB_DESCRIPTION,
            "question": state["question"],
            "plan": state["plan"]
        })

        return {"sql_query": result}

    def __run_query(self, sql_query):
        con = sqlite3.connect("customers.db")
        try:
            response = pd.read_sql_query(sql_query, con)
            return response.to_markdown()
        except Exception as e:
            return str(e)
        finally:
            con.close()

    def __execute_query(self, state):
        query = state["sql_query"]

        try:
            return {"sql_result": self.__run_query(query)}
        except Exception as e:
            return {"sql_result": str(e)}

    def __write_answer(self, state):
        write_answer_prompt = PromptTemplate(
        template="""You are a database reading bot that can answer users' questions using information from a database. \n

        In the previous step, you have planned the query as follows: {plan},
        generated the query {sql_query}
        and retrieved the following data:
        {sql_result}

        Return a text answering the user's question using the provided data.

        Question: {question} \n""",
        input_variables=["question", "plan", "sql_query", "sql_result"],
        )

        write_answer_chain = write_answer_prompt | self.__model | StrOutputParser()

        result = write_answer_chain.invoke({
            "question": state["question"],
            "plan": state["plan"],
            "sql_query": state["sql_query"],
            "sql_result": state["sql_result"]
        })

        return {"answer": result}

    def __explain_no_answer(self, state):
        cannot_answer_prompt = PromptTemplate(
            template="""You are a database reading bot that can answer users' questions using information from a database. \n

            You cannot answer the user's questions because of the following problem: {problem}.

            Explain the issue to the user and apologize for the inconvenience.

            Question: {question} \n""",
            input_variables=["question", "problem"],
        )

        cannot_answer_chain = cannot_answer_prompt | self.__model | StrOutputParser()

        result = cannot_answer_chain.invoke({
            "question": state["question"],
            "problem": state["plan"]
        })

        return {"answer": result}

    def check_if_can_answer(self, state):
        return state["can_answer"]
