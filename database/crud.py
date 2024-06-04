#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 01:42:54 2024

@author: shantanuaggarwal
"""

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from notesApp.schemas import user, note
from notesApp.models.db_models import User, Note


def get_all_users( db:Session ):
    result =  db.query( User ).all()
    users = []
    for i in result:
        users.append( i.username )
    return users

def get_user_by_user_id( user_id:int, db:Session ):
    return db.query( User ).filter( User.id == user_id ).first()


def get_user_by_email_or_username( username: str, db:Session ):
    a = db.query( User ).filter( or_( User.email == username, User.username == username ) ).first()
    return a

def create_user( user:user.User, db:Session, role:str = "user" ):
    hashed_password = user.password + "dummyHashing"
    db_user = User( username= user.username, email= user.email, hashed_password= hashed_password, role= role )
    db.add( db_user )
    db.commit()
    db.refresh( db_user )
    
    return db_user

def get_notes_for_user_id( user_id:int, db:Session ):
    return db.query( Note ).filter( Note.user_id == user_id ).all()

def get_notes_by_tag_and_user_id( user_id:int , tag:str, db:Session ):
    return db.query( Note ).filter( and_( Note.user_id == user_id, Note.tags.like(f"%{tag}%") ) ).all()
def create_note( user_id:int, note:note.Note, tags:list , db:Session ):
    db_note = Note( title= note.title, content= note.content, 
                             user_id= user_id, tags = ",".join( tags ).lower() )
    db.add( db_note )
    db.commit()
    db.refresh( db_note )
    return db_note.id

def get_note_by_note_id( note_id:int, db:Session ):
    return db.query( Note ).filter( Note.id == note_id ).first()

def delete_note( note:Note , db:Session ):
    db.delete( note )
    db.commit()
    return True
    
def update_note( db_note:Note, note:Note, tags, db:Session ):
    db_note.title = note.title
    db_note.content = note.content
    db_note.tags = ",".join( tags ).lower()
    db.commit()
    return True
    
        
    