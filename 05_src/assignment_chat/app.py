from assignment_chat.main import get_graph
from langchain_core.messages import HumanMessage, AIMessage
import gradio as gr
from dotenv import load_dotenv

from utils.logger import get_logger
_logs = get_logger(__name__)

llm = get_graph()

load_dotenv('.secrets')

def chat_with_jack(message: str, history: list[dict]) -> str:
    langchain_messages = []
    n = 0
    _logs.debug(f"History: {history}")
    for msg in history:
        if msg['role'] == 'user':
            langchain_messages.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'assistant':
            langchain_messages.append(AIMessage(content=msg['content']))
            n += 1
    langchain_messages.append(HumanMessage(content=message))

    state = {
        "messages": langchain_messages,
        "llm_calls": n
    }

    response = llm.invoke(state)
    return response['messages'][len(response['messages']) - 1].content

custom_css = """
/* Main background - ocean gradient */
body, .gradio-container {
    background: linear-gradient(135deg, #0a1929 0%, #1a3a52 50%, #2d5f7a 100%) !important;
}

/* Title style */
.gradio-container h1 {
    color: #ffd700 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.7) !important;
    font-family: 'Georgia', serif !important;
}

/* Description text - white for visibility on dark background */
.gradio-container .prose, .gradio-container .prose p, .gradio-container .prose em {
    color: #ffffff !important;
}

/* Chat messages */
.message.user {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
    color: #ffffff !important;
    border-left: 4px solid #ffd700 !important;
}

.message.bot {
    background: linear-gradient(135deg, #3d2314 0%, #5c3a1f 100%) !important;
    color: #f5f5f5 !important;
    border-left: 4px solid #8B4513 !important;
}

/* Chatbot container */
.chatbot {
    border: 2px solid #8B4513 !important;
    border-radius: 10px !important;
    background: rgba(26, 26, 46, 0.7) !important;
}

/* Input textbox */
.input-box, textarea {
    background: rgba(255, 255, 255, 0.9) !important;
    color: #1a1a1a !important;
    border: 2px solid #8B4513 !important;
    border-radius: 8px !important;
}

/* Example buttons */
.examples button {
    background: linear-gradient(135deg, #8B4513 0%, #654321 100%) !important;
    color: #f5deb3 !important;
    border: 1px solid #ffd700 !important;
    border-radius: 8px !important;
    font-family: 'Georgia', serif !important;
    transition: all 0.3s ease !important;
}

.examples button:hover {
    background: linear-gradient(135deg, #654321 0%, #8B4513 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3) !important;
}

/* Submit button */
.submit-btn {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
    color: #ffffff !important;
    border: 2px solid #ffd700 !important;
    font-weight: bold !important;
}

.submit-btn:hover {
    background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%) !important;
}
"""

chat = gr.ChatInterface(
    fn=chat_with_jack,
    type="messages",
    title=" Captain Jack Sparrow's Caribbean ChatBot ",
    description="'Not all treasure is silver and gold, mate.",
    examples=[
        "What's the sailing weather today?",
        "Tell me about Blackbeard",
        "Tell me a pirate tale"
    ],
    css=custom_css
)

if __name__ == "__main__":
    _logs.info('Entering Jack Sparrow\'s Caribbean world...')
    chat.launch()
