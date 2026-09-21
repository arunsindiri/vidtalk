from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class CommentCreate(BaseModel):
    video_id: int
    text: str = Field(min_length=1)
    timestamp: int | None = None
    parent_comment_id: int | None = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str):
        if not value.strip():
            raise ValueError("Comment text cannot be empty")
        return value


class CommentResponse(BaseModel):
    id: int
    user_id: int
    video_id: int
    text: str
    timestamp: int | None
    parent_comment_id: int | None
    created_at: datetime


class CommentUpdate(BaseModel):
    text: str = Field(min_length=1)
    timestamp: int | None = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str):
        if not value.strip():
            raise ValueError("Comment text cannot be empty")
        return value


class CommentDelete(BaseModel):
    pass


class ReplyCreate(BaseModel):
    text: str = Field(min_length=1)
    timestamp: int | None = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str):
        if not value.strip():
            raise ValueError("Reply text cannot be empty")
        return value


class CommentTreeResponse(CommentResponse):
    replies: list["CommentTreeResponse"] = []
