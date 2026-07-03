import sys
import os
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, ContextualPrecisionMetric
from deepeval.models.base_model import DeepEvalBaseLLM
from groq import Groq

