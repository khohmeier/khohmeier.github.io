# FROM THE LECTURE NOTES, LECT07-09: For an over-sampled DCT matrix, the larger F is, the more coherent the matrix.
# We compute coherence using the mutual coherence formula defined in LECT07-09.
import numpy as np
import matplotlib.pyplot as plt


np.random.seed(1)


def gen_A(M, N, F):
  """Generates a random DCT matrix of size M x N with F coefficients.
  
  Args:
    M (int): Number of rows in the matrix.
    N (int): Number of columns in the matrix.
    F (int): Number of coefficients in the matrix.
  
  Returns:
    A (np.ndarray): DCT matrix of size M x N with F coefficients."""
  w = np.random.randn(M, 1)
  A = np.zeros((M, N))

  # generate the over complete DCT matrix
  for j in range(1, N):
    for i in range(1, M):
      A[i, j] = (1 / np.sqrt(N)) * np.cos(2 * np.pi * j * w[i, 0] / F)
  return A


def soft_thresholding(v, kappa):
  """Performs soft thresholding on a vector as a helper function to l1_admm.
  
  Args:
    v (np.ndarray): A vector.
    kappa (float): Thresholding parameter.
  
  Returns:
    v_thresh (np.ndarray): Thresholded vector.""" ""
  return np.maximum(0, v - kappa) - np.maximum(0, -v - kappa)


def shrinkL1L2(y, lamb, alpha):
  """Performs L1-L2 shrinkage on a vector.
  
  Args:
    y (np.ndarray): A vector.
    lamb (float): Regularization parameter.
    alpha (float): Thresholding parameter.

  Returns:
    x (np.ndarray): Thresholded vector.""" ""
  x = np.zeros(np.size(y))
  if max(np.abs(y)) > lamb:
    x = np.maximum(0, np.abs(y) - lamb) * np.sign(y)
    x = x * (np.linalg.norm(x) + alpha * lamb) / (np.linalg.norm(x))
  elif max(np.abs(y)) >= (1 - alpha) * lamb:
    idx = np.abs(y).argmax()
    x[idx] = (np.abs(y[idx]) + (alpha - 1) * lamb) * np.sign(y[idx])
  return x


def l1_admm(A,
            b,
            lam,
            rho,
            max_iter,
            tol=None,
            x_true=None,
            x=None,
            y=None,
            u=None):
  """Solves L1 minimization using Alternating Direction of Multipliers (ADMM).
  
  Args:
    A (np.ndarray): DCT matrix.
    b (np.ndarray): Right-hand side vector.
    lam (float): Regularization parameter.
    rho (float): ADMM parameter.
    max_iter (int): Maximum number of iterations.
    tol (float): Tolerance.
    x_true (np.ndarray): Ground truth solution.
    x (np.ndarray): Current estimate.
    z (np.ndarray): Current dual variable.
    u (np.ndarray): Current primal variable.
  
  Returns:
    x (np.ndarray): Solution.
    k + 1 (int): Number of iterations used to reach solution.
    history (dict): Dictionary containing information collected at each iteration of ADMM."""
  # Initialize variables if not provided
  if x is None:
    x = np.zeros(A.shape[1])
  if y is None:
    y = np.zeros(A.shape[1])
  if u is None:
    u = np.zeros(A.shape[1])
  history = {'residual': [], 'rel_error': [], 'error_gt': [], 'objval': []}
  for k in range(max_iter):
    v = y - (u / rho)
    x_old = np.copy(x)
    x = soft_thresholding(v, lam /
                          rho)  # divide lam by rho for correct thresholding
    y = np.linalg.inv(A.T @ A + rho * np.eye(N)) @ (
        A.T @ b + rho * x + u
    )  # matrix inversion term was missing '@' for matrix multiplication
    u = u + rho * (x - y)
    # residual & error computations
    residual = np.linalg.norm(A @ x - b)
    if np.linalg.norm(x) > 0:
      rel_error = np.linalg.norm(x - x_old) / np.linalg.norm(x)
    else:
      rel_error = None
    if x_true is not None:
      error_gt = np.linalg.norm(x - x_true) / np.linalg.norm(x_true)
    else:
      error_gt = None
    history['objval'].append((np.linalg.norm(A @ x - b),1))
    history['residual'].append(residual)
    history['rel_error'].append(rel_error)
    if tol is not None and x_true is not None and (np.linalg.norm(x - x_true) <
                                                   tol):
      break
  return x, k + 1, history


