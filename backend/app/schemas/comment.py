from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class CommentCreate(BaseModel):
    video_id: int
    text: str | None = None
    video_url: str | None = None
    timestamp: int | None = None
    parent_comment_id: int | None = None

    @model_validator(mode="after")
    def validate_comment(self):
        if self.text is None and self.video_url is None:
            raise ValueError("Comment must contain text or video_url")

        if self.text is not None and not self.text.strip():
            raise ValueError("Comment text cannot be empty")

        return self


class CommentResponse(BaseModel):
    id: int
    user_id: int
    video_id: int
    text: str | None
    video_url: str | None
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
    text: str | None = None
    video_url: str | None = None
    timestamp: int | None = None

    @model_validator(mode="after")
    def validate_reply(self):
        if self.text is None and self.video_url is None:
            raise ValueError("Reply must contain text or video_url")

        if self.text is not None and not self.text.strip():
            raise ValueError("Reply text cannot be empty")

        return self


class CommentTreeResponse(CommentResponse):
    replies: list["CommentTreeResponse"] = []
