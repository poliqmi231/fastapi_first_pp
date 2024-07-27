from database import new_session, TaskOrm
from schemas import STaskAdd, STask
from sqlalchemy import select, delete

class TaskRepository():
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    
    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            tasks_schemas = [STask.model_validate(task_model) for task_model in task_models]
            return tasks_schemas
    
    
    @classmethod
    async def delete_one(cls, del_id:int) -> int:
        async with new_session() as session:
            task_to_del = delete(TaskOrm).where(TaskOrm.id == del_id)
            await session.execute(task_to_del)
            await session.commit()
            return del_id