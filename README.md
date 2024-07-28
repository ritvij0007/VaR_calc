# Value-at-Risk Estimation and Backtesting

In this project, we aim to estimate the Value-at-Risk (VaR) for a portfolio consisting of two stocks, Microsoft (MSFT) and Apple (AAPL). We will use various models to calculate the VaR and backtest these models to measure their accuracy. Our goal is to identify the model that leads to the lowest capital requirement while accurately predicting risk.

## Problem Statement

We are given daily adjusted close price data for two stocks, Microsoft (MSFT) and Apple (AAPL). The portfolio consists of 50 shares of each stock. Our task is to:

1. **Calculate daily 99% VaR** for the portfolio using different models.
2. **Backtest** the calculated VaR values over the past year to measure the number of exceedances (instances where the actual loss exceeds the predicted VaR).
3. **Determine the capital requirement** for the portfolio using the formula:

$C = \max[\text{VaR}_{t-1}, m \times \text{VaR}_{\text{avg}}]$

where \( m \) is a factor based on the number of exceedances.

## VaR Models

We will use the following models to estimate VaR, grouped into three main categories:

1. **Parametric Approach**: This approach assumes that the returns follow a particular distribution, and volatility is estimated using different models:
   - **Standard Deviation (std)**: A basic measure of volatility.
   - **Exponentially Weighted Moving Average (EWMA)**: A volatility model giving more weight to recent observations.
   - **GARCH Models**:
     - GARCH with Normal distribution (no leverage effect).
     - GARCH with Generalized Error Distribution (GED) (no leverage effect).
     - GJR-GARCH with Normal distribution (with leverage effect).
     - GJR-GARCH with GED (with leverage effect).

2. **Historical Simulation**: A non-parametric approach using historical data.

3. **Monte Carlo Simulation**: A simulation-based approach for VaR estimation.

## VaR Limits and Weights

The VaR limits and weights for the exceedance calculation are defined as follows:

| Exceedances    | m Factor |
|----------------|----------|
| Less than 5    | 1.5      |
| 5              | 1.7      |
| 6              | 1.76     |
| 7              | 1.83     |
| 8              | 1.88     |
| 9              | 1.92     |
| 10 or more     | 2.0      |


## Data and Portfolio

- The portfolio consists of 50 shares each of Microsoft (MSFT) and Apple (AAPL).
- The adjusted close price data for both stocks is stored in the data file.

In the following steps, we will implement and compare these models, calculate the VaR, perform backtesting, and determine the capital requirement for the portfolio.






## Parametric Approach for VaR Calculation

The Parametric Approach to VaR calculation assumes that the returns of the portfolio follow a particular statistical distribution. This approach estimates volatility using different models and then calculates VaR based on this estimated volatility.

### Volatility Models

1. **Standard Deviation (std)**: This model calculates the basic measure of volatility, assuming that past returns are indicative of future risk. It is simple and easy to implement but may not always be accurate for financial time series.

2. **Exponentially Weighted Moving Average (EWMA)**: This model gives more weight to recent observations, making it more responsive to recent changes in market conditions. It adjusts the volatility estimate dynamically.

3. **GARCH Models**: 
   - **GARCH with Normal distribution (no leverage effect)**: Models volatility clustering and assumes that returns follow a normal distribution.
   - **GARCH with Generalized Error Distribution (GED) (no leverage effect)**: Similar to GARCH with a normal distribution but assumes returns follow a GED, which can better capture the fat tails in return distributions.
   - **GJR-GARCH with Normal distribution (with leverage effect)**: Extends GARCH to account for leverage effects, where volatility tends to increase more after negative shocks than positive shocks.
   - **GJR-GARCH with GED (with leverage effect)**: Combines GJR-GARCH with GED to model both leverage effects and fat tails in the return distribution.

