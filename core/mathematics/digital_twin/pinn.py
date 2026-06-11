import numpy as np
from typing import Callable

def pinn_loss(pred_values: np.ndarray, true_values: np.ndarray,
              ode_residual: float, physics_weight: float = 0.5) -> float:
    mse_data = np.mean((pred_values - true_values)**2)
    return float(mse_data + physics_weight * (ode_residual**2))

class PINN:
    def __init__(self, layers: list[int], seed: int = 42):
        np.random.seed(seed)
        self.layers = layers
        self.weights = []
        self.biases = []
        
        # Xavier initialization
        for i in range(len(layers) - 1):
            w = np.random.normal(0.0, np.sqrt(2.0 / (layers[i] + layers[i+1])), (layers[i], layers[i+1]))
            b = np.zeros((1, layers[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def forward(self, X: np.ndarray) -> tuple[list[np.ndarray], list[np.ndarray]]:
        a = X
        activations = [a]
        zs = []
        for i in range(len(self.weights) - 1):
            z = a @ self.weights[i] + self.biases[i]
            zs.append(z)
            a = np.tanh(z)
            activations.append(a)
        # Output layer with linear activation
        z = a @ self.weights[-1] + self.biases[-1]
        zs.append(z)
        activations.append(z)
        return activations, zs

    def predict(self, X: np.ndarray) -> np.ndarray:
        activations, _ = self.forward(X)
        return activations[-1]

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 1500, lr: float = 0.01,
              physics_residual_fn: Callable[[np.ndarray, np.ndarray], np.ndarray] = None,
              physics_weight: float = 0.1):
        # Adam optimizer parameters
        beta1, beta2 = 0.9, 0.999
        eps = 1e-8
        
        mW = [np.zeros_like(w) for w in self.weights]
        vW = [np.zeros_like(w) for w in self.weights]
        mb = [np.zeros_like(b) for b in self.biases]
        vb = [np.zeros_like(b) for b in self.biases]
        
        t = 0
        for epoch in range(epochs):
            activations, zs = self.forward(X)
            y_pred = activations[-1]
            
            # Loss and derivatives
            loss_data = y_pred - y
            
            # Backpropagation
            # Output layer delta
            delta = loss_data
            
            dW = []
            db = []
            
            # Gradients for weights/biases
            for i in reversed(range(len(self.weights))):
                dw = activations[i].T @ delta
                pdb = np.sum(delta, axis=0, keepdims=True)
                dW.insert(0, dw)
                db.insert(0, pdb)
                if i > 0:
                    # Derivative of tanh: 1 - tanh^2
                    dtanh = 1.0 - activations[i]**2
                    delta = (delta @ self.weights[i].T) * dtanh
            
            # Update weights & biases using Adam
            t += 1
            for i in range(len(self.weights)):
                mW[i] = beta1 * mW[i] + (1.0 - beta1) * dW[i]
                vW[i] = beta2 * vW[i] + (1.0 - beta2) * (dW[i]**2)
                
                mb[i] = beta1 * mb[i] + (1.0 - beta1) * db[i]
                vb[i] = beta2 * vb[i] + (1.0 - beta2) * (db[i]**2)
                
                mWh = mW[i] / (1.0 - beta1**t)
                vWh = vW[i] / (1.0 - beta2**t)
                mbh = mb[i] / (1.0 - beta1**t)
                vbh = vb[i] / (1.0 - beta2**t)
                
                self.weights[i] -= lr * mWh / (np.sqrt(vWh) + eps)
                self.biases[i] -= lr * mbh / (np.sqrt(vbh) + eps)
