# Genesis.py - Universal GenAI Interface

Genesis.py is a sophisticated broker between OpenRouter and end users/devices, providing a streamlined interface for accessing multiple GenAI models through OpenRouter's API. Originally created as an alternative solution for Hong Kong users who cannot access ChatGPT directly.

**Current Version:** 0.1.1  
**Supported Python Version:** 3.10+  
**Author:** Victor McTrix (Enhanced)

## 🚀 Recent Updates

**Version 0.1.1 (Enhanced) - Latest:**
- ✅ Enhanced error handling and timeout management
- ✅ Improved image handling with automatic format detection
- ✅ Better JSON response parsing and validation
- ✅ Added `ClearAll()` method for content management
- ✅ Enhanced provider selection with fallback options
- ✅ Optimized for large batch processing (10k token support)
- ✅ Fixed file encoding and base64 conversion issues
- ✅ Added comprehensive debugging and logging features

**Version 0.1.0 (January 18th, 2025):**
- 🔄 Final update addressing OpenAI access restrictions through OpenRouter
- ➕ Added provider selection in `TXRX()` method
- 📝 Initial stable release

## 📚 Theoretical Foundation

### Prompt Engineering Principles

Prompt engineering is the methodology for programming Large Language Models (LLMs) through carefully crafted instructions. Genesis.py implements a dual-prompt system:

**System Prompts:** Core instructions that define the AI's role, behavior, and constraints. These set the foundational context for all interactions.

**User Prompts:** Dynamic input from users that triggers specific responses within the system-defined framework.

### Architecture Benefits

By separating system and user contexts, Genesis.py enables:
- **Role-based AI behavior** with consistent personality and expertise
- **Context-aware responses** tailored to specific use cases
- **Scalable applications** suitable for enterprise deployment
- **Multi-modal input support** (text, images, files)

## 🔧 Core Features

### Multi-Modal Content Support
- **Text Messages:** Direct string input with UTF-8 support
- **Image Processing:** Automatic base64 conversion with format detection (JPEG, PNG, WebP, GIF)
- **File Integration:** Markdown conversion for documents, PDFs, and structured data
- **URL Handling:** Direct image URL processing without local conversion

### Enhanced AI Model Access
- **Multiple Providers:** OpenAI, Google, Anthropic, and other OpenRouter-supported models
- **Provider Fallback:** Automatic failover when primary providers are unavailable
- **Token Management:** Configurable limits up to 10,000 tokens for large responses
- **Temperature Control:** Adjustable creativity levels (0.0-1.0)

### Robust Error Handling
- **Timeout Management:** 30-second default with configurable options
- **Response Validation:** JSON parsing with error recovery
- **Network Resilience:** Automatic retry and detailed error reporting
- **Debug Support:** Comprehensive logging for troubleshooting

## 📖 API Reference

### Constructor

```python
Genesis(key: str, httpRef: str = "", projTitle: str = "")
```

**Parameters:**
- `key`: OpenRouter API key (required)
- `httpRef`: HTTP referer for usage tracking (optional)
- `projTitle`: Project title for organization (optional)

### Primary Methods

#### `TXRX(LLM: str, provider: List[str], max_tokens: int, temperature: float) -> Optional[str]`
Main communication method with enhanced parameter support.

**Parameters:**
- `LLM`: Model identifier (default: "openai/gpt-4o-2024-11-20")
- `provider`: Preferred provider list (default: ["OpenAI"])
- `max_tokens`: Response length limit (optional)
- `temperature`: Creativity level 0.0-1.0 (optional)

**Returns:** AI response string or None if error

#### Content Management Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `PushMsgToSystem(value: str)` | Add system instruction | None |
| `PushFileToSystem(filename: str)` | Add file to system context | bool |
| `PushMsgToUser(dicttype: str, value: str)` | Add user message | None |
| `PushImgToUser(value: str, fileType: str)` | Add image to user context | None |
| `PushFileToUser(filename: str)` | Add file to user context | bool |
| `PopMsgOfSystem()` | Remove last system message | bool |
| `PopMsgOfUser()` | Remove last user message | bool |
| `ClearAll()` | Clear all content | None |

