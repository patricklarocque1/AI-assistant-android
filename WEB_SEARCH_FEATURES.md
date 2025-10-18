# Web Search & Research Features

## Overview

The Local AI Server now includes powerful web search and research capabilities, allowing your AI assistant to access real-time information from the internet. This feature enables the AI to provide up-to-date answers based on current web content, similar to how frameworks like LangChain, AutoGPT, and Perplexity AI work.

## Key Features

### 🔍 Web Search
- **DuckDuckGo Integration**: Privacy-focused search without requiring API keys
- **Real-time Results**: Access current information from the web
- **Multiple Results**: Get up to 10 search results per query
- **Rich Metadata**: Each result includes title, URL, and snippet

### 🤖 AI Research Mode
- **Search & Summarize**: AI searches the web and provides comprehensive answers
- **Context-Aware**: Combines search results with AI's language understanding
- **Source Citations**: Includes links to original sources
- **Intelligent Synthesis**: AI summarizes and analyzes multiple sources

### 🌐 User-Friendly Web Interface
- **Modern UI**: Clean, responsive interface accessible via web browser
- **Multiple Modes**: 
  - AI Chat (standard conversation)
  - Web Search (direct search results)
  - Search & Chat (AI-powered research)
- **Real-time Updates**: See results as they're generated
- **No Installation Required**: Access via any web browser

## How It Works

### Architecture

The system follows best practices from leading AI frameworks:

1. **Tool Integration**: Similar to LangChain's tool architecture
   - AI can invoke web search as a tool
   - Results are formatted and passed to the AI model
   - AI generates responses based on search context

2. **Privacy-First**: Like Perplexity but self-hosted
   - Uses DuckDuckGo (privacy-focused search)
   - No tracking or data collection
   - All processing happens on your local machine

3. **Autonomous Research**: Inspired by AutoGPT
   - AI determines when web search is needed
   - Combines multiple sources intelligently
   - Provides comprehensive, sourced answers

## Usage

### Web Interface

1. **Start the Server**:
   ```bash
   cd local_ai_server
   python ai_server.py
   ```

2. **Access the Interface**:
   - Open your browser to the Ngrok URL (shown in terminal)
   - Or access locally at `http://localhost:5000`

3. **Choose Your Mode**:
   - **AI Chat**: Traditional AI conversation
   - **Web Search**: Direct web search results
   - **Search & Chat**: AI researches and answers

### API Usage

#### 1. Standard Chat (No Web Search)
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is machine learning?",
    "max_length": 512
  }'
```

#### 2. Web Search Only
```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "latest AI developments 2024",
    "max_results": 5
  }'
```

**Response**:
```json
{
  "query": "latest AI developments 2024",
  "results": [
    {
      "title": "AI Breakthrough in 2024",
      "link": "https://example.com/article",
      "snippet": "Recent developments in AI include..."
    }
  ],
  "count": 5
}
```

#### 3. Search & Chat (AI Research)
```bash
curl -X POST http://localhost:5000/search_and_chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the latest developments in quantum computing?"
  }'
```

**Response**:
```json
{
  "query": "What are the latest developments in quantum computing?",
  "response": "Based on recent web sources, quantum computing has seen...\n\nSources:\n1. Title: URL\n2. Title: URL",
  "model": "Qwen/Qwen3-0.6B",
  "device": "cpu"
}
```

### Android App Integration

Update your Android app to use the new search features:

```kotlin
// In your API service interface
@POST("search_and_chat")
suspend fun searchAndChat(
    @Body request: SearchChatRequest
): Response<SearchChatResponse>

data class SearchChatRequest(
    val query: String,
    val search_query: String? = null
)

data class SearchChatResponse(
    val query: String,
    val response: String,
    val model: String,
    val device: String
)
```

## Configuration

The web search features work out of the box with no additional configuration needed. However, you can customize behavior:

### Environment Variables

Add to your `.env` file:

```bash
# Web Search Configuration
ENABLE_WEB_SEARCH=true
MAX_SEARCH_RESULTS=5
SEARCH_TIMEOUT=30
```

### Customization Options

In `ai_server.py`, you can adjust:

- **Search Results Count**: Change `max_results` parameter
- **AI Context Length**: Adjust how much search context is provided to AI
- **Source Citation Format**: Customize how sources are displayed

## Examples

### Example 1: Current Events
**User**: "What are the latest news about AI regulations?"

**AI Response**:
```
Based on recent web sources, AI regulations have been a hot topic in 2024. 
The European Union has passed comprehensive AI legislation focusing on 
transparency and safety. In the United States, several states are considering 
their own AI regulation frameworks...

Sources:
1. EU AI Act Updates: https://example.com/eu-ai-act
2. US AI Regulation Status: https://example.com/us-ai-regulation
3. Global AI Policy Review: https://example.com/global-ai-policy
```

### Example 2: Technical Information
**User**: "How does the new GPT-4 architecture work?"

**AI Response** (with web search):
```
According to recent technical articles, GPT-4 uses a mixture of experts 
architecture with approximately 1.8 trillion parameters. The model combines...

Sources:
1. GPT-4 Architecture Explained: https://example.com/gpt4-arch
2. Technical Deep Dive: https://example.com/gpt4-technical
```

### Example 3: Factual Queries
**User**: "What is the current price of Bitcoin?"

**AI Response** (with web search):
```
According to recent sources, Bitcoin is currently trading at approximately 
$X,XXX USD. The cryptocurrency has seen...

