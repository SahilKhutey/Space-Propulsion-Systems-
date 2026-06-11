import numpy as np

class ParameterSampler:
    @staticmethod
    def sample_normal(mean: float, std: float) -> float:
        return float(np.random.normal(mean, std))

    @staticmethod
    def sample_uniform(low: float, high: float) -> float:
        return float(np.random.uniform(low, high))
