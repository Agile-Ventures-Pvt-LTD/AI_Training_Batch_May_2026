from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Tuple
from guardrails import Guard
from guardrails.hub import ProfanityFree
from guardrails.hub import ToxicLanguage


logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",)
logger = logging.getLogger(__name__)
INPUT_BLOCK_MESSAGE = ("Your request violates the platform's ""safety guidelines and cannot be processed.")
OUTPUT_BLOCK_MESSAGE = ("The generated response did not pass ""safety validation and was blocked.")
@dataclass
class ValidationResult:
    is_valid: bool
    message: str

class SafetyGuardrails:
    """
    Input and Output Moderation Layer.
    """

    def __init__(self) -> None:

        # Input validation chain
        self.input_guard = Guard().use(
            ProfanityFree()
        ).use(
            ToxicLanguage(
                threshold=0.5
            )
        )

        # Output validation chain
        self.output_guard = Guard().use(
            ProfanityFree()
        ).use(
            ToxicLanguage(
                threshold=0.5
            )
        )

    def validate_input(self,user_query: str,) -> ValidationResult:
        """
        Validate user input before retrieval or LLM.
        """
        try:
            logger.info("Running input guardrails...")

            self.input_guard.validate(user_query)
            return ValidationResult(is_valid=True,message=user_query,)
        except Exception as ex:
            logger.warning("Input validation failed: %s",ex,)
            return ValidationResult(is_valid=False,message=INPUT_BLOCK_MESSAGE,)
    def validate_output(self,response: str) -> ValidationResult:
        """
        Validate generated answer.
        """
        try:
            logger.info("Running output guardrails..." )
            self.output_guard.validate(response)
            return ValidationResult(is_valid=True,message=response,)
        except Exception as ex:
            logger.warning("Output validation failed: %s",ex,)

            return ValidationResult(
                is_valid=False,
                message=OUTPUT_BLOCK_MESSAGE,
            )

   

    def validate_request(
        self,
        user_query: str,
    ) -> Tuple[bool, str]:
        """
        Validate incoming query.
        """

        result = self.validate_input(
            user_query
        )

        return (
            result.is_valid,
            result.message,
        )

    def validate_response(
        self,
        response: str,
    ) -> Tuple[bool, str]:
        """
        Validate outgoing response.
        """

        result = self.validate_output(
            response
        )

        return (
            result.is_valid,
            result.message,
        )



guardrails = SafetyGuardrails()


def check_input(
    user_query: str,
) -> Tuple[bool, str]:
    """
    Validate user query.
    """

    return guardrails.validate_request(
        user_query
    )


def check_output(
    response: str,
) -> Tuple[bool, str]:
    """
    Validate generated output.
    """

    return guardrails.validate_response(
        response
    )


if __name__ == "__main__":

    sample_query = (
        "How can I improve seller ratings?"
    )

    valid, message = check_input(
        sample_query
    )

    print("Input Valid:", valid)
    print("Message:", message)

    sample_response = (
        "You can improve ratings by improving "
        "shipping speed and customer service."
    )

    valid, message = check_output(
        sample_response
    )

    print("Output Valid:", valid)
    print("Message:", message)