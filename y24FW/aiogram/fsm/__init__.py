from typing import Dict, Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from .FSMContext import FSMContext

class FSMMiddleware(BaseMiddleware):
    '''Swapping the original FSM for a custom one'''

    def __init__(self):
        pass

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, any]], Awaitable[Any]],
                       event: Message | CallbackQuery,
                       data: Dict[str, Any]) -> Any:

        async def _wrapped_handler(event: Message, data: Dict[str, Any]) -> Any:
            if not isinstance(data["state"], FSMContext):
                storage = data["state"].storage
                key = data["state"].key

                data["state"] = FSMContext(storage, key) 

            return await handler(event, data)
        
        return await _wrapped_handler(event, data)