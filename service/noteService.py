#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 11:19:00 2024

@author: shantanuaggarwal
"""
import logging
import traceback

from notesApp.database import crud
from notesApp.schemas.note import Note, SaveNote
from notesApp.service import userService, llmService
from notesApp.database.init import SessionLocal
from notesApp.models import db_models
from notesApp.models.appConstants import Status, Roles


def checkUserAcces( user_id:int, note:db_models.Note ):
    if note:
        if note.user_id == user_id:
            return Status.SUCCESS
        else:
            status = userService.checkRole( user_id, Roles.ADMIN)
            return status
    else:
        return Status.INVALID_OPERATION
    
def fetchNotes( user_id:int ):
    db = SessionLocal()
    status = Status.ERROR
    notes = []
    try:
        db_notes = crud.get_notes_for_user_id( user_id, db )
        print(db_notes[0])
        for i in db_notes:
            notes.append( Note( id= i.id, title= i.title, content= i.content, tags= i.tags.split(',') ))
        status = Status.SUCCESS
    except:
        logging.error(traceback.format_exc())
    finally:
        db.close()
    
    return notes, status



def  getNote( user_id:int, note_id:int ):
    db = SessionLocal()
    status = Status.ERROR
    note = None
    try:
        db_note = crud.get_note_by_note_id( note_id, db )
        status = checkUserAcces(user_id, db_note)
        
        if status == Status.SUCCESS and db_note:
            note = Note( id= db_note.id, title= db_note.title, 
                        content= db_note.content, tags= db_note.tags.split(',') )
            
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR
    finally:
        db.close()
        
    return note, status

def createNote( user_id:int, note:SaveNote ):
    db = SessionLocal()
    status = Status.ERROR
    response = None
    try:
        if crud.get_user_by_user_id( user_id, db ):
            tags, status = llmService.generateTag( note )
            response = crud.create_note( user_id, note, tags, db )
            status = Status.SUCCESS
        else:
            status = Status.USER_UNDEFINED
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR
    finally:
        db.close()
    
    return response, status
        

def deleteNote( user_id:int, note_id:int ):
    db = SessionLocal()
    status = Status.ERROR
    
    try:
        note = crud.get_note_by_note_id( note_id, db )
        # if note exists delete if user_id is the owner of note or has admin rights
        status = checkUserAcces(user_id, note)
        
        if status == Status.SUCCESS:
            crud.delete_note( note, db )
            
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR
    finally:
        db.close()
        
    return status

def updateNote( user_id:int, note_id:int, note:SaveNote ):
    db = SessionLocal()
    status = Status.ERROR
    
    try: 
        old_note = crud.get_note_by_note_id( note_id, db )
        status = checkUserAcces(user_id, old_note)
        
        if status == Status.SUCCESS:
            tags, status = llmService.generateTag( note )
            crud.update_note( old_note, note, tags, db)
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR
    finally:
        db.close()
        
    return status
    
def getNoteSummary( user_id:int, note_id:int ):
    db = SessionLocal()
    status = Status.ERROR
    summary = ""
    try: 
        note = crud.get_note_by_note_id( note_id, db )
        status = checkUserAcces(user_id, note)
        
        if status == Status.SUCCESS:
            summary, status = llmService.getSummary( note.title, note.content)
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR
    finally:
        db.close()
        
    return summary, status
    

def getSummaryForTag( user_id:int, tag:str ):
    db = SessionLocal()
    status = Status.ERROR
    summary = ""
    if len(tag) == 0:
        return "", Status.SUCCESS
    
    try:
        notes = crud.get_notes_by_tag_and_user_id( user_id, tag, db)
    
        if len(notes)==0:
            return "No notes found with provided tags". Status.SUCCESS
        
        summary, status = llmService.getTagSummary( tag, notes )
        
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR
    finally:
        db.close()
    
    return summary, status

    

def getActionItems( user_id:int, note_id: int ):
    db = SessionLocal()
    status = Status.ERROR
    actionItems = ""
    try: 
        db_note = crud.get_note_by_note_id( note_id, db )
        status = checkUserAcces(user_id, db_note)
        
        if status == Status.SUCCESS:
            actionItems, status = llmService.getActionItems( db_note.title, db_note.content )
    except:
        logging.error( traceback.format_exc() )
        status = Status.ERROR
    finally:
        db.close()
    
    return actionItems, status
    
    