def admm_l1_l2(A, b, lamb, alpha, rho, num_iters, tol=None, x_true=None):
  """Solves L1 - L2 minimization using Alternating Direction of Multipliers (ADMM).
  
  Args:
    A (np.ndarray): DCT matrix.
    b (np.ndarray): Right-hand side vector.
    lam (float): Regularization parameter.
    alpha (float): ADMM parameter.
    rho (float): ADMM parameter.
    num_iters (int): Maximum number of iterations.
    tol (float): Tolerance.
    x_true (np.ndarray): Ground truth solution.

  Returns:
    x (np.ndarray): Solution.
    k + 1 (int): Number of iterations used to reach solution.
    history (dict): Dictionary containing information collected at each iteration of ADMM."""
  x = np.zeros(A.shape[1])
  y = np.zeros(A.shape[1])
  u = np.zeros(A.shape[1])
  # Precompute to save computational effort
  Atb = A.T @ b
  AAt = A.T @ A
  # Cholesky decomposition of (A^TA + rho*I) for faster inversion
  L = np.linalg.cholesky(AAt + rho * np.eye(A.shape[1]))
  history = {'residual': [], 'rel_error': [], 'error_gt': [], 'objval': []}
  for k in range(num_iters):
    # x-update (using the previously computed Cholesky decomposition)
    xold = np.copy(x)
    x = shrinkL1L2(y - u, lamb / rho, alpha)
    # y-update
    rhs = Atb + rho * (x + u)
    y = np.linalg.solve(L.T, np.linalg.solve(L, rhs))
    # u-update
    u = u + x - y
    # stop conditions and outputs
    residual = np.linalg.norm(A @ x - b) / np.linalg.norm(b)
    if np.linalg.norm(x) > 0:
      rel_error = np.linalg.norm(x - xold) / np.linalg.norm(x)
    else:
      rel_error = None
    if x_true is not None:
      error_gt = np.linalg.norm(x - x_true) / np.linalg.norm(x_true)
    else:
      error_gt = None
    if x_true is not None:
      error_gt = np.linalg.norm(x_true - x) / np.linalg.norm(x_true)
    if tol is not None and x_true is not None and (np.linalg.norm(x - x_true) <
                                                   tol):
      break
    history['objval'].append(np.linalg.norm(x, 1) / np.linalg.norm(x, 2))
    history['rel_error'].append(rel_error)
    history['error_gt'].append(error_gt)
    history['residual'].append(residual)
  return x, k + 1, history


