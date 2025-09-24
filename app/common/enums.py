from enum import Enum as NativeEnum


class Gender(NativeEnum):
    NONE = "NONE"
    MALE = "male"
    FEMALE = "female"


class CompanyMode(NativeEnum):
    OUTSOURCE = "outsource"
    PRODUCT = "product"


class TaskStatus(NativeEnum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(NativeEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
