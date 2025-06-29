# 🎲 Probability Horizon

[中文 README](README.md)

An interactive probability learning tool that helps users understand core probability concepts through visualization and simulation.

## ✨ Main Features

### 🎯 Central Limit Theorem Interactive Simulator
- **Multiple Population Distributions**: Supports 8 different probability distributions (Uniform, Normal, Exponential, Poisson, Gamma, Beta, Chi-square, Binomial)
- **Adjustable Parameters**: Flexibly adjust sample size (1-200) and number of samples (10-5000)
- **Real-time Visualization**: Dynamically display original distribution, sample mean distribution, histograms, and Q-Q plots
- **Theoretical Comparison**: Compare actual statistics with theoretical values
- **Normality Tests**: Shapiro-Wilk and Kolmogorov-Smirnov tests

### 🔍 Classic Probability Distribution Explorer
- **Rich Distribution Types**: 12 commonly used probability distributions (continuous and discrete)
- **Real-time Parameter Adjustment**: Adjust distribution parameters in real time with sliders
- **PDF/PMF Visualization**: High-quality probability density/mass function charts
- **Statistics Calculation**: Mean, variance, standard deviation, skewness, kurtosis, etc.
- **Quantile Information**: 25%, 50%, 75% quantiles and interquartile range
- **Application Scenarios**: Real-world application scenarios for each distribution

## 🚀 Quick Start

### Requirements
- Python 3.12+
- uv package manager

### Installation Steps

1. **Clone the project**
```bash
git clone https://github.com/zym9863/prob-horizon.git
cd Prob-Horizon
```

2. **Install dependencies**
```bash
uv sync
```

3. **Run the application**
```bash
uv run streamlit run main.py
```

4. **Access the app**
Open your browser and visit `http://localhost:8501`

## 📖 User Guide

### Central Limit Theorem Simulator

1. **Select Population Distribution**: Choose a population distribution from the sidebar
2. **Set Parameters**:
   - Sample size: Number of samples per draw
   - Number of samples: Total number of draws
3. **Start Simulation**: Click the "Start Simulation" button
4. **Observe Results**:
   - See if the sample mean distribution approaches normality
   - Compare actual values with theoretical values
   - View normality test results

### Probability Distribution Explorer

1. **Select Distribution**:
   - First select distribution type (continuous/discrete)
   - Then select the specific distribution
2. **Adjust Parameters**: Use sliders to adjust distribution parameters
3. **View Results**:
   - View PDF/PMF charts in real time
   - View statistics and quantile information
   - Learn about real-world application scenarios

## 🛠️ Tech Stack

- **Frontend Framework**: Streamlit
- **Numerical Computing**: NumPy, SciPy
- **Data Processing**: Pandas
- **Visualization**: Plotly, Matplotlib
- **Package Management**: uv

## 📁 Project Structure

```
Prob-Horizon/
├── main.py                 # Main application entry
├── src/
│   ├── components/         # UI components
│   │   ├── clt_simulator_ui.py
│   │   └── distribution_explorer_ui.py
│   └── utils/             # Core logic
│       ├── clt_simulator.py
│       └── distribution_explorer.py
├── tests/                 # Test files
├── pyproject.toml         # Project config
└── README.md              # Project documentation
```

## 🎓 Educational Value

### Central Limit Theorem
- **Intuitive Understanding**: Visually understand the meaning of the CLT
- **Parameter Impact**: Observe the effect of sample size on the theorem
- **Distribution Independence**: Verify the universality of the theorem for different population distributions

### Probability Distributions
- **Parameter Effects**: Understand how parameter changes affect distribution shapes
- **Distribution Characteristics**: Master the statistical characteristics of various distributions
- **Practical Applications**: Learn about real-world applications of different distributions

## 🤝 Contribution Guide

Contributions are welcome! Please submit Issues and Pull Requests to help improve this project.

### Development Environment Setup
```bash
# Clone the project
git clone https://github.com/zym9863/prob-horizon.git
cd Prob-Horizon

# Install development dependencies
uv add --dev pytest black flake8

# Run tests
uv run pytest

# Code formatting
uv run black .
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

Thanks to the following open source projects:
- [Streamlit](https://streamlit.io/) - Rapid data app development
- [SciPy](https://scipy.org/) - Scientific computing library
- [Plotly](https://plotly.com/) - Interactive visualization
- [NumPy](https://numpy.org/) - Numerical computing foundation

---

**Probability Horizon** - Making probability learning more intuitive and fun! 🎲✨
