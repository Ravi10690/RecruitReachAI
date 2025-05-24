"""
Language Model Service for RecruitReach2.

This module provides a service for interacting with language models.
"""

import os
from typing import Any, Optional, Type, TypeVar, Dict

from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from pydantic import BaseModel

from Recruiter.utils.config.config_manager import ConfigManager

T = TypeVar('T', bound=BaseModel)


class LLMService:
    """
    Service for interacting with language models.
    
    This class provides methods for initializing and using language models
    for various tasks such as generating text and extracting information.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-4.1-mini",
        temperature: float = 0.2,
        api_key: Optional[str] = None
    ):
        """
        Initialize the language model service.
        
        Args:
            model_name: Name of the language model to use.
            temperature: Temperature parameter for text generation.
            api_key: OpenAI API key. If not provided, will try to get from config.
        """
        self.model_name = model_name
        self.temperature = temperature
        
        # Get API key from config if not provided
        if api_key is None:
            config_manager = ConfigManager()
            api_key = config_manager.get_value("openai", "OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API key not provided and not found in config")
        
        # Initialize the language model
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
    
    def generate_text(self, prompt: str) -> str:
        """
        Generate text using the language model.
        
        Args:
            prompt: Prompt for text generation.
            
        Returns:
            Generated text.
        """
        # Create a simple chat template with the prompt as a human message
        chat_prompt = ChatPromptTemplate([
            ("human", prompt)
        ])
        
        # Create chain and invoke
        chain = chat_prompt | self.llm
        response = chain.invoke({})
        return response.content
    
    def generate_with_template(
        self,
        template: str,
        input_variables: Dict[str, Any],
        output_schema: Optional[Type[T]] = None
    ) -> Any:
        """
        Generate text using a template and input variables.
        
        Args:
            template: Template for text generation.
            input_variables: Input variables for the template.
            output_schema: Optional Pydantic model for structured output.
            
        Returns:
            Generated text or structured output.
        """
        # Create prompt template with system and human messages
        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(template),
            HumanMessagePromptTemplate.from_template("Please generate the content based on the above instructions.")
        ])
        
        # Create chain with or without structured output
        if output_schema:
            chain = chat_prompt | self.llm.with_structured_output(output_schema)
        else:
            chain = chat_prompt | self.llm
        
        # Invoke the chain with input variables
        return chain.invoke(input_variables)
