"""
Tests for the LLM service.

This module contains tests for the LLM service.
"""

import unittest
from unittest.mock import patch, MagicMock

from Recruiter.services.llm.llm_service import LLMService


class TestLLMService(unittest.TestCase):
    """Tests for the LLMService class."""
    
    @patch('RecruitReach2.services.llm.llm_service.ChatOpenAI')
    @patch('RecruitReach2.services.llm.llm_service.ConfigManager')
    def test_init_with_api_key(self, mock_config_manager, mock_chat_openai):
        """Test initializing LLMService with an API key."""
        # Arrange
        api_key = "test_api_key"
        model_name = "gpt-4o-mini"
        temperature = 0.2
        
        # Mock the ChatOpenAI instance
        mock_llm = MagicMock()
        mock_chat_openai.return_value = mock_llm
        
        # Act
        llm_service = LLMService(
            model_name=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        # Assert
        mock_chat_openai.assert_called_once_with(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        self.assertEqual(llm_service.llm, mock_llm)
        self.assertEqual(llm_service.model_name, model_name)
        self.assertEqual(llm_service.temperature, temperature)
        
        # Verify that ConfigManager was not called
        mock_config_manager.assert_not_called()
    
    @patch('RecruitReach2.services.llm.llm_service.ChatOpenAI')
    @patch('RecruitReach2.services.llm.llm_service.ConfigManager')
    def test_init_without_api_key(self, mock_config_manager, mock_chat_openai):
        """Test initializing LLMService without an API key."""
        # Arrange
        config_api_key = "config_api_key"
        model_name = "gpt-4o-mini"
        temperature = 0.2
        
        # Mock the ConfigManager instance
        mock_config = MagicMock()
        mock_config_manager.return_value = mock_config
        mock_config.get_value.return_value = config_api_key
        
        # Mock the ChatOpenAI instance
        mock_llm = MagicMock()
        mock_chat_openai.return_value = mock_llm
        
        # Act
        llm_service = LLMService(
            model_name=model_name,
            temperature=temperature
        )
        
        # Assert
        mock_config_manager.assert_called_once()
        mock_config.get_value.assert_called_once_with("openai", "OPENAI_API_KEY")
        mock_chat_openai.assert_called_once_with(
            model=model_name,
            temperature=temperature,
            api_key=config_api_key
        )
        self.assertEqual(llm_service.llm, mock_llm)
    
    @patch('RecruitReach2.services.llm.llm_service.ChatOpenAI')
    @patch('RecruitReach2.services.llm.llm_service.ConfigManager')
    def test_generate_text(self, mock_config_manager, mock_chat_openai):
        """Test generating text with LLMService."""
        # Arrange
        api_key = "test_api_key"
        prompt = "Test prompt"
        expected_response = "Generated text"
        
        # Mock the ChatOpenAI instance
        mock_llm = MagicMock()
        mock_chat_openai.return_value = mock_llm
        
        # Mock the response from the LLM
        mock_response = MagicMock()
        mock_response.content = expected_response
        mock_llm.invoke.return_value = mock_response
        
        # Act
        llm_service = LLMService(api_key=api_key)
        result = llm_service.generate_text(prompt)
        
        # Assert
        mock_llm.invoke.assert_called_once_with(prompt)
        self.assertEqual(result, expected_response)
    
    @patch('RecruitReach2.services.llm.llm_service.ChatOpenAI')
    @patch('RecruitReach2.services.llm.llm_service.ConfigManager')
    @patch('RecruitReach2.services.llm.llm_service.ChatPromptTemplate')
    def test_generate_with_template(self, mock_chat_prompt_template, mock_config_manager, mock_chat_openai):
        """Test generating text with a template using LLMService."""
        # Arrange
        api_key = "test_api_key"
        template = "Template {variable}"
        input_variables = {"variable": "value"}
        expected_response = "Generated text"
        
        # Mock the ChatOpenAI instance
        mock_llm = MagicMock()
        mock_chat_openai.return_value = mock_llm
        
        # Mock the ChatPromptTemplate instance
        mock_prompt = MagicMock()
        mock_chat_prompt_template.return_value = mock_prompt
        
        # Mock the chain
        mock_chain = MagicMock()
        mock_prompt.__or__.return_value = mock_chain
        mock_chain.invoke.return_value = expected_response
        
        # Act
        llm_service = LLMService(api_key=api_key)
        result = llm_service.generate_with_template(
            template=template,
            input_variables=input_variables
        )
        
        # Assert
        mock_chat_prompt_template.assert_called_once_with([("system", template), ("human", "generate")])
        mock_prompt.__or__.assert_called_once_with(mock_llm)
        mock_chain.invoke.assert_called_once_with(input_variables)
        self.assertEqual(result, expected_response)


if __name__ == '__main__':
    unittest.main()
