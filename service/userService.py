#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 23:29:22 2024

@author: shantanuaggarwal
"""
import re
import logging
import traceback

from notesApp.database import crud
from notesApp.schemas.user import User
from notesApp.database.init import SessionLocal
from notesApp.models.appConstants import Status, Roles


EMAIL_REGEX = r"^[a-zA-Z0-9+_.-]*@[a-z0-9]*(\.[a-z]*)(\.[a-z]*)?"


    
def getAll( user_id:int ):
    db = SessionLocal()
    response = None
    status = Status.ERROR
    try:
        status = checkRole(user_id, Roles.ADMIN)
        if status == Status.SUCCESS:
            users = crud.get_all_users(db)
            response = users
            
    except Exception:
        logging.error(traceback.format_exc())
        status = Status.ERROR
    finally:
        db.close()
    return response, status
        
def checkRole( user_id:int, role:Roles ):
    db = SessionLocal()
    status = Status.ERROR
    try:
        user = crud.get_user_by_user_id( user_id, db )
        if user:
            if user.role == role.value:
                status = Status.SUCCESS
            else:
                status = Status.INVALID_OPERATION
        else:
            status = Status.USER_UNDEFINED
    except Exception:
        logging.error(traceback.format_exc())
    finally:
        db.close()
    return status
    

def createUser( user:User ):
    response= None
    status = Status.ERROR
    if ( not (user.username or user.email) ) or ( len(user.username) == 0 and len(user.email)== 0 ) :
        return { "error" : "Both email and username cannat be null or empty"}, Status.INVALID_OPERATION
    
    if user.email:
        if not re.compile(EMAIL_REGEX):
            return { "error" : "Email not in correct format." }, Status.INVALID_OPERATION
        
    if user.username is None:
        user.username = user.email
    
    db = SessionLocal()
    response = None
    try:
        check = crud.get_user_by_email_or_username( user.username, db )
        if check:
            response = { "error" : "Email or Username already exists." }, Status.INVALID_OPERATION
        else:
            user = crud.create_user( user, db )
            response = { "user_id": user.id }
            status = Status.SUCCESS
    
    except Exception:
        logging.error( traceback.format_exc() )
        logging.error("Errored Occured")
        response = { "error" : "Error occured while creating user" }    
    
    finally:
        db.close()
    
    return response, status
        

def validateUser( username:str, password:str ):
    db = SessionLocal()
    user_id = None
    status = Status.ERROR
    try:
        user = crud.get_user_by_email_or_username( username, db )
        status = Status.SUCCESS
    except:
        logging.error(traceback.format_exc())
    finally:
        db.close()
    
    if user:
        if user.hashed_password == password + "dummyHashing":
            # create session return session id
            user_id = user.id
        else:
            status = Status.INVALID_OPERATION
    elif status == Status.SUCCESS :
        status = Status.USER_UNDEFINED
    
    return user_id, status
    
def logout_user( user_id:int ):
    # terminate session_id
    return 
        
    