def admml1ratiol2(A, b, rho_one, rho_two, num_iters, tol=None, x_true=None):
  x = np.random.normal(0, 1, A.shape[1])
  y = np.random.normal(0, 1, A.shape[1])
  v = np.random.normal(0, 1, A.shape[1])
  w = np.random.normal(0, 1, A.shape[1])
  u = np.random.normal(0, 1, A.shape[1])
  e = np.random.normal(0, 1, A.shape[1])
  #f = np.zeros(A.shape[1])
  #eta = 0
  history = {'residual': [], 'rel_error': [], 'error_gt': [], 'objval': []}
  for k in range(num_iters):
    f = (rho_one / (rho_one + rho_two)) * (y - (1 / rho_one) * v) + (
        rho_two / (rho_one + rho_two)) * (u - (1 / rho_two) * w)
    #small_id = 1e-5 * np.eye(A.shape[0])
    x = (np.eye(A.shape[1]) - A.T @ np.linalg.pinv(A @ A.T) @ A
         ) @ f + A.T @ np.linalg.pinv(A @ A.T) @ b
    d = x + (v / rho_one)
    eta = np.linalg.norm(d, 2)
    c = np.linalg.norm(u, 1)
    D = c / (rho_one * eta**3)
    C = ((27 * D + 2 + np.sqrt(27 * D + 2)**2 - 2) / 2)**(1 / 3)
    tau = (1 / 3) + (1 / 3) * (C + (1 / C))
    if d.all() == 0:
      y = e
    else:
      y = tau * d
    u = np.max(
        np.abs(x + (w / rho_two)) - 1 /
        (rho_two * np.linalg.norm(y, 2)), 0) * np.sign(x + (w / rho_two))
    v = v + rho_one * (x - y)
    w = w + rho_two * (x - u)

    # stop conditions and outputs
    residual = np.linalg.norm(A @ x - b) / np.linalg.norm(b)
    if np.linalg.norm(x) > 0:
      rel_error = np.linalg.norm(x - x_true) / np.linalg.norm(x)
      if x_true is not None:
        error_gt = np.linalg.norm(x - x_true) / np.linalg.norm(x_true)
      #error_gt = np.linalg.norm(x_true - x) / np.linalg.norm(x_true)
    else:
      error_gt = None
      rel_error = None
    if tol is not None and x_true is not None and (np.linalg.norm(x - x_true) <
                                                   tol):
      break
    #history['objval'].append(soft_thresholding(A @ x - b, lamb / rho).sum())
    history['rel_error'].append(rel_error)
    history['error_gt'].append(error_gt)
    history['residual'].append(residual)
  return x, k + 1, history


# Parameters
M = 250
N = 500
rho = 5  # Penalty parameter for ADMM
lam = 1e-4  # Weight of the L1 norm term in the objective
max_iter = N  # Maximum number of iterations
abstol = 1e-3  # Absolute tolerance
alpha = 1e-3  # Weight of the L2 norm term in the objective
rho_one = 1
rho_two = 1
F_low = 1
F_med = 10
F_high = 50
A_lowF = gen_A(M, N, F_low)
A_medF = gen_A(M, N, F_med)
A_highF = gen_A(M, N, F_high)

# Problem setup - generate ground truth xg and b (with noise)
xg = np.zeros(N)
s = 25
indices = np.random.choice(np.arange(N), replace=False,
                           size=s)  # select 's' random indices
xg[indices] = np.random.uniform(low=0.01, high=0.05,
                                size=s)  # assign small, random non-zero values
b_lowF = np.matmul(A_lowF, xg)  # Example measurement vector b, using low F A
b_lowF = b_lowF + 0.01 * np.random.normal(0, 1, b_lowF.shape)
b_medF = np.matmul(A_medF, xg)
b_medF = b_medF + 0.01 * np.random.normal(0, 1, b_medF.shape)
b_highF = np.matmul(A_highF,
                    xg)  # Example measurement vector b, using high F A
b_highF = b_highF + 0.01 * np.random.normal(0, 1, b_highF.shape)

# Call the ADMM solver
# Low F/low coherence first
x_admm_lowF, iters_admm_lowF, hist_admm_lowF = l1_admm(A_lowF,
                                                       b_lowF,
                                                       lam,
                                                       rho,
                                                       max_iter,
                                                       abstol,
                                                       x_true=xg)
print(x_admm_lowF)
# Med F/med coherence
x_admm_medF, iters_admm_medF, hist_admm_medF = l1_admm(A_medF,
                                                       b_medF,
                                                       lam,
                                                       rho,
                                                       max_iter,
                                                       abstol,
                                                       x_true=xg)
print(x_admm_medF)
# High F/high coherence
x_admm_highF, iters_admm_highF, hist_admm_highF = l1_admm(A_highF,
                                                          b_highF,
                                                          lam,
                                                          rho,
                                                          max_iter,
                                                          abstol,
                                                          x_true=xg)
