"""Configuration module for deep-research-cli"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for model settings"""
    #deepseek-r1-distill-qwen-32b
    #deepseek-r1-distill-llama-70b
    SMART_MODEL = os.getenv('SMART_MODEL', "deepseek-r1-distill-qwen-32b")
    NORMAL_MODEL = os.getenv('NORMAL_MODEL', "deepseek-r1-distill-qwen-32b")
    API_KEY = os.getenv('OPENAI_KEY')
    API_BASE = os.getenv('OPENAI_BASE')
