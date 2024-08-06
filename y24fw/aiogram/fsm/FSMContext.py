from typing import Coroutine, Any, Callable

from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext as OldFSMContext


class FSMContext(OldFSMContext):
    stack_states_fun: list[State] = []
    current_state_fun: State | None = None

    def __init__(self, storage, key):
        super().__init__(storage, key)
    
    async def set_state(self, state: str | State | None = None, 
                  fun: Callable | None = None, 
                  **fun_kwargs: dict[Any]) -> Coroutine[Any, Any, None]:
        if not isinstance(state, State):
            return

        if self.current_state_fun is not None:
            self.stack_states_fun.append(self.current_state_fun)

        self.current_state_fun: tuple[State, Callable, dict[Any]] = (state, fun, fun_kwargs)

        return await super().set_state(state)

    async def undo_state(self) -> Coroutine[Any, Any, None]:
        if self.stack_states_fun:
            state = self.stack_states_fun.pop()
            self.current_state_fun = state

            if state[1]:
                state[1](**state[2])
        else:
            self.current_state_fun = None
            raise IndexError("No more states to undo")

    async def clear(self) -> Coroutine[Any, Any, None]:
        self.stack_states_fun.clear()
        self.current_state_fun = None
        return await super().clear()
