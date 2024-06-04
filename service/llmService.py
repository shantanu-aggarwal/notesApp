#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:26:31 2024

@author: shantanuaggarwal
"""
import logging
import traceback

from langchain_community.tools import Tool, DuckDuckGoSearchRun, ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import initialize_agent, AgentType

from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain.chains import StuffDocumentsChain,RefineDocumentsChain, LLMChain
from langchain.chains.summarize import load_summarize_chain

from notesApp.models import db_models
from notesApp.schemas.note import SaveNote
from notesApp.models.appConstants import Status


def getSummary( title:str, content:str):
    status = Status.ERROR
    if not content or content == "":
        return "", Status.SUCCESS
    text = f"Title : {title}\n\n" if title else ""
    text += f"Content: {content}"
    template = """Write a concise summary of the following note:
        
        

    "{text}"


    CONCISE SUMMARY:"""
    prompt = PromptTemplate.from_template( template )
    docs = [ Document( page_content = text ) ]
    
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    chain = load_summarize_chain(llm, chain_type="stuff", **{"prompt" : prompt})
    
    
    summary = None
    try:
        summary = chain.invoke( docs )[ "output_text" ]
        status = Status.SUCCESS
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR
    
        
    
    return summary, status

def getTagSummary( tag:str,  notes:db_models.Note ):
    docs = []
    status = Status.ERROR
    if len(notes)==0 or len(tag) == 0:
        return "", Status.SUCCESS
    for note in notes:
        
        context = f"Title : {note.title}\n\n" if note.title else ""
        context += f"Content: {note.content}"
        docs.append( Document( page_content = context ) )
    
    
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    template = f"Write a concise summary of the following note that emphasizes on {tag} tags:" +\
    """

    "{context}"


    SUMMARY:"""
    prompt = PromptTemplate( template= template, input_variables= ["context"] )
    initial_llm_chain = LLMChain(llm= llm, prompt= prompt)
    initial_response_name = "prev_response"
    
    prompt_refine = PromptTemplate.from_template(
    "Summary from previous notes: {prev_response}. "
    f"Add to summary from following note with emphasizes on {tag} tags:"
    "Note :{context}"
    )
    refine_llm_chain = LLMChain(llm=llm, prompt=prompt_refine)

    document_prompt = PromptTemplate(
    input_variables=["page_content"],
     template="{page_content}"
     )
    document_variable_name = "context"
    
    chain = RefineDocumentsChain(
    initial_llm_chain=initial_llm_chain,
    refine_llm_chain=refine_llm_chain,
    document_prompt=document_prompt,
    document_variable_name=document_variable_name,
    initial_response_name=initial_response_name,
    )
    
    summary = None
    try:
        summary = chain.invoke( docs )[ "output_text" ]
        status = Status.SUCCESS
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR
        
    return summary, status

def generateTag( note: SaveNote ):
    status = Status.ERROR
    if not note.content or len(note.content)==0:
        return [], Status.SUCCESS
    
    context = f"Title : {note.title}\n\n" if note.title else ""
    context += f"Content: {note.content}"
    template ="""From the following note, please extract up to 4 tags:
    
    Context:
    {context}
    
    Tags are keywords or phrases that categorize or summarize the content of the note. 
    They often represent important topics, themes, or subjects mentioned in the text. 
    Please identify up to 4 tags that best represent the content of the note, 
    ensuring they are relevant and succinct.Generate comma(,) seperated list"""
    
    prompt = PromptTemplate( template= template, input_variables = ["context"])
   
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    docs = [ Document( page_content = context ) ]
    document_prompt = PromptTemplate(
    input_variables=["page_content"],
     template="{page_content}"
     )
    document_variable_name = "context"
    
    chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_prompt=document_prompt,
    document_variable_name=document_variable_name
    )
    
    tags = None
    try:
        tags = chain.invoke( docs )
        tags = tags[ "output_text" ].split(',')
        status = Status.SUCCESS
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR
    
    return tags, status


def getActionItems( title:str, content:str ):
    status = Status.ERROR

    if not content or content == "":
        return "", Status.SUCCESS
    context = f"Title : {title}\n\n" if title else ""
    context += f"Content: {content}"
    
    template = """From the following note, please identify any action items if they are mentioned:
    
    note:
    {context}
    
    Action items are tasks, responsibilities, or commitments that need to be completed or followed up on. 
    They typically start with action-oriented verbs such as 'complete,' 'send,' 'follow up,' etc. 
    If there are any action items mentioned in the note, please list them along with any relevant context or details provided. 
    If no action items are present, simply indicate that none were found."""
    
    prompt = PromptTemplate( template= template, input_variables = ["context"])
    
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    docs = [ Document( page_content = context ) ]
    document_prompt = PromptTemplate(
    input_variables=["page_content"],
     template="{page_content}"
     )
    document_variable_name = "context"
    
    chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_prompt=document_prompt,
    document_variable_name=document_variable_name
    )
    
    
    actionItems = None
    try:
        actionItems = chain.invoke( docs )[ "output_text" ]
        status = Status.SUCCESS
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR
    
    return actionItems, status

def getCompletion( title:str, content:str ):
    note = None
    status = Status.ERROR
    
    llm = ChatOpenAI(temperature=0)
    agent = initialize_agent(get_llm_tools( llm ) , llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=False, return_intermediate_steps=True)
    
    prompt = "Write an essay in 1000 words for the topic {input}, use the tools to retrieve the necessary information"  
    
    input = f"Title: {title} \n\n  content: {content}"
      
    try: 
        note = agent.invoke(prompt.format(input=input) )['intermediate_steps'][0][1]
        print(note)
        
        status = Status.SUCCESS
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR       
    return note, status
    
def get_llm_tools( llm ):
    prompt_template = "Complete the essay for the title provided ( use the content as startingg of the note )by the user with the help of following content: {content}"  
    essay = LLMChain(  
        llm=llm,  
        prompt=PromptTemplate.from_template(prompt_template)  
    )
    
    search = DuckDuckGoSearchRun()
    arxiv = ArxivQueryRun()
    wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    
    Tool.from_function(  
     func=essay.run,  
     name="Essay",  
     description="useful when you need to write an essay"  
    )
    
    tools = [  
        Tool(  
         name="Search",  
         func=search.run,  
         description="useful for when you need to answer questions about current events."  
     ),  
     Tool(  
         name="Arxiv",  
         func=arxiv.run,  
         description="useful when you need an answer about encyclopedic general knowledge"  
     ),  
     Tool(  
         name="Wikipedia",  
         func=wiki.run,  
         description="useful when you need an answer about encyclopedic general knowledge"  
     ),  
     Tool.from_function(  
         func=essay.run,  
         name="Essay",  
         description="useful when you need to write an essay"  
     ),
    ]
    return tools