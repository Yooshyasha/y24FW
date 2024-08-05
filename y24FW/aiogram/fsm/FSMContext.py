from aiogram.fsm.context import FSMContext as OldFSMContext

class FSMContext(OldFSMContext):
    def __init__(self, FSMContext: OldFSMContext):
        super().__init__(FSMContext.storage, FSMContext.key)
