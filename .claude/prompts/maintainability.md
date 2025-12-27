# Maintainability Implementation Guide

Implement the feature with focus on **maintainability**: clean architecture, SOLID principles, and long-term sustainability.

## Implementation Philosophy

Prioritize:
- **Clean architecture** - Clear separation of concerns
- **SOLID principles** - Especially Open/Closed for extensibility
- **Modularity** - Small, focused modules that do one thing well
- **Testability** - Code that's easy to unit test
- **Readability** - Self-documenting code with clear intent

## Implementation Requirements

### File Structure

Create this structure:
```
src/
├── __init__.py          # Package init, exports Calculator
├── calculator.py        # Main Calculator class
├── operations.py        # Operation classes (Strategy pattern)
└── exceptions.py        # Custom exceptions

features/
└── steps/
    └── calculator_steps.py  # Update to import from src.calculator
```

### Steps

1. Read `features/calculator.feature` to understand requirements
2. Read `features/steps/calculator_steps.py` to see expected interface
3. Create `src/__init__.py`, `src/calculator.py`, `src/operations.py`, `src/exceptions.py`
4. Update `features/steps/calculator_steps.py` to import and use Calculator
5. Run `uv run behave` to verify all tests pass

## Maintainability Patterns to Apply

### 1. Strategy Pattern for Operations
```python
# operations.py
from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass

class Addition(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b
```

### 2. Separation of Concerns
- `calculator.py` - Orchestration and state management
- `operations.py` - Individual operation implementations
- `exceptions.py` - Error types and handling

### 3. Open/Closed Principle
- Easy to add new operations without modifying existing code
- Register new operations through configuration
- Plugin-style architecture

### 4. Dependency Injection
- Operations injected into Calculator
- Easy to mock for testing
- Configurable behavior

### 5. Type Hints Throughout
```python
def add(self, a: float, b: float) -> float:
    """Add two numbers."""
    return a + b
```

### 6. Clear Documentation
- Module-level docstrings
- Class and method documentation
- Type hints as documentation

## Verification Checklist

Before reporting completion:
- [ ] `src/__init__.py` exists and exports Calculator
- [ ] `src/calculator.py` exists with Calculator class
- [ ] `src/operations.py` exists with Operation classes
- [ ] `src/exceptions.py` exists with custom exceptions
- [ ] `features/steps/calculator_steps.py` imports from src
- [ ] `uv run behave` shows all 5 scenarios passing
- [ ] Strategy pattern is implemented for operations
- [ ] Type hints are present throughout
