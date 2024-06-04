#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 05:36:27 2024

@author: shantanuaggarwal
"""

from fastapi import APIRouter

from notesApp.service import userService
from notesApp.schemas.user import User, UserLogin
from notesApp.models.appConstants import Roles, Status





router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get('/')
async def get( user_id:int ):
    users, status = userService.getAll( user_id )
    if status == Status.ERROR:
        return { "error" : "Error occured while checking note access"}
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User not found" }
    elif status == Status.INVALID_OPERATION:
        return { "error" : "User does not have access to view user list"}
    elif status == Status.SUCCESS:
        return { "users" : users }
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}


@router.post('/create')
async def create( user : User ):
    response, status = userService.createUser(user )
    if status == Status.ERROR:
        return { "error" : "Error occured while checking note access"}
    elif status == Status.SUCCESS:
        return response
    elif status == Status.INVALID_OPERATION:
        return response
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}

@router.post('/login')
async def login( userLogin : UserLogin ):
    user, status = userService.validateUser( userLogin.username, userLogin.password )
    if status == Status.ERROR:
        return { "error" : "Error occured while checking note access"}
    elif status == Status.INVALID_OPERATION:
        return { "error" : "Password is incorrect."}
    elif status == Status.SUCCESS:
        return { "message" : "User Logged In.", "user_id": user}
    elif status == Status.USER_UNDEFINED:
        return { "error" : "User does not exists."}
    else:
        return { "error" : "Internal Server Error. Unhandled error occured."}

@router.post('/logout')
async def logout( username : str):
    return { "message" : "User Logged Out."}