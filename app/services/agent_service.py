"""
Customer Care Agent Service
Core business logic for the AI support agent
"""

import logging
from typing import Dict, List

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate

from app.core.config import settings


# Configure logging
logging.basicConfig(
    filename=settings.log_file,
    level=getattr(logging, settings.log_level),
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


class AgentService:
    """Customer Care Agent Service"""
    
    def __init__(self):
        """Initialize the agent service"""
        self.llm = None
        self.retriever = None
        self.conversation_memory: List[Dict[str, str]] = []
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize LLM, embeddings, and vector store"""
        try:
            # Initialize LLM
            self.llm = ChatOpenAI(
                model=settings.openai_model,
                temperature=settings.openai_temperature
            )
            
            # Load knowledge base
            loader = TextLoader(settings.knowledge_base_path)
            documents = loader.load()
            
            # Split documents
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap
            )
            docs = splitter.split_documents(documents)
            
            # Create embeddings and vector store
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(docs, embeddings)
            
            # Create retriever
            self.retriever = vectorstore.as_retriever(
                search_kwargs={"k": settings.retrieval_k}
            )
            
            logger.info("Agent service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize agent service: {str(e)}")
            raise
    
    def is_safe_query(self, query: str) -> bool:
        """Check if query contains unsafe keywords"""
        query_lower = query.lower()
        for keyword in settings.unsafe_keywords:
            if keyword in query_lower:
                logger.warning(f"Unsafe query detected: {query}")
                return False
        return True
    
    def retrieve_context(self, query: str) -> str:
        """Retrieve relevant context from knowledge base"""
        try:
            docs = self.retriever.invoke(query)
            if not docs:
                return "No relevant knowledge found."
            
            context = "\n".join([doc.page_content for doc in docs])
            return context
        except Exception as e:
            logger.error(f"Context retrieval failed: {str(e)}")
            return "Error retrieving context."
    
    def add_to_memory(self, role: str, message: str):
        """Add message to conversation memory"""
        self.conversation_memory.append({
            "role": role,
            "message": message
        })
        
        # Keep only recent messages
        if len(self.conversation_memory) > settings.max_conversation_memory:
            self.conversation_memory.pop(0)
    
    def get_memory_context(self) -> str:
        """Get conversation memory as formatted string"""
        if not self.conversation_memory:
            return "No previous conversation."
        
        memory_text = ""
        for item in self.conversation_memory:
            memory_text += f"{item['role']}: {item['message']}\n"
        
        return memory_text
    
    def generate_response(self, user_query: str) -> Dict[str, str]:
        """Generate response for user query"""
        try:
            # Safety check
            if not self.is_safe_query(user_query):
                return {
                    "response": (
                        "I cannot assist with this request as it may violate "
                        "security policies. Please contact human support for assistance."
                    ),
                    "status": "blocked"
                }
            
            # Retrieve context
            context = self.retrieve_context(user_query)
            
            # Get memory
            memory = self.get_memory_context()
            
            # Create prompt
            prompt = PromptTemplate.from_template("""
You are an enterprise AI customer support agent.

Rules:
- Use only retrieved knowledge from the knowledge base
- Avoid hallucinations or making up information
- Escalate sensitive issues to human support
- Be professional and courteous
- Protect customer privacy
- If information is not in the knowledge base, say so clearly

--------------------------------------------------

Conversation Memory:
{memory}

--------------------------------------------------

Retrieved Context:
{context}

--------------------------------------------------

Customer Query:
{query}

--------------------------------------------------

Provide a helpful response that includes:
- Clear understanding of the issue
- Resolution steps based on retrieved knowledge
- Whether escalation to human support is needed
- Your confidence level in the response
""")
            
            # Generate final prompt
            final_prompt = prompt.invoke({
                "memory": memory,
                "context": context,
                "query": user_query
            })
            
            # Get LLM response
            result = self.llm.invoke(final_prompt)
            
            return {
                "response": result.content,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            return {
                "response": (
                    "I encountered a technical issue while processing your request. "
                    "Please try again or contact human support."
                ),
                "status": "failed"
            }
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.conversation_memory.clear()
        logger.info("Conversation memory cleared")


# Global agent service instance
agent_service = AgentService()

# Made with Bob