For implementing GARCH and GJR-GARCH models, we use the `arch` package in Python. For more information, refer to the [arch documentation](https://arch.readthedocs.io/).

### VaR Calculation

Once the volatility is estimated using any of the above models, the VaR is calculated using the following formula:

VaRᵢ = α × σᵢ × √h

where:
- `α` is the critical value from the standard normal distribution corresponding to the confidence level (e.g., 2.33 for 99% confidence level).
- `σᵢ` is the estimated volatility from model `i` ('std', 'ewma', 'garch_normal', 'garch_ged', 'gjr_garch_normal', 'gjr_garch_ged').
- `h` is the time horizon (typically 1 day for daily VaR).

The VaR is then adjusted based on the initial investment:

VaR_adjusted = VaRᵢ × Investmentₜ₋₁

### Volatility Calculation

Volatility (`σ`) for daily returns can be calculated using:

$\sigma = \sqrt{\frac{1}{n-1} \sum_{t=1}^{n} (r_{t} - \bar{r})^2}$


where:
- `n` is the number of observations.
- `rₜ` is the return at time `t`.
- `r̄` is the mean return.

By using the estimated volatility from each model, we can calculate the corresponding VaR for the portfolio.



## Historical Simulation for VaR Calculation

The Historical Simulation approach to VaR calculation does not assume any particular distribution for returns. Instead, it uses historical return data to estimate potential future losses based on past data.

### Historical Simulation

In Historical Simulation, the historical returns of the portfolio are directly used to estimate the distribution of future returns. This method is simple and intuitive, as it relies on actual historical data rather than making assumptions about the return distribution.

### VaR Calculation

The VaR is calculated by sorting the historical returns and finding the return at the desired confidence level. For example, to calculate the 99% VaR, we find the return at the 1st percentile of the sorted historical returns for each rolling window of 60 days.

$\text{VaR}_{\text{Historical}} = \text{Percentile}(1 - \text{confidence level})$

where:
- The confidence level is typically 99%, meaning we are interested in the 1st percentile of the returns.

The VaR is then adjusted based on the initial investment:

$\text{VaR}_{\text{Historical, adjusted}} = \text{VaR}_{\text{Historical}} \times \text{Investment}_{t-1}$

By using the historical returns, we can calculate the corresponding VaR for the portfolio without making any distributional assumptions.





## Monte Carlo Simulation for VaR Calculation

The Monte Carlo Simulation approach to VaR calculation uses random sampling to estimate potential future losses based on the statistical properties of historical return data. This method is flexible and can accommodate complex risk factors and distributions.

### Monte Carlo Simulation

In Monte Carlo Simulation, we generate a large number of possible future return scenarios based on the historical statistical properties of the returns. The steps for calculating VaR using Monte Carlo Simulation are as follows:

1. **Estimate Statistical Properties**: Calculate the mean and covariance of the historical returns over a rolling window of 60 days.

   $\mu_t = \frac{1}{n} \sum_{i=t-n+1}^{t} r_i$

   $\Sigma_t = \frac{1}{n-1} \sum_{i=t-n+1}^{t} (r_i - \mu_t)(r_i - \mu_t)^T$

2. **Generate Simulations**: Use these statistical properties to generate a large number (e.g., 1000) of possible future return scenarios.

   $r_{t+1}^i \sim \mathcal{N}(\mu_t, \Sigma_t)$

3. **Calculate Portfolio Values**: Calculate the portfolio values for each scenario.

   $P_{t+1}^i = P_t \cdot e^{r_{t+1}^i}$

4. **Determine Potential Losses**: Calculate the potential losses for each scenario by comparing the simulated portfolio values to the initial investment.

   $L_{t+1}^i = P_t - P_{t+1}^i$

5. **Calculate VaR**: Determine the VaR by finding the appropriate percentile of the distribution of potential losses.

   $\text{VaR}_{\text{Monte Carlo}} = \text{Percentile}(L_{t+1}^i, (1 - \text{confidence level}) \times 100\%)$

   where:
   - The confidence level is typically 99%, meaning we are interested in the 1st percentile of the simulated losses.
   - Rolling window is a window of time (e.g., 60 days) over which to calculate the mean and covariance.
   - $\mu_t$ is the mean return over the rolling window.
   - $\Sigma_t$ is the covariance matrix of returns over the rolling window.
   - $r_{t+1}^i$ are the simulated returns for the next period.
   - $P_t$ is the current portfolio value.
   - $P_{t+1}^i$ are the simulated portfolio values for the next period.
   - $L_{t+1}^i$ are the potential losses based on the calculated values.

The VaR is then adjusted based on the initial investment:

$\text{VaR}_{\text{Monte Carlo, adjusted}} = \text{VaR}_{\text{Monte Carlo}} \times \text{Investment}_{t-1}$

By using the simulated returns, we can calculate the corresponding VaR for the portfolio, incorporating a wide range of potential future scenarios.













# Class and Method Descriptions

### FinancialMetrics Class
A class to calculate financial metrics such as returns and portfolio volatility.

- **`__init__`**: Initializes the class with financial data.
- **`calculate_returns`**: Calculates logarithmic returns of the data.
- **`calculate_portfolio_volatility`**: Calculates portfolio volatility using different methods such as standard deviation, EWMA, and GARCH models.

### VaRCalculator Class
A class to calculate Value-at-Risk (VaR) using different methods and perform backtesting.

- **`__init__`**: Initializes the class with financial data, rolling window, and confidence level.
- **`parametric_var`**: Calculates parametric VaR using different volatility models.
- **`historical_var`**: Calculates historical VaR using historical returns data.
- **`Monte_Carlo_VaR`**: Calculates VaR using Monte Carlo simulation.
- **`backtest_var`**: Performs backtesting of VaR models to count exceedances.
- **`plot_exceedances`**: Plots VaR exceedances against actual portfolio P&L.

### VaRStatisticsCalculator Class
A class to calculate and analyze VaR statistics for a portfolio.

- **`__init__`**: Initializes the class with data path, models, rolling window, and confidence level.
- **`calculate_var`**: Calculates VaR using different models and combines them into a single DataFrame.
- **`calculate_and_plot_exceedances`**: Calculates and plots exceedances of VaR models.
- **`plot_exceedances_with_limits`**: Plots exceedances with corresponding color limits.
- **`calculate_capital_required`**: Calculates the capital required based on VaR models and exceedances.

### Parameter Tables

#### Calc of m used for calc of VaR
| Condition      | m    |
|----------------|------|
| green_less_5   | 1.5  |
| amber_5        | 1.7  |
| amber_6        | 1.76 |
| amber_7        | 1.83 |
| amber_8        | 1.88 |
| amber_9        | 1.92 |
| red_10_or_more | 2.0  |

#### Garch model used with parameters
| vol   | dist   | o |
|-------|--------|---|
| Garch | normal | 0 |
| Garch | ged    | 0 |
| Garch | normal | 1 |
| Garch | ged    | 1 |

#### Portfolio Holdings
| Stock | Quantity |
|-------|----------|
| AAPL  | 50       |
| MSFT  | 50       |

#### Color map coding for matplotlib
| Color | Hex Code |
|-------|----------|
| green | #00FF00  |
| amber | #FFBF00  |
| red   | #FF0000  |










