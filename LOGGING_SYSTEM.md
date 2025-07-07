# Logging System Documentation

## Overview

The RegReportRAG application now includes a comprehensive logging system that captures all application activities, errors, and system information in organized log files. This system provides detailed insights into application behavior, debugging capabilities, and operational monitoring.

## Log Files Structure

All log files are stored in the `backend/logs/` directory and are organized by date and type:

```
backend/logs/
├── app_YYYY-MM-DD.log           # Main application log
├── api_YYYY-MM-DD.log           # API requests and responses
├── vector_YYYY-MM-DD.log        # Vector service operations
├── database_YYYY-MM-DD.log      # Database operations
├── document_processing_YYYY-MM-DD.log  # Document processing activities
├── rag_YYYY-MM-DD.log           # RAG service operations
└── errors_YYYY-MM-DD.log        # Error log (ERROR level and above)
```

## Log File Details

### 1. Application Log (`app_*.log`)
- **Purpose**: Main application lifecycle events
- **Content**: Startup, shutdown, service initialization, system information
- **Level**: INFO and above
- **Rotation**: 10MB max size, 5 backup files

### 2. API Log (`api_*.log`)
- **Purpose**: API endpoint requests and responses
- **Content**: HTTP requests, response times, endpoint access
- **Level**: INFO and above
- **Rotation**: 10MB max size, 5 backup files

### 3. Vector Service Log (`vector_*.log`)
- **Purpose**: Vector database operations
- **Content**: Document processing, embedding generation, similarity searches
- **Level**: DEBUG and above
- **Rotation**: 5MB max size, 5 backup files

### 4. Database Log (`database_*.log`)
- **Purpose**: Database operations and queries
- **Content**: SQL queries, connection management, transaction logs
- **Level**: DEBUG and above
- **Rotation**: 5MB max size, 5 backup files

### 5. Document Processing Log (`document_processing_*.log`)
- **Purpose**: PDF processing and chunking activities
- **Content**: File processing, text extraction, chunk creation
- **Level**: DEBUG and above
- **Rotation**: 5MB max size, 5 backup files

### 6. RAG Service Log (`rag_*.log`)
- **Purpose**: RAG pipeline operations
- **Content**: Document retrieval, LLM interactions, compliance analysis
- **Level**: DEBUG and above
- **Rotation**: 5MB max size, 5 backup files

### 7. Error Log (`errors_*.log`)
- **Purpose**: Error tracking and debugging
- **Content**: All ERROR and CRITICAL level messages from all components
- **Level**: ERROR and above
- **Rotation**: 5MB max size, 10 backup files

## Log Format

Each log entry follows this format:
```
YYYY-MM-DD HH:MM:SS,mmm - logger_name - LEVEL - filename:line_number - function_name - message
```

Example:
```
2025-07-05 09:58:57,878 - vector_service - INFO - vector_service.py:56 - initialize_database - Initialized PostgreSQL database with pgvector extension
```

## Using the Log Viewer Script

A convenient script `view_logs.sh` is provided to easily view and manage log files:

### Basic Usage
```bash
# View main application log (last 20 lines)
./view_logs.sh app

# View error log (last 20 lines)
./view_logs.sh error

# View vector service log (last 50 lines)
./view_logs.sh vector 50
```

### Available Commands
```bash
# List all log files and their sizes
./view_logs.sh list

# View all logs (last 10 lines each)
./view_logs.sh all 10

# View specific log types
./view_logs.sh api          # API requests
./view_logs.sh database     # Database operations
./view_logs.sh document     # Document processing
./view_logs.sh rag          # RAG service
```

### Log Types
- `app`, `application` - Main application log
- `api` - API requests log
- `vector`, `vector_service` - Vector service operations
- `database`, `db` - Database operations
- `document`, `doc` - Document processing
- `rag` - RAG service operations
- `error`, `errors` - Error log
- `all` - Show all logs
- `list`, `ls` - List available log files

## Configuration

The logging system is configured in `backend/app/utils/logging_config.py`:

### Key Features
- **Automatic log rotation**: Prevents log files from growing too large
- **Date-based naming**: Logs are organized by date for easy management
- **Multiple log levels**: Different verbosity levels for different components
- **Structured format**: Consistent, parseable log format
- **System information**: Automatic logging of system details on startup

### Log Levels
- **DEBUG**: Detailed information for debugging
- **INFO**: General information about application flow
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for actual problems
- **CRITICAL**: Critical errors that may cause application failure

## Integration with Application

The logging system is automatically initialized when the application starts:

1. **Startup**: System information and configuration are logged
2. **Service Initialization**: Each service logs its initialization process
3. **Runtime Operations**: All major operations are logged with appropriate detail
4. **Error Handling**: All errors are captured with full context
5. **Shutdown**: Cleanup operations are logged

## Monitoring and Maintenance

### Daily Operations
- Check error logs for any issues: `./view_logs.sh error`
- Monitor application health: `./view_logs.sh app 50`
- Review API usage: `./view_logs.sh api`

### Log Management
- Log files are automatically rotated when they reach size limits
- Old backup files are automatically cleaned up
- Daily log files make it easy to track issues by date

### Performance Considerations
- Log rotation prevents disk space issues
- Different log levels allow for performance tuning
- Structured format enables easy parsing and analysis

## Troubleshooting

### Common Issues
1. **Empty log files**: Check if the application is running and generating logs
2. **Permission errors**: Ensure the `logs/` directory has write permissions
3. **Large log files**: Check for excessive logging or errors causing rapid log growth

### Debug Mode
To enable more detailed logging, modify the log level in `backend/app/main.py`:
```python
setup_logging(log_level="DEBUG", log_dir="logs")
```

## Best Practices

1. **Regular Monitoring**: Check error logs daily for issues
2. **Log Analysis**: Use the structured format for automated log analysis
3. **Backup Management**: Consider backing up important log files
4. **Performance**: Monitor log file sizes and adjust rotation settings if needed
5. **Security**: Ensure log files don't contain sensitive information

## Example Log Analysis

```bash
# Find all errors from today
grep "ERROR" backend/logs/errors_$(date +%Y-%m-%d).log

# Count API requests
wc -l backend/logs/api_$(date +%Y-%m-%d).log

# Monitor application startup
grep "startup\|initialization" backend/logs/app_$(date +%Y-%m-%d).log
```

This comprehensive logging system provides full visibility into the application's operation, making debugging, monitoring, and maintenance much more effective. 