print(x_admm_highF)

# Plotting the relative error
plt.figure()
plt.plot(hist_admm_lowF['rel_error'], label="low F")
plt.plot(hist_admm_medF['rel_error'], label="med F")
plt.plot(hist_admm_highF['rel_error'], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Relative Error')
plt.yscale("log")
plt.title('L1 ADMM Relative Error')
plt.show()
# Plotting the residuals
plt.figure()
plt.plot(hist_admm_lowF['residual'], label="low F")
plt.plot(hist_admm_medF['residual'], label="med F")
plt.plot(hist_admm_highF['residual'], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Residual')
plt.yscale("log")
plt.title('L1 ADMM Residual')
plt.show()
# Plotting the error to ground truth
plt.figure()
plt.plot(hist_admm_lowF["error_gt"], label="low F")
plt.plot(hist_admm_medF["error_gt"], label="med F")
plt.plot(hist_admm_highF["error_gt"], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Error to Ground Truth')
plt.yscale("log")
plt.title('L1 ADMM Error to Ground Truth')
plt.show()
# Plotting the objective value
plt.figure()
plt.plot(hist_admm_lowF['objval'], label="low F")
plt.plot(hist_admm_medF['objval'], label="med F")
plt.plot(hist_admm_highF['objval'], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Error to Ground Truth')
plt.yscale("log")
plt.title('L1 ADMM Error to Ground Truth')
plt.show()

# implement ADMM for low F A
x_l1l2_lowF, iters_l1l2_lowF, hist_l1l2_lowF = admm_l1_l2(A_lowF,
                                                          b_lowF,
                                                          lam,
                                                          alpha,
                                                          rho,
                                                          max_iter,
                                                          abstol,
                                                          x_true=xg)
print(x_l1l2_lowF)
# implement ADMM for med F A
x_l1l2_medF, iters_l1l2_medF, hist_l1l2_medF = admm_l1_l2(A_medF,
                                                          b_medF,
                                                          lam,
                                                          alpha,
                                                          rho,
                                                          max_iter,
                                                          abstol,
                                                          x_true=xg)
print(x_l1l2_medF)
# implement ADMM for high F A
x_l1l2_highF, iters_l1l2_highF, hist_l1l2_highF = admm_l1_l2(A_highF,
                                                             b_highF,
                                                             lam,
                                                             alpha,
                                                             rho,
                                                             max_iter,
                                                             abstol,
                                                             x_true=xg)
print(x_l1l2_highF)

# Plotting the relative error
plt.figure()
plt.plot(hist_l1l2_lowF['rel_error'], label="low F")
plt.plot(hist_l1l2_medF['rel_error'], label="med F")
plt.plot(hist_l1l2_highF['rel_error'], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Relative Error')
plt.yscale("log")
plt.title('L1-L2 ADMM Relative Error')
plt.show()
# Plotting the residuals
plt.figure()
plt.plot(hist_l1l2_lowF['residual'], label="low F")
plt.plot(hist_l1l2_medF['residual'], label="med F")
plt.plot(hist_l1l2_highF['residual'], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Residual')
plt.yscale("log")
plt.title('L1-L2 ADMM Residual')
plt.show()
# Plotting the error to ground truth
plt.figure()
plt.plot(hist_l1l2_lowF["error_gt"], label="low F")
plt.plot(hist_l1l2_medF["error_gt"], label="med F")
plt.plot(hist_l1l2_highF["error_gt"], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Error to Ground Truth')
plt.yscale("log")
plt.title('L1-L2 ADMM Error to Ground Truth')
plt.show()
# Plotting the objective value
plt.figure()
plt.plot(hist_l1l2_lowF['objval'], label="low F")
plt.plot(hist_l1l2_medF['objval'], label="med F")
plt.plot(hist_l1l2_highF['objval'], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Objective Value')
plt.yscale("log")
plt.title('L1-L2 ADMM Objective Value')
plt.show()

x_admml1dl2_lowF, iters_admml1dl2_lowF, hist_admml1dl2_lowF = admml1ratiol2(
    A_lowF, b_lowF, rho_one, rho_two, max_iter, abstol, x_true=xg)
print(x_admml1dl2_lowF)
# Med F/med coherence
x_admml1dl2_medF, iters_admml1dl2_medF, hist_admml1dl2_medF = admml1ratiol2(
    A_medF, b_medF, rho_one, rho_two, max_iter, abstol, x_true=xg)
print(x_admml1dl2_medF)
# High F/high coherence
x_admml1dl2_highF, iters_admml1dl2_highF, hist_admml1dl2_highF = admml1ratiol2(
    A_highF, b_highF, rho_one, rho_two, max_iter, abstol, x_true=xg)
print(x_admml1dl2_highF)

# Plotting the relative error
plt.figure()
plt.plot(hist_admml1dl2_lowF['rel_error'], label="low F")
plt.plot(hist_admml1dl2_medF['rel_error'], label="med F")
plt.plot(hist_admml1dl2_highF['rel_error'], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Relative Error')
plt.yscale("log")
plt.title('L1-L2 ADMM Relative Error')
plt.show()
# Plotting the residuals
plt.figure()
plt.plot(hist_admml1dl2_lowF['residual'], label="low F")
plt.plot(hist_admml1dl2_medF['residual'], label="med F")
plt.plot(hist_admml1dl2_highF['residual'], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Residual')
plt.yscale("log")
plt.title('L1-L2 ADMM Residual')
plt.show()
# Plotting the error to ground truth
plt.figure()
plt.plot(hist_admml1dl2_lowF["error_gt"], label="low F")
plt.plot(hist_admml1dl2_medF["error_gt"], label="med F")
plt.plot(hist_admml1dl2_highF["error_gt"], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Error to Ground Truth')
plt.yscale("log")
plt.title('L1-L2 ADMM Error to Ground Truth')
plt.show()

# Plotting the objective value
plt.figure()
plt.plot(hist_admml1dl2_lowF['objval'], label="low F")
plt.plot(hist_admml1dl2_medF['objval'], label="med F")
plt.plot(hist_admml1dl2_highF['objval'], label="high F")
plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Objective Value')
plt.yscale("log")
plt.title('L1-L2 ADMM Objective Value')
plt.show()

# PLOT ALL MODELS TOGETHER #
# Create a single figure with subplots arranged in 1 row and 3 columns
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
# Low Coherence plots
axs[0].plot(hist_admm_lowF['residual'], label="ADMM low F")
axs[0].plot(hist_l1l2_lowF['residual'], label="L1L2 low F")
axs[0].plot(hist_admml1dl2_lowF['residual'], label="ADMM L1-DL2 low F")
axs[0].set_title('Low Coherence')
axs[0].set_xlabel('Iteration')
axs[0].set_ylabel('Residual')
axs[0].set_yscale("log")
axs[0].legend()
# Med Coherence plots
axs[1].plot(hist_admm_medF['residual'], label="ADMM med F")
axs[1].plot(hist_l1l2_medF['residual'], label="L1L2 med F")
axs[1].plot(hist_admml1dl2_medF['residual'], label="ADMM L1-DL2 med F")
axs[1].set_title('Medium Coherence')
axs[1].set_xlabel('Iteration')
axs[1].set_ylabel('Residual')
axs[1].set_yscale("log")
axs[1].legend()
# High Coherence plots
axs[2].plot(hist_admm_highF['residual'], label="ADMM high F")
axs[2].plot(hist_l1l2_highF['residual'], label="L1L2 high F")
axs[2].plot(hist_admml1dl2_highF['residual'], label="ADMM L1-DL2 high F")
axs[2].set_title('High Coherence')
axs[2].set_xlabel('Iteration')
axs[2].set_ylabel('Residual')
axs[2].set_yscale("log")
axs[2].legend()
# Show the figure
plt.show()
