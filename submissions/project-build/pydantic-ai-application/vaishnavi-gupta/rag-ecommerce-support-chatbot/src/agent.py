from typing import List
from guardrails import Guard
from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError


class SellerReview(BaseModel):
  title: str
  sentiment: str  
  key_points: List[str]



external_data = {'str': 'review', 'key_points': [""]}  

try:
  SellerReview(**external_data)  
except ValidationError as e:
  print(e.errors())
  """
  [
      {
          'title': 'str',
          'sentiment': 'str',
          'msg': 'Input should be a valid integer, unable to parse string as an integer',
          'input': 'not an int',
          'url': 'https://errors.pydantic.dev/2/v/int_parsing',
      },
      {
          'title': 'missing',
          'sentiment': 'str',
          'msg': 'Field required',
          'input': {'id': 'not an int', 'tastes': {}},
          'url': 'https://errors.pydantic.dev/2/v/missing',
      },
  ]
  """