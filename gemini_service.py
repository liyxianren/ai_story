import os
import logging
import time
from typing import Dict, Any, Optional
import google.generativeai as genai

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    """Service for handling Gemini AI text processing"""
    
    def __init__(self):
        """Initialize the Gemini service with API key authentication"""
        try:
            # Get API key from environment variable
            self.api_key = os.environ.get('GOOGLE_API_KEY')
            
            if not self.api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not found")
            
            # Configure API key
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            
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
                    'language': 'en-US'  # Always return English since we translate everything
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
                
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7  # Balanced creativity
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
            language_instruction = "Please respond in English."
            prompt_template = """You are a professional story marketing copy editor. Your task is to create an engaging summary for the given story, for story publishing and promotion.

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
        # Always respond in English - translate if necessary
        language_instruction = "Please respond in English only."
        
        # Determine if translation is needed
        if language.startswith('zh') or language.startswith('cmn'):
            source_language = "Chinese"
        elif language.startswith('uk'):
            source_language = "Ukrainian" 
        elif language.startswith('ru'):
            source_language = "Russian"
        elif language.startswith('es'):
            source_language = "Spanish"
        elif language.startswith('fr'):
            source_language = "French"
        elif language.startswith('de'):
            source_language = "German"
        elif language.startswith('ja'):
            source_language = "Japanese"
        elif language.startswith('ko'):
            source_language = "Korean"
        elif language.startswith('ar'):
            source_language = "Arabic"
        elif language.startswith('hi'):
            source_language = "Hindi"
        elif language.startswith('pt'):
            source_language = "Portuguese"
        elif language.startswith('it'):
            source_language = "Italian"
        elif language.startswith('nl'):
            source_language = "Dutch"
        elif language.startswith('th'):
            source_language = "Thai"
        elif language.startswith('vi'):
            source_language = "Vietnamese"
        else:
            source_language = "the original language"
        
        prompt_template = """You are a professional story polishing and translation editor assistant. Your task is to transform the raw transcribed text from user's recording into a smooth, engaging, and well-crafted English story.

Please polish and translate this transcribed text according to the following requirements:

📝 **Polishing & Translation Requirements**:
1. **Translation to English**: If the original text is in {source_language}, translate it completely to natural, fluent English
2. **Grammar Perfection**: Ensure perfect English grammar, tense consistency, and natural phrasing
3. **Flow Enhancement**: Make sentences connect seamlessly and improve overall readability
4. **Narrative Enrichment**: Add vivid descriptions, emotional depth, and engaging details while staying true to the original story
5. **Structure Optimization**: Organize content into clear paragraphs with logical flow
6. **Preserve Core Intent**: Maintain the original story's meaning, emotions, and cultural context
7. **Natural English Style**: Create a story that reads as if it were originally written by a native English speaker
8. **Storytelling Excellence**: Transform the raw transcript into a compelling, publishable English story

**Original Transcribed Text in {source_language}**:
{transcript}

Please provide the polished English story directly without any explanations or meta-commentary. The result should be a beautifully written English story that captures the essence and emotion of the original while being completely natural and engaging to English readers.

{language_instruction}"""
        
        return prompt_template.format(
            transcript=transcript,
            source_language=source_language,
            language_instruction=language_instruction
        )
    
    def chat_conversation(self, user_message: str, current_story: str, chat_history: list, language: str = 'en-US') -> Dict[str, Any]:
        """
        Have a natural conversation with the user about their story
        
        Args:
            user_message (str): The user's message
            current_story (str): The current story text
            chat_history (list): Previous conversation history
            language (str): The language for the conversation
            
        Returns:
            Dict[str, Any]: Conversation result with success status and content
        """
        try:
            if not user_message or not user_message.strip():
                return {
                    'success': False,
                    'error': 'Empty message provided',
                    'content': '',
                    'model': ''
                }
            
            logger.info(f"Processing chat conversation: {user_message[:50]}...")
            
            # Create a conversational prompt
            prompt = self._create_chat_prompt(user_message, current_story, chat_history, language)
            
            # Generate content using Gemini with retry mechanism
            response = self._generate_content_with_retry(prompt)
            
            if response and response.text:
                logger.info(f"Gemini chat successful: {response.text[:50]}...")
                return {
                    'success': True,
                    'content': response.text.strip(),
                    'model': 'gemini-2.5-flash',
                    'language': language
                }
            else:
                logger.warning("Gemini returned empty response for chat")
                return {
                    'success': False,
                    'error': 'Gemini returned empty response',
                    'content': '',
                    'model': 'gemini-2.5-flash'
                }
                
        except Exception as e:
            logger.error(f"Gemini chat error: {str(e)}")
            return {
                'success': False,
                'error': f"Gemini chat failed: {str(e)}",
                'content': '',
                'model': 'gemini-2.5-flash'
            }
    
    def _create_chat_prompt(self, user_message: str, current_story: str, chat_history: list, language: str) -> str:
        """
        Create a conversational prompt for natural chat interaction
        
        Args:
            user_message (str): The user's latest message
            current_story (str): The current story text
            chat_history (list): Previous conversation history
            language (str): The language for the conversation
            
        Returns:
            str: The prompt for natural conversation
        """
        # Determine language for response
        if language.startswith('zh') or language.startswith('cmn'):
            language_instruction = "请用中文自然地回应。"
            greeting_words = ['hello', 'hi', 'hey', '你好', '嗨', '问好', 'how are you', '怎么样', '如何']
            
            # Check if this is a casual conversation
            is_casual = any(word.lower() in user_message.lower() for word in greeting_words)
            
            if is_casual or len(user_message.strip()) < 20:
                # For casual/short messages, be more conversational
                prompt_template = """你是一个友好的AI写作助手。用户正在和你聊天。

