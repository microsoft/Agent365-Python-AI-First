from enum import Enum


class AgentSubChannel(str, Enum):
    EMAIL = "email"
    EXCEL = "excel"
    WORD = "word"
    POWERPOINT = "powerpoint"
    FEDERATED_KNOWLEDGE_SERVICE = "federatedknowledgeservice"
