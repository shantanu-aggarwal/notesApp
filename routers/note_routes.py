#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 05:50:48 2024

@author: shantanuaggarwal
"""


from fastapi import APIRouter
from notesApp.schemas.note import Note
from notesApp.service import noteService
from notesApp.models.appConstants import Status

router = APIRouter()

@router.get("/notes/")
async def getNotes( user_id:str ):
    notes, status = noteService.fetchNotes( user_id )
    if status == Status.ERROR:
        return { "error": "Error occured while fetching notes " }
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == status.SUCCESS:
        return { "notes": notes }
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}
    

@router.post("/notes/create")
async def createNote( user_id:str, note:Note ): # user id to get user level apis
    note_id, status = noteService.createNote( note, user_id )
    
    if status == Status.ERROR:
        return { "error": "Error occured while creating a new note" }
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == status.SUCCESS:
        return { "note_id": note_id }
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}
    

@router.post("notes/delete")
async def deleteNote( note_id:str, user_id:str ):# user id to get user level apis
    status = noteService.deleteNote( note_id, user_id)
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
    
    
    

@router.post("notes/update")
async def updateNote( user_id:str, note_id:str, note:Note ):# user id to get user level apis
    
    note, status = noteService.updateNote( note_id, user_id )
    if status == Status.ERROR:
        return { "error" : "Error occured while checking note access"}
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == Status.INVALID_OPERATION:
        return { "error" : "User does not have access to note"}
    elif status == Status.SUCCESS:
        return { "note": note, "message" : "note updated." }
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}
    

@router.get("notes/summary")
async def getSummary( note_id:int ):
    summary, status = noteService.generateSummary( note_id )
    return summary

@router.get("notes/action_items")
async def getActionItems( note_id:int ):
    summary, status = noteService.generateSummary( note_id )
    return summary

@router.get("notes/tag/summary")
async def getSummaryByTags( user_id:int, tag:str ):
    return
    
@router.get("notes/czmpletion")
async def getSummaryByTags( title:str, content:str ):
    return
    