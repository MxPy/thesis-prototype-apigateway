from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from typing import Optional
from fastapi import UploadFile, Form
from files.utils import form_body

class Post(BaseModel):
    postId: int #backend
    userId: str
    username: str #backend
    title: str
    recordedAt: str #backend
    isVisible: str #backend
    tag: List[str]
    voteCount: int
    imageLink: Optional[str] = None
    description: Optional[str] = None
    
class PostOuterRequest(BaseModel):
    userId: str = Form(...)
    title: str = Form(...)
    tag: List[str] = Form(...)
    image: Optional[UploadFile] = Form(None)
    description: Optional[str] = Form(None)
    
class PostInerRequest(BaseModel):
    userId: str
    title: str
    tag: List[str]
    imageLink: Optional[str] = None
    description: Optional[str] = None
    