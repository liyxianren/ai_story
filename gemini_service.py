import os
import logging
import time
from typing import Dict, Any, Optional
from google import genai
from google.genai import types

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    """Service for handling Gemini AI text processing"""
    
    def __init__(self):
        """Initialize the Gemini service with API key authentication"""
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            key_file_path = os.path.join(script_dir, 'google_key.txt')
            
            # Read API key from google_key.txt file
            with open(key_file_path, 'r', encoding='utf-8') as f:
                self.api_key = f.read().strip()
            
            if not self.api_key:
                raise ValueError("API key is empty in google_key.txt")
            
            # Create client with API key and SSL configuration
            self.client = genai.Client(api_key=self.api_key)
            
            logger.info("Gemini service initialized successfully")
            
        except FileNotFoundError:
            logger.error("google_key.txt file not found. Please ensure the file exists in the project root.")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Gemini service: {str(e)}")
            raise
    
    def process_transcription(self, transcript: str, language: str = 'en-US') -> Dict[str, Any]:
        """
        Process a transcription using Gemini AI
        
        Args:
            transcript (str): The transcribed text to process
            language (str): The language of the transcript
            
        Returns:
            Dict[str, Any]: Processing result with success status and content
        """
        try:
            if not transcript or not transcript.strip():
                return {
                    'success': False,
                    'error': 'Empty transcript provided',
                    'content': '',
                    'model': ''
                }
            
            logger.info(f"Processing transcription with Gemini: {transcript[:50]}...")
            
            # Create a prompt for processing the transcription
            prompt = self._create_processing_prompt(transcript, language)
            
            # Generate content using Gemini with retry mechanism
            response = self._generate_content_with_retry(prompt)
            
            if response and response.text:
                logger.info(f"Gemini processing successful: {response.text[:50]}...")
                return {
                    'success': True,
                    'content': response.text.strip(),
                    'model': 'gemini-2.5-flash',
                    'language': language
                }
            else:
                logger.warning("Gemini returned empty response")
                return {
                    'success': False,
                    'error': 'Gemini returned empty response',
                    'content': '',
                    'model': 'gemini-2.5-flash'
                }
                
        except Exception as e:
            logger.error(f"Gemini processing error: {str(e)}")
            return {
                'success': False,
                'error': f"Gemini processing failed: {str(e)}",
                'content': '',
                'model': 'gemini-2.5-flash'
            }
    
    def _generate_content_with_retry(self, prompt: str, max_retries: int = 3):
        """
        Generate content with retry mechanism for SSL errors
        
        Args:
            prompt (str): The prompt to send to Gemini
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            Response object from Gemini API
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Gemini API call attempt {attempt + 1}/{max_retries}")
                
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,  # Balanced creativity
                        thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disable thinking for faster response
                    )
                )
                
                logger.info("Gemini API call successful")
                return response
                
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"Gemini API call attempt {attempt + 1} failed: {error_msg}")
                
                # Check if it's an SSL error
                if "SSL" in error_msg or "EOF" in error_msg or "protocol" in error_msg:
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 2  # Exponential backoff: 2s, 4s, 6s
                        logger.info(f"SSL/connection error detected. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error("All retry attempts failed due to SSL/connection errors")
                        raise Exception(f"SSL connection failed after {max_retries} attempts: {error_msg}")
                else:
                    # For non-SSL errors, raise immediately
                    logger.error(f"Non-SSL error encountered: {error_msg}")
                    raise
        
        # This should not be reached, but just in case
        raise Exception("Unexpected error: All retry attempts exhausted")
    
    def generate_story_description(self, story_content: str, language: str = 'zh-CN') -> Dict[str, Any]:
        """
        Generate a compelling story description/summary using Gemini AI
        
        Args:
            story_content (str): The full story content
            language (str): The language of the story
            
        Returns:
            Dict[str, Any]: Result with success status and generated description
        """
        try:
            if not story_content or not story_content.strip():
                return {
                    'success': False,
                    'error': 'Empty story content provided',
                    'description': ''
                }
            
            logger.info(f"Generating story description with Gemini: {story_content[:50]}...")
            
            # Create description generation prompt
            prompt = self._create_description_prompt(story_content, language)
            
            # Generate description using Gemini
            response = self._generate_content_with_retry(prompt)
            
            if response and response.text:
                description = response.text.strip()
                logger.info(f"Story description generated successfully: {description[:50]}...")
                return {
                    'success': True,
                    'description': description,
                    'model': 'gemini-2.5-flash'
                }
            else:
                logger.warning("Gemini returned empty description")
                return {
                    'success': False,
                    'error': 'Gemini returned empty response',
                    'description': ''
                }
                
        except Exception as e:
            logger.error(f"Description generation error: {str(e)}")
            return {
                'success': False,
                'error': f"Description generation failed: {str(e)}",
                'description': ''
            }

    def _create_description_prompt(self, story_content: str, language: str) -> str:
        """
        Create a prompt for generating story description
        
        Args:
            story_content (str): The full story content
            language (str): The language of the story
            
        Returns:
            str: The prompt for story description generation
        """
        # Determine language for response
        if language.startswith('zh') or language.startswith('cmn'):
            language_instruction = "请用中文回应。"
            prompt_template = """你是一个专业的故事推广文案编辑。你的任务是为给定的故事创作一个吸引人的简介，用于故事发布和推广。

