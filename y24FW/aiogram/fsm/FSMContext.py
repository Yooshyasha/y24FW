from typing import Coroutine, Any

from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext as OldFSMContext


class FSMContext(OldFSMContext):
    stack_states: list[State] = []
    current_state: State | None = None

    def __init__(self, storage, key):
        super().__init__(storage, key)

    def set_state(self, state: str | State | None = None) -> Coroutine[Any, Any, None]:
        if not isinstance(state, State):
            return

        if self.current_state is not None:
            self.stack_states.append(self.current_state)

        self.current_state = state

        return super().set_state(state)
    
    def undo_state(self) -> Coroutine[Any, Any, None]:
        if self.stack_states:
            state = self.stack_states.pop()
            return super().set_state(state)
        else:
            raise IndexError("No more states to undo")
        
    def clear(self) -> Coroutine[Any, Any, None]:
        self.stack_states.clear()
        return super().clear()
