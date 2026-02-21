# Data Cleansing with OpenAI

A batch processing system for cleansing and rephrasing business descriptions using OpenAI's API. This project automates the process of cleaning large datasets of business information by leveraging GPT models to standardize and improve text quality.

## Features

- **Batch Processing**: Efficiently processes large volumes of data using OpenAI's batch API
- **Database Integration**: Connects to MySQL databases for data export and import
- **Automated Workflow**: Orchestrates the entire pipeline from data export to final import
- **Error Handling**: Includes retry logic and dynamic chunk sizing for reliability
- **Usage Monitoring**: Tools to check OpenAI API usage and account status

## Prerequisites

- Python 3.8+
- MySQL database with business data
- OpenAI API key with batch processing access
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   DB_HOST=your_mysql_host
   DB_USER=your_mysql_username
   DB_PASS=your_mysql_password
   DB_NAME=your_database_name
   ```

## Usage

### Full Pipeline Run
Run the complete data cleansing pipeline:
```bash
python run_all.py
```

This will:
1. Export unprocessed business data from MySQL
2. Submit batches to OpenAI for processing
3. Monitor batch status
4. Import cleaned results back to the database

### Individual Steps
You can also run individual pipeline steps:

- **Export Data**: `python s1_export.py`
- **Submit Batch**: `python s2_submit.py`
- **Check Status**: `python s3_status.py`
- **Import Results**: `python s4_import.py`

### Check OpenAI Usage
Monitor your OpenAI account usage:
```bash
python usage.py
```

### Testing
Run tests to verify functionality:
```bash
python test.py
```

## Configuration

The system includes several configurable parameters in `run_all.py`:

- `GOAL_TOTAL`: Total number of records to process
- `CHUNK_SIZE`: Initial batch size (dynamically adjusts on failures)
- `MIN_CHUNK_SIZE`: Minimum batch size after failures
- `POLL_INTERVAL`: Status check interval in seconds
- `MAX_FAILURES`: Consecutive failures before reducing batch size

## Data Processing

The system processes business records with the following fields:
- `id`: Unique identifier
- `category`: Business category
- `business_name`: Business name
- `description`: Original description text

### Cleaning Rules
OpenAI is instructed to:
- Rephrase descriptions to be professional and clear
- Include real phone numbers if available (never guess or create them)
- Regenerate content based on category/name if source is inadequate
- Remove ads, repetition, junk, emojis, and URLs
- Limit to 1-2 concise sentences

## Database Schema

Expected table structure:
```sql
CREATE TABLE updated_business (
    id INT PRIMARY KEY,
    category VARCHAR(255),
    business_name VARCHAR(255),
    description TEXT,
    is_processed BOOLEAN DEFAULT FALSE
);
```

## File Structure

- `main.py`: Entry point for the pipeline
- `run_all.py`: Main orchestrator with dual-batch processing
- `s1_export.py`: Data export from MySQL to JSONL
- `s2_submit.py`: Batch submission to OpenAI
- `s3_status.py`: Batch status monitoring
- `s4_import.py`: Results import back to MySQL
- `usage.py`: OpenAI account usage checker
- `test.py`: Test suite
- `openai_test.py`: OpenAI API testing
- `batch_input.jsonl`: Temporary batch input file
- `config/`: Configuration directory (currently empty)
- `requirements.txt`: Python dependencies

## API Usage

This project uses OpenAI's Batch API for cost-effective processing of large datasets. Make sure your OpenAI account has:
- Sufficient credits
- Access to batch processing features
- Appropriate rate limits for your tier

## Error Handling

The system includes robust error handling:
- Automatic retry on submission failures
- Dynamic batch size reduction on consecutive failures
- Status polling with configurable intervals
- Graceful handling of API rate limits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues or questions:
- Check the OpenAI platform status
- Verify your API key and database credentials
- Review the batch processing limits and quotas