#### Utility Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `CheckSystemContentsExist()` | Verify system content | bool |
| `CheckUserContentsExist()` | Verify user content | bool |
| `DebugCheckSystem()` | Display system contents | None |
| `DebugCheckUser()` | Display user contents | None |

## 💡 Usage Examples

### Basic Text Interaction

```python
import os
from Genesis import Genesis

# Initialize with API key
api_key = os.getenv('OPENROUTER_API_KEY')
AI = Genesis(api_key, "https://myapp.com", "My Project")

# Set system context
AI.PushMsgToSystem("You are a helpful programming assistant.")

# Add user query
AI.PushMsgToUser("text", "Explain Python list comprehensions with examples.")

# Get response
response = AI.TXRX(
    LLM="openai/gpt-4o-2024-11-20",
    provider=["OpenAI"],
    max_tokens=500,
    temperature=0.7
)

print(response)
```

### Image Analysis Application

```python
# Financial document analysis
AI = Genesis(api_key, project_title="Financial Analysis")

AI.PushMsgToSystem("""You are a financial analyst. Analyze charts and 
provide investment insights based on visual data.""")

# Add image from file
AI.PushImgToUser("stock_chart.png")
AI.PushMsgToUser("text", "What trends do you see in this stock chart?")

response = AI.TXRX(
    LLM="google/gemini-2.5-flash-preview-05-20",
    provider=["google-ai-studio"],
    max_tokens=1000
)
```

### Batch Processing for Large Datasets

```python
# S&P 500 stock analysis
AI = Genesis(api_key, project_title="Bulk Stock Analysis")

AI.PushMsgToSystem("""You are a stock analyst. Provide investment scores 
(0.0-1.0) for all stocks in JSON format: {"SYMBOL": score, ...}""")

# Process multiple stocks
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
AI.PushMsgToUser("text", ", ".join(symbols))

response = AI.TXRX(
    LLM="google/gemini-2.5-flash-preview-05-20",
    provider=["google-ai-studio", "google-vertex"],
    max_tokens=10000,  # Large response for batch processing
    temperature=0.3
)
```

### File Processing Pipeline

```python
# Document analysis workflow
AI = Genesis(api_key, project_title="Document Processing")

# Add multiple context files
AI.PushFileToSystem("company_data.pdf")
AI.PushFileToSystem("market_report.docx")

# Query based on combined context
AI.PushMsgToUser("text", "Based on the provided documents, what are the key investment risks?")

response = AI.TXRX(
    LLM="anthropic/claude-3-sonnet",
    provider=["Anthropic"],
    max_tokens=2000
)
```

## ⚠️ Limitations and Requirements

### Dependencies

```bash
pip install requests markitdown python-dotenv
```

### OpenRouter Constraints
- **File Limitations:** Direct file upload not supported; requires markdown conversion
- **Rate Limits:** Subject to OpenRouter's API rate limiting
- **Model Availability:** Dependent on OpenRouter's model catalog
- **Token Costs:** Usage charges apply based on model and token consumption

### MarkItDown Limitations
- **Image Extraction:** Cannot convert embedded images to base64
- **Mathematical Notation:** LaTeX and complex math symbols may not convert properly
- **Formatting Loss:** Some document formatting may be simplified during conversion
- **File Size Limits:** Large files may cause processing delays

### File Format Support

**Supported for Conversion:**
- PDF documents
- Microsoft Office files (Word, Excel, PowerPoint)
- Plain text files
- Markdown files
- CSV and TSV data

**Image Formats:**
- JPEG/JPG
- PNG
- WebP
- GIF

## 🔒 Security Best Practices

### API Key Management

```python
# ✅ Recommended: Environment variables
import os
api_key = os.getenv('OPENROUTER_API_KEY')

# ❌ Avoid: Hardcoded keys
api_key = "sk-or-v1-..."  # Never do this in production
```

