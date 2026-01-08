from enum import Enum


class AgentLifecycleEvent(str, Enum):
    USERCREATED = "agenticuseridentitycreated"
    USERWORKLOADONBOARDINGUPDATED = "agenticuserworkloadonboardingupdated"
    USERDELETED = "agenticuseridentitydeleted"
