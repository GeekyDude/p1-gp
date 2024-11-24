#collections

category = "category"

def User(sharedState):
    if sharedState is None or 'Environment' not in sharedState or sharedState['Environment'] == 'test':
        return "TestUser"
    return "User"


def Agent(sharedState):
    if sharedState is None or 'Environment' not in sharedState or sharedState['Environment'] == 'test':
        return "TestAgent"
    return "Agent"