### Data Privacy
- **Sensitive Data:** Avoid sending confidential information through external APIs
- **Local Processing:** Consider local preprocessing for sensitive documents
- **Audit Logging:** Implement usage tracking for compliance requirements

## 🧪 Testing and Debugging

### Debug Mode

```python
# Enable comprehensive debugging
AI = Genesis(api_key, project_title="Debug Session")
AI.PushMsgToSystem("Test system message")
AI.PushMsgToUser("text", "Test user message")

# Check content before sending
AI.DebugCheckSystem()
AI.DebugCheckUser()

# Monitor errors
response = AI.TXRX()
if not response:
    print(f"Error: {AI.last_error}")
```

### Error Handling Patterns

```python
try:
    response = AI.TXRX(timeout=60)
    if response:
        # Process successful response
        return process_response(response)
    else:
        # Handle API errors
        log_error(AI.last_error)
        return fallback_response()
        
except Exception as e:
    # Handle unexpected errors
    log_exception(e)
    return error_response()
```

## 🌐 Production Deployment

### Azure Cloud Integration

For scalable applications, deploy Genesis.py on Azure Virtual Machines:

```python
# Azure-optimized configuration
class ProductionGenesis:
    def __init__(self, key: str):
        self.AI = Genesis(
            key=key,
            httpRef="https://myapp.azurewebsites.net",
            projTitle="Production App v1.0"
        )
        self.setup_logging()
    
    def setup_logging(self):
        # Configure Azure Application Insights
        pass
    
    def process_request(self, user_data: dict) -> dict:
        # Production request handler
        self.AI.ClearAll()  # Reset for new session
        return self.generate_response(user_data)
```

### Load Balancing

For high-volume applications, implement provider rotation:

```python
providers = [
    ["OpenAI"],
    ["google-ai-studio"],
    ["Anthropic"],
    ["Meta"]
]

for provider in providers:
    response = AI.TXRX(provider=provider)
    if response:
        break  # Success
```

## 📊 Performance Optimization

### Token Efficiency

```python
# Optimize for large batch processing
def optimize_for_batch(symbols: List[str]) -> dict:
    AI = Genesis(api_key)
    
    # Concise system prompt
    AI.PushMsgToSystem("Return JSON: {\"SYMBOL\": score}")
    
    # Batch symbols efficiently
    AI.PushMsgToUser("text", ",".join(symbols))
    
    # Use high token limit for complete responses
    return AI.TXRX(max_tokens=10000, temperature=0.3)
```

### Memory Management

```python
# Clean up for long-running processes
def periodic_cleanup(AI: Genesis):
    if len(AI.systemContents) > 10:
        AI.ClearAll()
        # Reload essential system context
        AI.PushMsgToSystem(essential_system_prompt)
```

## 📈 Version History

| Version | Release Date | Key Features |
|---------|-------------|--------------|
| 0.1.1 | 2025 | Enhanced error handling, batch processing, provider fallback |
| 0.1.0 | Jan 18, 2025 | Initial stable release, provider selection |
| 0.0.x | Development | Core functionality, basic OpenRouter integration |

## 🤝 Contributing

Genesis.py is maintained as part of a larger trading and analysis system. For issues or feature requests, please ensure compatibility with the existing COMP2012 Enhanced Trading Bot architecture.

## 📚 References

[1] J. White et al., "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT," 2023. Available: https://arxiv.org/pdf/2302.11382

[2] P. Liu, W. Yuan, J. Fu, Z. Jiang, H. Hayashi, and G. Neubig, "Pre train, prompt, and predict: A systematic survey of prompting methods in natural language processing," ACM Computing Surveys, vol. 55, no. 9, pp. 1–35, 2023.

[3] M. Groenewege, "System prompt design: Bridging the gap between novice mental models and reality," Discourse & Communication, Aug. 2024, doi: https://doi.org/10.1177/17504813241267055.

---