Sources:
1. Bitcoin Price Tracker: https://example.com/btc-price
```

## Best Practices

### When to Use Web Search

✅ **Good Use Cases**:
- Current events and news
- Recent developments in technology
- Up-to-date statistics and data
- Latest research findings
- Product reviews and comparisons
- Real-time information (weather, stocks, etc.)

❌ **Not Recommended For**:
- Basic conversational AI
- General knowledge questions (AI's training is sufficient)
- Creative writing or brainstorming
- Personal advice or opinions

### Optimizing Performance

1. **Use Specific Queries**: More specific search queries yield better results
2. **Combine with AI Context**: Let AI interpret and synthesize results
3. **Limit Results**: Start with 3-5 results for faster responses
4. **Cache Frequent Queries**: Consider caching common searches

## Troubleshooting

### Web Search Not Working

**Issue**: Search endpoint returns errors

**Solutions**:
1. Check internet connection
2. Verify DuckDuckGo is accessible
3. Check Python dependencies: `pip install duckduckgo-search`
4. Review server logs for specific errors

### Slow Response Times

**Issue**: Search & Chat takes too long

**Solutions**:
1. Reduce `max_results` (default: 5)
2. Use a smaller AI model
3. Reduce `max_length` parameter
4. Consider GPU acceleration

### Rate Limiting

**Issue**: Too many requests error

**Solutions**:
1. Add delays between requests
2. Implement request caching
3. Use exponential backoff for retries

## Privacy & Security

### Privacy Benefits

- ✅ **No API Keys Required**: DuckDuckGo search is anonymous
- ✅ **No Tracking**: Searches are not logged or tracked
- ✅ **Local Processing**: AI processing happens on your machine
- ✅ **No Data Sharing**: Nothing is sent to third-party services

### Security Considerations

- 🔒 Always use HTTPS (Ngrok provides this)
- 🔒 Consider adding authentication for production use
- 🔒 Sanitize user inputs to prevent injection attacks
- 🔒 Rate limit requests to prevent abuse

## Comparison with Other Frameworks

| Feature | This Implementation | LangChain | AutoGPT | Perplexity |
|---------|-------------------|-----------|---------|------------|
| **Self-Hosted** | ✅ Yes | ⚠️ Optional | ⚠️ Optional | ❌ No |
| **Privacy** | ✅ 100% Private | ⚠️ Depends | ⚠️ Depends | ❌ Shared |
| **No API Keys** | ✅ None needed | ❌ Required | ❌ Required | ❌ Required |
| **Cost** | ✅ FREE | 💰 Varies | 💰 Varies | 💰 Subscription |
| **Web Search** | ✅ Built-in | ✅ Plugin | ✅ Built-in | ✅ Built-in |
| **Easy Setup** | ✅ 15 minutes | ⚠️ Complex | ⚠️ Complex | ✅ Easy |
| **Customizable** | ✅ Full control | ✅ Full control | ✅ Full control | ❌ Limited |

## Advanced Features

### Custom Search Sources

You can extend the search functionality to include other sources:

```python
def search_multiple_sources(query):
    """Search multiple sources and combine results"""
    results = []
    
    # DuckDuckGo search
    ddg_results = search_web(query)
    results.extend(ddg_results)
    
    # Add custom sources here
    # wikipedia_results = search_wikipedia(query)
    # results.extend(wikipedia_results)
    
    return results
```

### Result Filtering

Filter search results based on criteria:

```python
def filter_results(results, min_relevance=0.5):
    """Filter results based on relevance"""
    filtered = []
    for result in results:
        # Add your filtering logic
        if is_relevant(result, min_relevance):
            filtered.append(result)
    return filtered
```

### Caching Search Results

Implement caching for frequently searched topics:

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_search(query):
    """Cache search results for common queries"""
    return search_web(query)
```

## Future Enhancements

Planned improvements:

- [ ] **Multi-source Search**: Combine multiple search engines
- [ ] **Image Search**: Add support for image search results
- [ ] **News Search**: Dedicated news search endpoint
- [ ] **Search History**: Track and display search history
- [ ] **Advanced Filtering**: Filter by date, domain, etc.
- [ ] **Custom Search Engines**: Add support for specialized searches
- [ ] **Result Ranking**: Implement relevance-based ranking
- [ ] **Query Expansion**: Automatically expand queries for better results

## Support & Resources

### Documentation
- [Main README](README.md)
- [Local Server Setup](LOCAL_SERVER_SETUP.md)
- [API Documentation](local_ai_server/README.md)

### Getting Help
- Check [Troubleshooting](TROUBLESHOOTING.md)
- Review server logs for errors
- Open an issue on GitHub

### Community
- Share your use cases
- Contribute improvements
- Report bugs and suggestions

## Acknowledgments

This implementation draws inspiration from:
- **LangChain**: Tool-based architecture for AI agents
- **AutoGPT**: Autonomous agent design patterns
- **Perplexity AI**: Search + AI synthesis approach
- **DuckDuckGo**: Privacy-focused search engine

## License

This feature is part of the AI Assistant Android App project and is available under the MIT License.
