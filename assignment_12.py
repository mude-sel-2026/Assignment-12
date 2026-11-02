# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 19:43:41 2026

@author: 736su
"""
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# TASK 1: Load dataset and plot the data
# ============================================================

def task1_load_and_plot():
    ## TODO: Load the dataset and extract the curing-age (ca) and strength (fc) arrays.
    data = np.load()

    ca = data[]
    fc = data[]

    print("\n========== TASK 1 ==========")
    print("Total number of samples:", len(ca))
    print("Curing age range:", ca.min(), "to", ca.max(), "days")
    print("Concrete strength range:", round(fc.min(), 3),
          "to", round(fc.max(), 3), "MPa")

    ## TODO: Plot curing age against concrete compressive strength and label the axes.
    plt.figure(figsize=(8, 5))
    plt.scatter()
    plt.xlabel("Curing age (days)")
    plt.ylabel("Concrete compressive strength (MPa)")
    plt.title("Curing Age vs Concrete Compressive Strength")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    return ca, fc


# ============================================================
# TASK 2: Split the dataset into training, validation and test
# ============================================================

def task2_split_data(ca, fc):
    print("\n========== TASK 2 ==========")

    # Random permutation with seed 2.
    rng = np.random.default_rng(2)
    indices = rng.permutation(len(ca))
    
    ## TODO: Calculate the number of training (70%) and validation (10%) samples.
    n = len()
    n_train = int()
    n_val = int()
    
    ## TODO: Insert appropriate indices to split into training, validation, and test data.
    train_idx = indices[]
    val_idx = indices[]
    test_idx = indices[]
    
    ca_train = ca[train_idx]
    fc_train = fc[train_idx]

    ca_val = ca[val_idx]
    fc_val = fc[val_idx]

    ca_test = ca[test_idx]
    fc_test = fc[test_idx]

    print("Training samples:", len(ca_train))
    print("Validation samples:", len(ca_val))
    print("Testing samples:", len(ca_test))
    print("Total samples:", len(ca_train) + len(ca_val) + len(ca_test))

    return (
        ca_train, fc_train,
        ca_val, fc_val,
        ca_test, fc_test
    )


# ============================================================
# TASK 3: Define the polynomial models and initial parameters
# ============================================================

def task3_initialize_models():
    print("\n========== TASK 3 ==========")
    
    ## TODO: Define initial_learning_rate, initial_model_size and initial_epochs as 0.01, 2, 5000
    initial_learning_rate = 
    initial_model_size =
    initial_epochs = 
    
    ## TODO: Define model_sizes as the three prescribed sizes: 2, 3, and 4.
    model_sizes = []

    print("Model size 2: fc = C1 + C2*ca")
    print("Model size 3: fc = C1 + C2*ca + C3*ca^2")
    print("Model size 4: fc = C1 + C2*ca + C3*ca^2 + C4*ca^3")

    print("\nInitial learning rate:", initial_learning_rate)
    print("Initial model size:", initial_model_size)
    print("Initial number of epochs:", initial_epochs)

    return (
        initial_learning_rate,
        initial_model_size,
        initial_epochs,
        model_sizes
    )

# ============================================================
# TASK 4: Implement gradient descent analytically
# ============================================================

def task4_gradient_descent(X, y, learning_rate, epochs):
    """
    Minimize MSE using batch gradient descent.

    Prediction:
        y_pred = X @ theta

    Loss:
        MSE = (1/n) * sum((y_pred - y)^2)

    Analytical gradient:
        gradient = (2/n) * X.T @ (y_pred - y)

    Parameter update:
        theta = theta - learning_rate * gradient
    """

    n_samples, n_parameters = X.shape
    training_loss = []
    theta = np.zeros(n_parameters, dtype=float)
    
    for epoch in range(epochs):

        ## TODO: Predict y, and calculate the MSE
        y_pred = 
        error = y_pred - y
        mse =
        
        training_loss.append(mse)
        
        ## TODO: Calculate the analytical gradient of MSE with respect to theta.
        gradient = 
        
        ## TODO: Update theta using the learning rate and calculated gradient.
        theta = 
        
        # Stop if the calculations become numerically unstable.
        if not np.all(np.isfinite(theta)):
            raise FloatingPointError(
                "Gradient descent diverged. Reduce the learning rate."
            )

    return theta, np.asarray(training_loss)


# ============================================================
# TASK 5: Train the initial model and evaluate validation loss
# ============================================================

def task5_train_initial_model(
    ca_train, fc_train,
    ca_val, fc_val,
    learning_rate, model_size, epochs
):
    print("\n========== TASK 5 ==========")

    # Normalize using training data only.
    x_train, y_train, x_scale, y_mean, y_std = (
        prepare_training_data(ca_train, fc_train)
    )

    X_train = create_design_matrix(x_train, model_size)

    theta, training_loss = task4_gradient_descent(
        X_train, y_train, learning_rate, epochs
    )

    # Predict training and validation strengths in MPa.
    fc_train_pred = predict_strength(
        ca_train, theta, model_size, x_scale, y_mean, y_std
    )

    fc_val_pred = predict_strength(
        ca_val, theta, model_size, x_scale, y_mean, y_std
    )

    train_mse = calculate_mse(fc_train, fc_train_pred)
    val_mse = calculate_mse(fc_val, fc_val_pred)
    val_rmse = np.sqrt(val_mse)

    print("Initial learning rate:", learning_rate)
    print("Initial model size:", model_size)
    print("Number of epochs:", epochs)

    print("Training MSE (MPa^2):", round(train_mse, 6))
    print("Validation MSE (MPa^2):", round(val_mse, 6))
    print("Validation RMSE (MPa):", round(val_rmse, 6))

    # Plot training loss.
    plt.figure(figsize=(8, 5))
    ## TODO: Plot the loss vs number of epochs
    plt.plot()
    plt.xlabel("Epoch")
    plt.ylabel("Training MSE (standardized target)")
    plt.title("Task 5: Training Loss vs Epoch")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return theta, training_loss


# ============================================================
# TASK 6: Tune learning rate and model size
# ============================================================

def task6_hyperparameter_tuning(
    ca_train, fc_train,
    ca_val, fc_val,
    epochs
):
    print("\n========== TASK 6 ==========")

    ## TODO: Define three learning rates to test (three rates x three model sizes = nine combinations).
    learning_rates = []
    model_sizes = []
    
    results = []

    for model_size in model_sizes:

        # Use the same training-only scaling for all combinations.
        x_train, y_train, x_scale, y_mean, y_std = (
            prepare_training_data(ca_train, fc_train)
        )

        X_train = create_design_matrix(x_train, model_size)

        for learning_rate in learning_rates:

            try:
                theta, training_loss = task4_gradient_descent(
                    X_train,
                    y_train,
                    learning_rate,
                    epochs
                )

                # Predict training set.
                fc_train_pred = predict_strength(
                    ca_train,
                    theta,
                    model_size,
                    x_scale,
                    y_mean,
                    y_std
                )

                # Predict validation set.
                fc_val_pred = predict_strength(
                    ca_val,
                    theta,
                    model_size,
                    x_scale,
                    y_mean,
                    y_std
                )

                train_mse = calculate_mse(fc_train, fc_train_pred)
                val_mse = calculate_mse(fc_val, fc_val_pred)

                results.append({
                    "learning_rate": learning_rate,
                    "model_size": model_size,
                    "train_mse": train_mse,
                    "val_mse": val_mse,
                    "theta": theta,
                    "x_scale": x_scale,
                    "y_mean": y_mean,
                    "y_std": y_std
                })

            except FloatingPointError:
                print(
                    "Divergence detected for learning rate",
                    learning_rate,
                    "and model size",
                    model_size
                )

    if len(results) == 0:
        raise RuntimeError(
            "All configurations diverged. Reduce the learning rates."
        )

    # Display the results.
    print("\nHyperparameter comparison:")
    print("-" * 10)

    print(
        f"{'Learning Rate':<18}"
        f"{'Model Size':<14}"
        f"{'Training MSE':<20}"
        f"{'Validation MSE':<20}"
    )

    print("-" * 10)

    for result in results:
        print(
            f"{result['learning_rate']:<18.4f}"
            f"{result['model_size']:<14}"
            f"{result['train_mse']:<20.6f}"
            f"{result['val_mse']:<20.6f}"
        )

    print("-" * 10)

    results.sort(key=lambda result: result["val_mse"])
    best_model = results[0]
    
    print("\nBest configuration:")
    print("Learning rate:", best_model["learning_rate"])
    print("Model size:", best_model["model_size"])
    print("Training MSE:", round(best_model["train_mse"], 6))
    print("Validation MSE:", round(best_model["val_mse"], 6))

    return best_model, results


# ============================================================
# TASK 7: Evaluate the selected model on the test set
# ============================================================

def task7_test_evaluation(
    ca_test, fc_test, best_model
):
    print("\n========== TASK 7 ==========")

    # Retrieve the selected configuration.
    theta = best_model["theta"]
    model_size = best_model["model_size"]
    x_scale = best_model["x_scale"]
    y_mean = best_model["y_mean"]
    y_std = best_model["y_std"]

    # Predict test-set strengths.
    fc_test_pred = predict_strength(
        ca_test,
        theta,
        model_size,
        x_scale,
        y_mean,
        y_std
    )

    ## TODO: Calculate test MSE, and MAE in the original MPa units.
    test_mse = 
    test_rmse = 
    test_mae =
    
    print("Selected learning rate:", best_model["learning_rate"])
    print("Selected model size:", model_size)

    print("\nTest-set performance:")
    print("Test MSE (MPa^2):", round(test_mse, 6))
    print("Test RMSE (MPa):", round(test_rmse, 6))
    print("Test MAE (MPa):", round(test_mae, 6))

    plt.figure(figsize=(7,7))
    ## TODO: Plot measured versus predicted test strengths.
    plt.scatter()
    
    lower = min(fc_test.min(), fc_test_pred.min())
    upper = max(fc_test.max(), fc_test_pred.max())
    
    ## TODO: Plot the ideal y = x line using lower and upper values calculated above.
    plt.plot()
    plt.xlabel("Measured Strength (MPa)")
    plt.ylabel("Predicted Strength (MPa)")
    plt.title("Measured vs Predicted Concrete Strength")
    plt.legend()
    plt.grid(True)
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

    return test_mse, test_rmse, test_mae


# ============================================================
# Helper function: Normalize and prepare the training data
# ============================================================

def prepare_training_data(ca_train, fc_train):

    x_scale = np.max(np.abs(ca_train))

    if x_scale == 0:
        x_scale = 1.0

    y_mean = np.mean(fc_train)
    y_std = np.std(fc_train)

    if y_std == 0:
        y_std = 1.0

    x_train = ca_train / x_scale
    y_train = (fc_train - y_mean) / y_std

    return x_train, y_train, x_scale, y_mean, y_std


# ============================================================
# Helper function: Predict in the original MPa units
# ============================================================

def predict_strength(ca, theta, model_size, x_scale, y_mean, y_std):
    x = np.asarray(ca, dtype=float) / x_scale

    X = create_design_matrix(x, model_size)

    # Prediction in standardized target units.
    y_pred_standardized = X @ theta

    # Convert predictions back to MPa.
    fc_pred = y_pred_standardized * y_std + y_mean

    return fc_pred


# ============================================================
# Helper function: Construct the polynomial design matrix
# ============================================================

def create_design_matrix(x, model_size):
    """
    Model size 2: y = C1 + C2*x
    Model size 3: y = C1 + C2*x + C3*x^2
    Model size 4: y = C1 + C2*x + C3*x^2 + C4*x^3
    """

    x = np.asarray(x, dtype=float).reshape(-1)

    X = np.column_stack([
        x ** power for power in range(model_size)
    ])

    return X

# ============================================================
# Helper function: Calculate mean squared error
# ============================================================

def calculate_mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# ============================================================
# MAIN: Call all seven task functions
# ============================================================

if __name__ == "__main__":
    # Task 1: Load the dataset and plot the data.
    ca, fc = task1_load_and_plot()

    # Task 2: Split the dataset.
    (
        ca_train, fc_train,
        ca_val, fc_val,
        ca_test, fc_test
    ) = task2_split_data(ca, fc)

    # Task 3: Define initial hyperparameters and model sizes.
    (
        initial_learning_rate,
        initial_model_size,
        initial_epochs,
        model_sizes
    ) = task3_initialize_models()

    # Task 4: The analytical gradient descent implementation
    # is defined in task4_gradient_descent().
    # It is called by the training functions in Tasks 5 and 6.

    # Task 5: Train the initial model.
    task5_train_initial_model(
        ca_train, fc_train,
        ca_val, fc_val,
        initial_learning_rate,
        initial_model_size,
        initial_epochs
    )

    # Task 6: Tune hyperparameters using validation MSE.
    best_model, results = task6_hyperparameter_tuning(
        ca_train, fc_train,
        ca_val, fc_val,
        initial_epochs
    )

    # Task 7: Evaluate the selected configuration on test data.
    task7_test_evaluation(
        ca_test, fc_test, best_model
    )