📖 **当前故事**：
{current_story}

💬 **聊天历史**：
{chat_history_text}

👤 **用户消息**：{user_message}

请自然地回应用户。如果他们只是打招呼或聊天，就正常对话。如果他们询问故事改进，再提供建议。不要强制将每个对话都转向故事润色。保持友好和自然的语调。

{language_instruction}"""
            else:
                # For longer messages, provide more detailed assistance
                prompt_template = """你是一个专业的写作导师和故事编辑。用户正在和你交流关于他们的故事。

📖 **当前故事**：
{current_story}

💬 **聊天历史**：
{chat_history_text}

👤 **用户消息**：{user_message}

根据用户的消息内容自然回应：
- 如果用户想要改进故事：提供具体的建议和可能的修改版本
- 如果用户询问写作技巧：分享相关的写作知识和技巧
- 如果用户只是想讨论故事：进行有意义的讨论
- 如果用户有其他问题：友好地回答并提供帮助

保持对话的自然性，不要总是推销故事润色服务。

{language_instruction}"""
        else:
            language_instruction = "Please respond naturally in English."
            greeting_words = ['hello', 'hi', 'hey', 'how are you', 'what\'s up', 'good morning', 'good afternoon', 'good evening']
            
            # Check if this is a casual conversation
            is_casual = any(word.lower() in user_message.lower() for word in greeting_words)
            
            if is_casual or len(user_message.strip()) < 20:
                # For casual/short messages, be more conversational
                prompt_template = """You are a friendly AI writing assistant. The user is chatting with you.

📖 **Current Story**:
{current_story}

💬 **Chat History**:
{chat_history_text}

👤 **User Message**: {user_message}

Please respond naturally to the user. If they're just greeting or chatting, have a normal conversation. Only offer story improvement suggestions if they specifically ask for help with their story. Don't force every conversation toward story polishing. Keep it friendly and natural.

{language_instruction}"""
            else:
                # For longer messages, provide more detailed assistance
                prompt_template = """You are a professional writing mentor and story editor. The user is communicating with you about their story.

📖 **Current Story**:
{current_story}

💬 **Chat History**:
{chat_history_text}

👤 **User Message**: {user_message}

Respond naturally based on the user's message:
- If user wants story improvement: Provide specific suggestions and possible revisions
- If user asks about writing techniques: Share relevant writing knowledge and tips
- If user wants to discuss the story: Have a meaningful discussion
- If user has other questions: Answer helpfully and friendly

Keep the conversation natural and don't always push story polishing services.

{language_instruction}"""
        
        # Format chat history
        chat_history_text = ""
        if chat_history:
            for i, chat in enumerate(chat_history[-5:]):  # Only include last 5 exchanges
                role = chat.get('role', 'unknown')
                content = chat.get('content', '')
                if role.lower() == 'user':
                    chat_history_text += f"User: {content}\n"
                elif role.lower() == 'assistant':
                    chat_history_text += f"AI: {content}\n"
        else:
            chat_history_text = "No previous conversation."
        
        return prompt_template.format(
            current_story=current_story,
            chat_history_text=chat_history_text,
            user_message=user_message,
            language_instruction=language_instruction
        )

# Global instance
gemini_service = GeminiService() 