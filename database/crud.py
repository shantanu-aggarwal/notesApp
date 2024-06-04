#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 01:42:54 2024

@author: shantanuaggarwal
"""

from sqlalchemy import or_
from sqlalchemy.orm import Session

from notesApp.schemas.user import User
from notesApp.schemas.note import Note
from notesApp.models import db_models


def get_all_users( db:Session ):
    result =  db.query( db_models.User ).all()
    users = []
    for i in result:
        users.append( i.username )
    return users

def get_user_by_user_id( user_id:int, db:Session ):
    return db.query( db_models.User ).filter( db_models.User.id == user_id ).first()


def get_user_by_email_or_username( username: str, db:Session ):
    a = db.query( db_models.User) .filter( or_( db_models.User.email == username, db_models.User.username == username ) ).first()
    return a

def create_user( user:User, db:Session ):
    hashed_password = user.password + "dummyHashing"
    db_user = db_models.User( username= user.username, email= user.email, hashed_password= hashed_password, role= user.role )
    db.add( db_user )
    db.commit()
    db.refresh( db_user )
    
    return db_user

def get_notes_for_user_id( user_id:int, db:Session ):
    return db.query( db_models.Note ).filter( db_models.Note.user_id == user_id ).all()

def create_note( user_id:int, note:Note, db:Session ):
    db_note = db_models.Note( title= note.title, content= note.content, user_id= user_id )
    db.add( db_note )
    db.commit()
    db.refresh( db_note )
    return db_note.id

def get_note_by_note_id( note_id:int, db:Session ):
    return db.query( db_models.Note ).filter( db_models.Note.id == note_id ).first()

def delete_note( note:db_models.Note , db:Session ):
    db.delete( note )
    db.commit()
    return True
    
def update_note( db_note:db_models.Note, note:Note, db:Session ):
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    return True
    
        
    