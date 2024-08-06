import pytest
from unittest.mock import MagicMock, AsyncMock
from aiogram.fsm.state import StatesGroup, State
from y24fw.aiogram.fsm import FSMContext

class MyStates(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()

@pytest.fixture
def fsm_context():
    storage = AsyncMock()
    key = "test_key"
    return FSMContext(storage, key)

@pytest.mark.asyncio
async def test_set_state(fsm_context):
    state1_function = MagicMock()
    await fsm_context.set_state(MyStates.state1, state1_function)
    assert fsm_context.current_state_fun[0] == MyStates.state1
    assert fsm_context.current_state_fun[1] == state1_function

@pytest.mark.asyncio
async def test_set_state_with_kwargs(fsm_context):
    state2_function = MagicMock()
    await fsm_context.set_state(MyStates.state2, state2_function, arg1="value1", arg2="value2")
    assert fsm_context.current_state_fun[2] == {"arg1": "value1", "arg2": "value2"}

@pytest.mark.asyncio
async def test_undo_state(fsm_context):
    state1_function = MagicMock()
    state2_function = MagicMock()
    await fsm_context.set_state(MyStates.state1, state1_function, arg1="value1", arg2="value2")
    await fsm_context.set_state(MyStates.state2, state2_function, arg1="value3", arg2="value4")

    await fsm_context.undo_state()
    state1_function.assert_called_once_with(arg1="value1", arg2="value2")
    assert fsm_context.current_state_fun[0] == MyStates.state1

@pytest.mark.asyncio
async def test_undo_state_multiple_times(fsm_context):
    state1_function = MagicMock()
    state2_function = MagicMock()
    state3_function = MagicMock()
    await fsm_context.set_state(MyStates.state1, state1_function)
    await fsm_context.set_state(MyStates.state2, state2_function)
    await fsm_context.set_state(MyStates.state3, state3_function)

    await fsm_context.undo_state()
    state2_function.assert_called_once()
    assert fsm_context.current_state_fun[0] == MyStates.state2

    await fsm_context.undo_state()
    state1_function.assert_called_once()
    assert fsm_context.current_state_fun[0] == MyStates.state1

    with pytest.raises(IndexError) as exc_info:
        await fsm_context.undo_state()
    assert fsm_context.current_state_fun is None
    assert str(exc_info.value) == "No more states to undo"

@pytest.mark.asyncio
async def test_clear(fsm_context):
    state1_function = MagicMock()
    state2_function = MagicMock()
    await fsm_context.set_state(MyStates.state1, state1_function)
    await fsm_context.set_state(MyStates.state2, state2_function)

    await fsm_context.clear()
    assert fsm_context.stack_states_fun == []
    assert fsm_context.current_state_fun is None
