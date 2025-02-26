from teams import Application, ApplicationOptions, TeamsAdapter
from teams.state import TurnState, ConversationState
from config import Config
from botbuilder.core import MemoryStorage, TurnContext
from semantic_kernel.contents import ChatHistory

from sk_conversation_agent import SemanticKernelConversationAgent

CONFIG = Config()
BOTAPPID = CONFIG.APP_ID
storage = MemoryStorage()

teamsApp = Application[TurnState](
    ApplicationOptions(
        bot_app_id=CONFIG.APP_ID,
        storage=storage,
        adapter=TeamsAdapter(CONFIG)
    )
)

teamsApp.kernel = None

@teamsApp.before_turn
async def setupSemanticKernel(context: TurnContext, state: TurnState):
    # Initialize Semantic Kernel
    if teamsApp.kernel is None:
        print("\nSetting up new Semantic Kernel...")
        # Check if there is a chat history already in the state and if yes, use it
        chat_history = state.conversation.get("chat_history") or ChatHistory()
        teamsApp.kernel = SemanticKernelConversationAgent(chat_history=chat_history)
    else:
        print("\nUsing existing Semantic Kernel...") 

    
    # # Load existing chat history from state or initialize a new one
    # chat_history = state.conversation.get("chat_history")
    # if chat_history is None:
    #     chat_history = ChatHistory()
    # state.kernel = SemanticKernelConversationAgent(chat_history=chat_history)
    return state

@teamsApp.activity("message")
async def on_message(context: TurnContext, state: TurnState):
    user_message = context.activity.text
    # sk_response = await state.kernel.chat(user_message)
    sk_response = await teamsApp.kernel.chat(user_message)
    
    # Store the updated chat_history back into conversation state
    # state.conversation["chat_history"] = state.kernel.chat_history
    state.conversation["chat_history"] = teamsApp.kernel.chat_history
    await context.send_activity(f"{sk_response}")
    return True