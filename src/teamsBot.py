from teams import Application, ApplicationOptions, TeamsAdapter
from teams.state import TurnState
from config import Config
from botbuilder.core import MemoryStorage, TurnContext

from sk_conversation_agent import SemanticKernelConversationAgent

CONFIG = Config()
BOTAPPID = CONFIG.APP_ID
sotrage = MemoryStorage()

teamsApp = Application[TurnState](
    ApplicationOptions(
        bot_app_id=CONFIG.APP_ID,
        storage=sotrage,
        adapter=TeamsAdapter(CONFIG)
    )
)

@teamsApp.activity("message")
async def on_message(context: TurnContext, state: TurnState):
    sk_response = await state.kernel.chat(context.activity.text)
    await context.send_activity(f"{sk_response}")
    return True

@teamsApp.before_turn
async def setupSemanticKernel(context: TurnContext, state: TurnState):
    state.kernel = SemanticKernelConversationAgent()
    return state