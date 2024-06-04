#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 05:50:48 2024

@author: shantanuaggarwal
"""
import logging
import traceback

from fastapi import APIRouter
from notesApp.schemas.note import SaveNote
from notesApp.service import noteService, llmService
from notesApp.models.appConstants import Status

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def getNotes( user_id:int ):
    notes, status = noteService.fetchNotes( user_id )
    if status == Status.ERROR:
        return { "error": "Error occured while fetching notes " }
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == status.SUCCESS:
        return { "notes": notes }
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}

@router.get("/{note_id}")
async def getNote( user_id:int, note_id:int ):
    note, status = noteService.getNote( user_id, note_id )
    if status == Status.ERROR:
        return { "error": "Error occured while fetching notes " }
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == status.SUCCESS:
        return { "note": note }
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}

@router.post("/create")
async def createNote( user_id:str, note:SaveNote ): # user id to get user level apis
    note_id, status = noteService.createNote( user_id, note, )
    
    if status == Status.ERROR:
        return { "error": "Error occured while creating a new note" }
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == status.SUCCESS:
        return { "note_id": note_id }
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}
    

@router.delete("/delete/{note_id}")
async def deleteNote( note_id:str, user_id:str ):# user id to get user level apis
    status = noteService.deleteNote( note_id, user_id )
    if status == Status.ERROR:
        return { "error" : "Error occured while checking note access"}
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == Status.INVALID_OPERATION:
        return { "error" : "User does not have access to Note or Note does not exists."}
    elif status == Status.SUCCESS:
        return { "message" : "note deleted." }
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}
    
    
        

@router.post("/update/{note_id}")
async def updateNote( note_id:int, note:SaveNote, user_id:int):# user id to get user level apis
    
    status = noteService.updateNote( user_id, note_id, note )
    if status == Status.ERROR:
        return { "error" : "Error occured while checking note access"}
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == Status.INVALID_OPERATION:
        return { "error" : "User does not have access to note"}
    elif status == Status.SUCCESS:
        return { "message" : "note updated." }
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}
    

@router.get("/summary/{note_id}")
async def getSummary( user_id:int, note_id:int ):
    summary, status = noteService.getNoteSummary( user_id, note_id )
    if status == Status.SUCCESS:
        return { "summary" : summary }
    elif status == Status.ERROR:
        return { "error" : "Error occured while checking note access"}
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == Status.INVALID_OPERATION:
        return { "error" : "User does not have access to note"}
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}

@router.get("/action_items/{note_id}")
async def getActionItems( user_id:int, note_id:int ):
    actionItems, status = noteService.getActionItems( user_id, note_id )
    
    if status == Status.SUCCESS:
        return { "actionItems" : actionItems }
    elif status == Status.ERROR:
        return { "error" : "Error occured while checking note access"}
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == Status.INVALID_OPERATION:
        return { "error" : "User does not have access to note"}
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}
    

@router.get("/tag/summary")
async def getSummaryByTag( user_id:int, tag:str ):
    summary, status = noteService.getSummaryForTag( user_id, tag )
    
    if status == Status.SUCCESS:
        return { "summary" : summary }
    elif status == Status.ERROR:
        return { "error" : "Error occured while getting notes"}
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == Status.INVALID_OPERATION:
        return { "error" : "User does not notes with this tag"}
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}
    
@router.get("/completion")
async def noteCompletion( title:str, content:str ):
    completion = None
    try:
        completion, status = llmService.getCompletion( title, content)
        if status == Status.SUCCESS:
            return { "note" : completion }
        else:
            return { "error" : "Internal Server Error. Unhandled error occured."}
    except:
        logging.error( traceback.format_exc() )
        return { "error" : "Internal Server Error. Unhandled error occured."}
        
    
    
    