# Development Guide

## Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd The-AI-s-Mercado-Libre-in-develop-main
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env with your values
```

### Configuration

The application uses `config.yaml` for thresholds and settings:

- **metrics**: CTR, Conversion Rate, and ACOS thresholds
- **scoring**: Points allocation for scoring system
- **logging**: Log level and file settings

Edit `config.yaml` to customize these values for your use case.

## Running the Application

### Batch Analysis
```bash
python app_batch.py
```

### Streamlit Dashboard
```bash
streamlit run dashboard.py
```

The dashboard will be available at `http://localhost:8501`

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_metrics.py -v
```

### Run Tests with Coverage
```bash
pytest --cov=. --cov-report=html
```

Coverage report will be generated in `htmlcov/index.html`

### Run Specific Test Class
```bash
pytest tests/test_metrics.py::TestCalculateCTR -v
```

### Run Specific Test
```bash
pytest tests/test_metrics.py::TestCalculateCTR::test_normal_ctr_calculation -v
```

## Project Structure

```
├── analyzer/
│   ├── __init__.py
│   ├── metrics.py          # KPI calculations
│   ├── diagnosis.py        # Issue detection
│   ├── recommendations.py  # Action generation
│   └── product_ranking.py  # Scoring & classification
├── ads/
│   ├── __init__.py
│   ├── acos_optimizer.py   # ACOS management
│   └── bidding_logic.py    # Bidding strategies
├── tests/
│   ├── __init__.py
│   ├── test_metrics.py
│   ├── test_product_ranking.py
│   ├── test_diagnosis.py
│   └── test_acos_optimizer.py
├── inputs/
│   └── product_data.json   # Sample data
├── app_batch.py            # Batch analysis script
├── dashboard.py            # Streamlit dashboard
├── config.yaml             # Configuration file
├── config_loader.py        # Config management
├── logger_config.py        # Logging setup
├── requirements.txt        # Dependencies
├── pytest.ini             # Pytest configuration
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

## Logging

Logs are stored in `logs/app.log` by default and are configured in `config.yaml`.

Log levels:
- `DEBUG`: Detailed information
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

## Code Quality

### Adding a New Module

1. Create the module file with full docstrings
2. Add type hints to all functions
3. Implement input validation
4. Add logging for important operations
5. Write unit tests in `tests/test_*.py`

### Documentation Standards

- Use Google-style docstrings
- Include Args, Returns, Raises sections
- Provide examples where helpful
- Document all public functions

## Troubleshooting

### Import Errors
Ensure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### Config File Not Found
Place `config.yaml` in the root directory. The application will use defaults if not found.

### Logging Issues
Check that the `logs/` directory exists and is writable:
```bash
mkdir -p logs
```

## Contributing

1. Create a branch for your feature
2. Write tests for new functionality
3. Ensure all tests pass: `pytest`
4. Update documentation
5. Create a pull request

## Performance Tips

- Use batch processing for large catalogs
- Monitor ACOS thresholds (typically 20-30%)
- Review recommendations weekly
- Scale products with score >= 70
- Optimize products with 40-70 score
- Pause products with score < 40
