# Pokemon Data Pipeline Evolution

This project shows how I've built a data extraction pipeline from the ground up, starting simple and adding complexity step by step. Each version teaches different data engineering concepts.

## Current Progress

### Level 1: Basic Sequential Processing (`level_1_basic_sync.py`)

The simplest approach - one API call at a time. This version demonstrates:

- **Sequential processing**: Making requests one after another
- **Basic error handling**: Simple try/catch blocks 
- **Data extraction**: Pulling specific fields from API responses
- **CSV output**: Using pandas to save structured data

**Key concepts**: ETL basics, REST API consumption, data transformation

This is where most data pipelines start - getting the data flowing first, then optimising later.

## What's Next

I'm planning to add more sophisticated versions that show:
- Concurrent processing for better speed
- Async/await patterns
- Better error handling and retries
- Data validation
- Production-ready patterns

Each version will build on the previous one, showing how real data pipelines evolve from simple scripts to robust systems.