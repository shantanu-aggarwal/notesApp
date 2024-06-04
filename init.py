#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 14:59:39 2024

@author: shantanuaggarwal
"""
import os
import logging
import traceback

from notesApp.database import crud
from notesApp.schemas import user
from notesApp.models import db_models, appConstants
from notesApp.database.init import engine, SessionLocal

def init():
    
    OPENAI_API_KEY = "<open_api_key>"
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    db_models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not crud.get_user_by_email_or_username( "admin", db ):
            _user = user.User( 
                              username = "admin",
                              email     = "default@default.com",
                              password  = "admin" ,
                              role      = appConstants.Roles.ADMIN.value
                              )
            crud.create_user( _user, db, role = appConstants.Roles.ADMIN.value )
    except:
        logging.error( traceback.format_exc() )
        logging.error( "Admin user not created" )