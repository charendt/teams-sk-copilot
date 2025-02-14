from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.contents import AuthorRole, ChatHistory, ChatMessageContent


class SemanticKernelConversationAgent():
    def __init__(self):

        self.kernel = Kernel()
        service_id = "agent"
        self.kernel.add_service(AzureChatCompletion(env_file_path=".env", service_id=service_id))

        settings = self.kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
        settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

        self.chat_history = ChatHistory()
        self.agent = ChatCompletionAgent(
            kernel=self.kernel, 
            service_id=service_id,
            name="ChatAgent",
            instructions="You can chat with me about any topic.",
            arguments=KernelArguments(settings=settings)
        )

    async def chat(self, prompt: str) -> str:
        self.chat_history.add_message(ChatMessageContent(role=AuthorRole.USER, content=prompt))

        response = None
        async for response in self.agent.invoke(history=self.chat_history, user_input=prompt):
            if not hasattr(self, 'logged_once'):
                print(f'Chat history: {self.chat_history}')
                print(f'User prompt: {prompt}')
                self.logged_once = True
            print(f'SK response: {response.content}')
        
        return response.content