请根据以下要求为这个故事写一个简介：

📝 **简介要求**：
1. **长度控制**：简介应该在50-150字之间，简洁而有力
2. **吸引读者**：突出故事的核心亮点和吸引人的元素
3. **不剧透**：不要透露故事的结局或关键转折点
4. **情感触达**：传达故事的情感基调和主要主题
5. **读者群体**：适合目标读者群体的语言风格
6. **直接输出**：只输出简介内容，不要添加任何解释

**故事内容**：
{story_content}

请直接提供简介内容，让读者产生阅读兴趣。

{language_instruction}"""
        else:
            language_instruction = "Please respond in English."
            prompt_template = """You are a professional story marketing copywriter. Your task is to create an engaging description for the given story that will be used for story publishing and promotion.

Please write a description for this story according to the following requirements:

📝 **Description Requirements**:
1. **Length Control**: The description should be 50-150 words, concise yet powerful
2. **Attract Readers**: Highlight the core appeal and engaging elements of the story
3. **No Spoilers**: Don't reveal the ending or key plot twists
4. **Emotional Impact**: Convey the story's emotional tone and main themes
5. **Target Audience**: Use language style appropriate for the target readers
6. **Direct Output**: Only output the description content without any explanations

**Story Content**:
{story_content}

Please provide the description directly to make readers interested in reading the story.

{language_instruction}"""
        
        return prompt_template.format(
            story_content=story_content,
            language_instruction=language_instruction
        )

    def _create_processing_prompt(self, transcript: str, language: str) -> str:
        """
        Create a story polishing prompt for the transcription
        
        Args:
            transcript (str): The transcribed text
            language (str): The language of the transcript
            
        Returns:
            str: The prompt for Gemini story polishing
        """
        # Determine language for response
        if language.startswith('zh') or language.startswith('cmn'):
            language_instruction = "请用中文回应。"
            prompt_template = """你是一个专业的故事润色编辑助手。你的任务是将用户录音转录的原始文本转换成一个流畅、引人入胜的故事。

请按照以下要求润色这段转录文本：

📝 **润色要求**：
1. **语法修正**：修复语法错误、时态问题和语言不当之处
2. **流畅性改进**：使句子衔接更自然，提高可读性
3. **叙述增强**：丰富描述，增加生动的细节和情感表达
4. **结构优化**：整理段落结构，确保逻辑清晰
5. **保持原意**：确保不改变原故事的核心内容和意图
6. **自然风格**：保持讲述者的个人风格和语调
7. **保持语言**：必须保持原文的语言，不要翻译成其他语言

**原始转录文本**：
{transcript}

请直接提供润色后的故事，无需解释过程。让故事听起来自然、完整且引人入胜。保持原文语言不变。

{language_instruction}"""
        else:
            language_instruction = "Please respond in English."
            prompt_template = """You are a professional story polishing editor assistant. Your task is to transform the raw transcribed text from user's recording into a smooth, engaging, and well-crafted story.

Please polish this transcribed text according to the following requirements:

📝 **Polishing Requirements**:
1. **Grammar Correction**: Fix grammatical errors, tense issues, and awkward phrasing
2. **Flow Improvement**: Make sentences connect naturally and improve readability
3. **Narrative Enhancement**: Enrich descriptions, add vivid details and emotional expression
4. **Structure Optimization**: Organize paragraph structure and ensure logical clarity
5. **Preserve Intent**: Maintain the core content and intention of the original story
6. **Natural Style**: Keep the storyteller's personal style and tone
7. **Keep Original Language**: Maintain the same language as the original text - do not translate to other languages

**Original Transcribed Text**:
{transcript}

Please provide the polished story directly without explaining the process. Make the story sound natural, complete, and engaging. Keep the same language as the original text.

{language_instruction}"""
        
        return prompt_template.format(
            transcript=transcript,
            language_instruction=language_instruction
        )

# Global instance
gemini_service = GeminiService() 