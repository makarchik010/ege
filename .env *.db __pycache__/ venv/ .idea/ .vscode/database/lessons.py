from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db import add_user, get_user_lesson_id, get_lesson, update_user_lesson

router = Router()

class TaskState(StatesGroup):
    waiting_for_answer = State()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await add_user(message.from_user.id)
    await message.answer(
        "👋 Здорово! Бот запущен из GitHub-репозитория.\n\n"
        "Жми /lesson, чтобы открыть текущий урок."
    )

@router.message(Command("lesson"))
async def cmd_lesson(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lesson_id = await get_user_lesson_id(user_id)
    lesson = await get_lesson(lesson_id)
    
    if not lesson:
        await message.answer("🎉 Ты закрыл все доступные уроки! Жди новых обновлений.")
        return

    text = (
        f"📖 **Урок {lesson['lesson_id']}: {lesson['title']}**\n\n"
        f"💡 **Теория:**\n{lesson['theory']}\n\n"
        f"🎯 **Задача:**\n{lesson['task_text']}"
    )
    
    await message.answer(text, parse_mode="Markdown")
    await message.answer("Напиши ответ числом или строкой:")
    
    await state.set_state(TaskState.waiting_for_answer)
    await state.update_data(correct_answer=lesson["answer"], current_lesson=lesson["lesson_id"])

@router.message(TaskState.waiting_for_answer)
async def check_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    correct_answer = data.get("correct_answer")
    current_lesson = data.get("current_lesson")
    
    if message.text.strip().lower() == correct_answer.strip().lower():
        await update_user_lesson(message.from_user.id, current_lesson + 1)
        await message.answer("✅ Ответ верный! Урок зачтен.\nЖми /lesson, чтобы перейти к следующему.")
        await state.clear()
    else:
        await message.answer("❌ Ответ не сходится. Попробуй пересчитать.")
