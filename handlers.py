from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter, BaseFilter  
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext




router = Router()

tasks: dict[int, list[str]] = {}
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    choice_eat = State()     
    remove_eat = State()   
 
@router.message(Command(commands='show_list'))
async def show_list(msg: Message):
    if msg.from_user.id in tasks and tasks[msg.from_user.id]:
        product_list = enumerate(tasks[msg.from_user.id], 1)
        for i, val in product_list:
            await msg.answer(text=f'{i}. {val}')
    else:
        await msg.answer(text='Список пуст') 

@router.message(Command(commands='remove'))
async def remove_dp(msg: Message,state: FSMContext):
        await msg.answer(text='Введите номер продукта который хотите удалить')
        await state.set_state(FSMFillForm.remove_eat)



@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(msg: Message, state: FSMContext):
    await msg.answer(
        text='Этот бот демонстрирует работу составления и перечесление списка продуктов для дома\n\n'
    )
    await state.set_state(FSMFillForm.choice_eat)
    



@router.message(StateFilter(FSMFillForm.choice_eat))
async def add_unit_food(msg: Message):
    user_id = msg.from_user.id
    if user_id not in tasks:
        tasks[user_id] = []
    tasks[user_id].append(msg.text)
    await msg.answer(text='Продукт добавлен. Введите следующий продукт или введите /show_list для просмотра списка.')
    

@router.message(StateFilter(FSMFillForm.remove_eat))
async def remove_eat(msg: Message,state: FSMContext):
    try:
        eat_index = int(msg.text)
        if(0 < eat_index <len(tasks[msg.from_user.id])+1):
            remove_eat_index = tasks[msg.from_user.id].pop(eat_index-1)
            await msg.answer(text=f'Продукт {remove_eat_index} удалён')
        else:
            await msg.answer(text='Введите неверный номер')
    except (ValueError, IndexError):
        await msg.answer(text='Значение должо быть число')
    finally:
        await state.set_state(FSMFillForm.choice_eat)

@router.message(Command(commands='app'))
async def app_dp(msg: Message):
        await msg.answer(text='app')


