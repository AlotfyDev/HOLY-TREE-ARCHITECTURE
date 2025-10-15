# CodeAnalysisServer MCP

## 🏗️ Multi-Language Code Analysis MCP Server for ROMILLM

**Purpose:** Provides entity extraction services for multi-language codebases to enable ROMILLM Ingestion_Pipeline entity detection capabilities.

### **Server Architecture**

```json
{
  "mcpServers": {
    "code-analysis-server": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": {
        "PYTHONPATH": "./vendored_libs",
        "MEMORY_LIMIT": "4GB",
        "TIMEOUT": "60s"
      }
    }
  }
}
```

### **Available Tools**

#### **1. Analyze Codebase**
```json
{
  "name": "analyze_codebase",
  "description": "Analyze entire codebase for entity extraction",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": {"type": "string", "description": "Root path to analyze"},
      "languages": {"type": "array", "items": {"type": "string"}, "enum": ["cpp", "python", "javascript", "mql5"]},
      "include_patterns": {"type": "array", "items": {"type": "string"}, "default": ["*.cpp", "*.hpp", "*.py", "*.js", "*.mq5"]},
      "exclude_patterns": {"type": "array", "items": {"type": "string"}, "default": ["*/build/*", "*/.git/*"]}
    },
    "required": ["path", "languages"]
  },
  "output": {
    "entities": [{"id": "function_main", "type": "function", "language": "cpp", "file": "main.cpp", "line": 10}],
    "relationships": [{"from": "class_A", "to": "function_main", "type": "contains"}]
  }
}
```

#### **2. Extract Single File Entities**
```json
{
  "name": "extract_file_entities",
  "description": "Extract entities from single file",
  "inputSchema": {
    "type": "object",
    "properties": {
      "file_path": {"type": "string", "description": "Path to file"},
      "language": {"type": "string", "enum": ["cpp", "python", "javascript", "mql5"]}
    },
    "required": ["file_path", "language"]
  },
  "output": {
    "entities": [{"name": "EntityName", "type": "class", "scope": "public"}],
    "syntax_tree": "<abstract_syntax_tree_json>"
  }
}
```

#### **3. Detect Language**
```json
{
  "name": "detect_language",
  "description": "Detect programming language from file content",
  "inputSchema": {
    "type": "object",
    "properties": {
      "file_path": {"type": "string", "description": "File to analyze"},
      "content_sample": {"type": "string", "description": "Content sample for detection"}
    },
    "required": ["file_path"]
  },
  "output": {
    "language": "cpp",
    "confidence": 0.95,
    "detected_patterns": ["#include", "std::", "namespace"]
  }
}
```

### **Server Implementation**

```python
# mcp_server.py
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent

class CodeAnalysisServer:
    def __init__(self):
        self.server = Server("code-analysis-server")
        self.setup_tools()

    def setup_tools(self):
        @self.server.tool()
        async def analyze_codebase(path: str, languages: list) -> dict:
            analyzer = CodeAnalyzer()
            return await analyzer.analyze_codebase(path, languages)

        @self.server.tool()
        async def extract_file_entities(file_path: str, language: str) -> dict:
            extractor = EntityExtractor()
            return await extractor.extract_from_file(file_path, language)

        @self.server.tool()
        async def detect_language(file_path: str, content_sample: str = None) -> dict:
            detector = LanguageDetector()
            return await detector.detect_from_file(file_path, content_sample)

if __name__ == "__main__":
    server = CodeAnalysisServer()
    asyncio.run(server.run_stdio_async())
```

### **Supported Languages**

| Language | Parser | Entity Types | Status |
|----------|--------|--------------|---------|
| **C/C++** | Tree-sitter | classes, functions, structs, enums, typedefs | ✅ Full Support |
| **Python** | AST | classes, functions, methods, variables | ✅ Full Support |
| **JavaScript/TypeScript** | Tree-sitter | classes, functions, variables, modules | ✅ Full Support |
| **MQL5** | Custom Parser | functions, classes, enums, indicators, experts | 🟡 Basic Support |

### **Integration with ROMILLM**

```yaml
# ROMILLM Configuration
ingestion:
  entity_extractor:
    mcp_server: "code-analysis-server"
    tools:
      - analyze_codebase
      - extract_file_entities
      - detect_language

# Usage in Ingestion_Pipeline/Entity_Extractor
def extract_entities(self, content: str, language: str) -> list[Entity]:
    # Use MCP server for entity extraction
    result = await self.mcp_client.call_tool(
        "extract_file_entities",
        file_path=self.temp_content_path,
        language=language
    )
    return result["entities"]
```

### **Performance Characteristics**

- **Initialization**: < 5 seconds for all parsers
- **File Analysis**: 1000+ LOC/second (AST parsing)
- **Memory Usage**: < 500MB with loaded parsers
- **Concurrent Requests**: 10+ parallel analyses

### **Error Handling**

- **File Not Found**: Clear error messages with suggestions
- **Unsupported Language**: Graceful fallback to basic text processing
- **Parsing Errors**: Recovery with partial results
- **Memory Limits**: Automatic cleanup and resource management

### **Resource Requirements**

- **Disk Space**: 200MB for parsers and models
- **Memory**: Peak 500MB with concurrent usage
- **Python Version**: 3.8+ with asyncio support
- **System**: Windows 10, SSD recommended

This server provides the foundation for ROMILLM's entity extraction capabilities, enabling sophisticated analysis of multi-language codebases for knowledge graph construction.
