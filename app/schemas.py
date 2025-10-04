from pydantic import BaseModel


class SummarizeOptions(BaseModel):
    include_sentiment: bool = False


class SummarizeRequest(BaseModel):
    transcript: str
    options: SummarizeOptions = SummarizeOptions()
