import pytest
import numpy as np
import sys
from pathlib import Path

# Add paths for standalone execution if needed
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))

from core.mathematics.optimization.genetic import genetic_algorithm
from core.mathematics.optimization.bayesian import BayesianOptimizer


# ===== Test 30: Genetic Optimization =====
@pytest.mark.ai
class TestGeneticOptimization:
    """Test 30: Fitness improves over generations."""

    def test_fitness_improves(self):
        def f(x):
            return -(x[0] - 3.0)**2 - (x[1] + 1.0)**2
        best, best_f, history = genetic_algorithm(
            f, [(-10.0, 10.0), (-10.0, 10.0)], pop_size=30, n_gen=50
        )
        # Best fitness should be near 0 (at optimum)
        assert best_f > -1.0
        # History should be non-decreasing
        fitnesses = [h["best_f"] for h in history]
        assert fitnesses[-1] >= fitnesses[0]

    def test_converges_to_optimum(self):
        def f(x):
            return -((x[0] - 5.0)**2 + (x[1] - 2.0)**2)
        best, best_f, _ = genetic_algorithm(
            f, [(-10.0, 10.0), (-10.0, 10.0)], pop_size=50, n_gen=100
        )
        assert abs(best[0] - 5.0) < 0.5
        assert abs(best[1] - 2.0) < 0.5


# ===== Test 31: Bayesian Optimization =====
@pytest.mark.ai
class TestBayesianOptimization:
    """Test 31: Bayesian converges toward optimum."""

    def test_bayesian_converges(self):
        def f(x):
            return -((x[0] - 2.5)**2 + (x[1] - 7.0)**2)
        opt = BayesianOptimizer([(-5.0, 5.0), (-5.0, 5.0)])
        result = opt.optimize(f, n_iter=30)
        # Best found
        assert abs(result["best_x"][0] - 2.5) < 1.5
        assert abs(result["best_x"][1] - 7.0) < 1.5

    def test_bayesian_better_than_random(self):
        def f(x):
            return -((x[0] - 1.0)**2 + (x[1] - 1.0)**2)
        opt = BayesianOptimizer([(-3.0, 3.0), (-3.0, 3.0)])
        result = opt.optimize(f, n_iter=20)
        best = result["best_f"]
        np.random.seed(42)
        random_best = max(-((x - 1.0)**2 + (y - 1.0)**2)
                         for x, y in zip(np.random.uniform(-3.0, 3.0, 20),
                                        np.random.uniform(-3.0, 3.0, 20)))
        assert best >= random_best * 0.9


# ===== Test 32: Neural Surrogate =====
@pytest.mark.ai
class TestNeuralSurrogate:
    """Test 32: ML prediction vs simulation < 5% error."""

    def test_surrogate_accuracy(self):
        from core.mathematics.digital_twin.pinn import PINN
        # Train on a simple function: y = sin(x) + 0.1*x
        x_data = np.linspace(-3.0, 3.0, 50).reshape(-1, 1)
        y_data = np.sin(x_data) + 0.1 * x_data

        pinn = PINN([1, 16, 16, 1], seed=42)
        
        # Train
        pinn.train(x_data, y_data, epochs=1000, lr=0.01)
        
        # Predict
        y_pred = pinn.predict(x_data)
        
        # Calculate mean absolute relative error
        error = np.mean(np.abs(y_pred - y_data)) / (np.max(y_data) - np.min(y_data))
        assert error < 0.05
