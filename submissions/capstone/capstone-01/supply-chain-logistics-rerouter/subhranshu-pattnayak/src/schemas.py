from pydantic import BaseModel


class ManifestTextOutput(BaseModel):
    manifest_text: str