from abc import ABC, abstractmethod



class DeploymentStrategy(ABC):
    @abstractmethod
    # class that inherits will define the configuration for the deployment such as the instance type, number of instances, etc.
    def deploy(self, model, endpoint_name: str, endpoint_config_name: str) -> None:
        pass


class Inference(ABC):
    """An abstract class that performs inference"""
    def __init__(self):
        self.model = None

    @abstractmethod
    def set_payload(self, inputs, parameters=None):
        pass

    @abstractmethod
    def inference(self):
        pass
        
        
        