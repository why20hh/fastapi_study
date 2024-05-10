# class TaskManager:
#     def __init__(self):
#         self.tasks = {}
#
#     def add_task(self, task_id, task_info=None):
#         self.tasks[task_id] = {"status": "pending", "info": task_info}
#
#     def update_task_status(self, task_id, status):
#         if task_id in self.tasks:
#             self.tasks[task_id]["status"] = status
#             print(f"Task {task_id} status updated to {status}")
#
#     def get_tasks(self):
#         # 返回所有任务状态，根据需要可以过滤或格式化
#         return list(self.tasks.values())
import asyncio


class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.task_events = {}

    def add_task(self, task_id, task_info=None):
        self.tasks[task_id] = {"status": "pending", "info": task_info}
        self.task_events[task_id] = asyncio.Event()

    def update_task_status(self, task_id, status):
        print(self.tasks)
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status
            print(f"Task {task_id} status updated to {status}")
            self.task_events[task_id].set()

    async def wait_for_task_completion(self, task_id):
        await self.task_events[task_id].wait()

    def get_tasks(self):
        return list(self.tasks.values())
