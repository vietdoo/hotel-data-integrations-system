# Hotel Data Integration System

## System Architecture

### Core Components

1. **Supplier Layer**
- [`BaseSupplier`](suppliers/base_supplier.py) - Abstract base class for all suppliers
- Implementations: [`AcmeSupplier`](suppliers/modules/acme.py), [`PatagoniaSupplier`](suppliers/modules/patagonia.py), [`PaperfliesSupplier`](suppliers/modules/paperflies.py)
- Managed by [`SupplierManager`](suppliers/suppliers.py) for unified data fetching.

2. **Data Processing Layer**
- Normalization: [`DataNormalizer`](services/normalizer.py) for data cleaning and standardization
- Merging: [`DataMerger`](services/merger.py) for combining data from multiple sources
- Validation: Uses Pydantic models in [`models/hotel.py`](models/hotel.py)

3. **Storage Layer**
- Abstract [`BaseDB`](services/database.py) interface
- Implementations: [`HotelDB`](services/database.py) and [`RawHotelDB`](services/database.py)

4. **API Layer**
- FastAPI-style routing with [`HotelAPI`](api/services/hotel.py)
- Endpoint handlers in [api/routers](api/routers)

### Data Flow
1. Data fetching from suppliers
2. Normalization and cleaning
3. Updating fully normalized data in database
4. Merging with bias handling for multiple suppliers
5. Storage in databases 
6. API access to merged data

## Design Principles

### 1. SOLID Principles
- **Single Responsibility**: Each class has one purpose (e.g., [`Normalizer`](services/normalizer.py))
- **Open/Closed**: Abstract base classes allow extension (e.g., [`BaseSupplier`](suppliers/base_supplier.py))
- **Liskov Substitution**: All database implementations follow [`BaseDB`](services/database.py) contract
- **Interface Segregation**: Targeted interfaces like [`AttributeNormalizer`](services/normalizer.py)
- **Dependency Injection**: Services accept dependencies in constructors

### 2. Clean Architecture
- Clear separation between data, domain logic, and presentation
- Domain models independent of external concerns
- Use of interfaces for flexibility

### 3. Design Patterns
- **Strategy**: Different merger strategies in [`services/merger.py`](services/merger.py)
- **Factory**: Supplier creation in [`SupplierManager`](suppliers/suppliers.py)
- **Singleton**: Logger implementation in [`utils/logger.py`](utils/logger.py)
- **Decorator**: API routing decorators

## Key Features

1. **Data Quality**
- Robust normalization via [`HotelCleaner`](utils/cleaner.py)
- Configurable bias handling for data merging
- Validation using Pydantic models

2. **Extensibility**
- Easy to add new suppliers
- Pluggable normalizers and mergers
- Configurable via [configs/config.py](configs/config.py)

3. **Maintainability**
- Comprehensive logging system
- Clear error handling with custom exceptions
- Well-defined interfaces

## Usage

```
python main.py hotel_id1,hotel_id2 destination_id1
```

 