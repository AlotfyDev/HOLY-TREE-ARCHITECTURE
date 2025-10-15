#!/usr/bin/env python3
"""
CodeAnalysisServer MCP - Multi-language code analysis MCP server for ROMILLM

Provides entity extraction capabilities for ROMILLM's Ingestion_Pipeline.
Supports C/C++, Python, JavaScript/TypeScript, and MQL5 codebases.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("code-analysis-server")

class CodeAnalysisServer:
    """
    MCP server providing code analysis and entity extraction capabilities.

    This server enables ROMILLM to extract entities from multi-language codebases,
    supporting the Ingestion_Pipeline/Entity_Extractor component.
    """

    def __init__(self):
        self.supported_languages = {
            "cpp": "C/C++",
            "python": "Python",
            "javascript": "JavaScript/TypeScript",
            "mql5": "MQL5"
        }

        logger.info("CodeAnalysisServer MCP initialized with support for: %s",
                   ", ".join(self.supported_languages.values()))

    async def handle_call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle MCP tool calls for code analysis operations.

        Args:
            name: Tool name (analyze_codebase, extract_file_entities, detect_language)
            arguments: Tool arguments

        Returns:
            Tool execution results
        """
        try:
            if name == "analyze_codebase":
                return await self.analyze_codebase(arguments)
            elif name == "extract_file_entities":
                return await self.extract_file_entities(arguments)
            elif name == "detect_language":
                return await self.detect_language(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            logger.error(f"Error executing tool {name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def analyze_codebase(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze entire codebase for entity extraction.

        Args:
            args: Contains 'path', 'languages', 'include_patterns', 'exclude_patterns'

        Returns:
            Dictionary with extracted entities and relationships
        """
        path = args["path"]
        languages = args.get("languages", ["cpp", "python", "javascript"])
        include_patterns = args.get("include_patterns", ["*.cpp", "*.hpp", "*.py", "*.js", "*.mq5"])
        exclude_patterns = args.get("exclude_patterns", ["*/build/*", "*/.git/*", "*/node_modules/*"])

        logger.info(f"Analyzing codebase at {path} with languages: {languages}")

        all_entities = []
        all_relationships = []

        # Implement recursive directory traversal
        root_path = Path(path)
        if not root_path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")

        # Scan for files matching patterns
        for file_path in self._find_files_recursively(root_path, include_patterns, exclude_patterns):
            try:
                # Detect language for this file
                language = await self._detect_file_language(file_path)

                if language in languages:
                    # Extract entities from this file
                    entities, relationships = await self._extract_entities_from_file(file_path, language)
                    all_entities.extend(entities)
                    all_relationships.extend(relationships)

            except Exception as e:
                logger.warning(f"Failed to process {file_path}: {e}")
                continue

        logger.info(f"Analysis complete: {len(all_entities)} entities, {len(all_relationships)} relationships")

        return {
            "success": True,
            "entities": all_entities,
            "relationships": all_relationships,
            "summary": {
                "total_files_processed": len(all_entities),  # Approximation
                "total_entities": len(all_entities),
                "total_relationships": len(all_relationships)
            }
        }

    async def extract_file_entities(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract entities from a single file.

        Args:
            args: Contains 'file_path', 'language'

        Returns:
            Dictionary with entities and syntax tree
        """
        file_path = args["file_path"]
        language = args.get("language", "auto")

        logger.info(f"Extracting entities from {file_path} ({language})")

        # Auto-detect language if not specified
        if language == "auto":
            language = await self._detect_file_language(Path(file_path))

        entities, relationships = await self._extract_entities_from_file(Path(file_path), language)

        return {
            "success": True,
            "entities": entities,
            "relationships": relationships,
            "language": language,
            "file_path": file_path
        }

    async def detect_language(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect programming language from file content.

        Args:
            args: Contains 'file_path', 'content_sample'

        Returns:
            Dictionary with language detection results
        """
        file_path = args["file_path"]
        content_sample = args.get("content_sample")

        logger.info(f"Detecting language for {file_path}")

        if content_sample is None:
            # Read first few KB from file
            file_path_obj = Path(file_path)
            content_sample = self._read_file_sample(file_path_obj)

        language, confidence, patterns = await self._detect_language_from_content(content_sample)

        return {
            "success": True,
            "language": language,
            "confidence": confidence,
            "detected_patterns": patterns,
            "file_path": file_path
        }

    def _find_files_recursively(self, root_path: Path, include_patterns: List[str],
                               exclude_patterns: List[str]) -> List[Path]:
        """
        Recursively find files matching include patterns while excluding certain directories.

        Note: This is a basic implementation. A full solution would use fnmatch or similar.
        """
        matching_files = []

        def should_exclude(path: Path) -> bool:
            path_str = str(path)
            for exclude_pattern in exclude_patterns:
                if exclude_pattern in path_str:
                    return True
            return False

        def matches_include_pattern(filename: str) -> bool:
            for pattern in include_patterns:
                # Simple glob matching (basic implementation)
                if pattern.startswith("*."):
                    extension = pattern[1:]  # Remove *
                    if filename.endswith(extension):
                        return True
            return False

        for file_path in root_path.rglob("*"):
            if file_path.is_file() and not should_exclude(file_path):
                if matches_include_pattern(file_path.name):
                    matching_files.append(file_path)

        return matching_files

    async def _detect_file_language(self, file_path: Path) -> str:
        """
        Detect language from file extension and content.

        Note: Basic implementation. Production would use more sophisticated detection.
        """
        extension_map = {
            ".cpp": "cpp", ".hpp": "cpp", ".cc": "cpp", ".cxx": "cpp",
            ".py": "python",
            ".js": "javascript", ".ts": "javascript", ".jsx": "javascript",
            ".mq5": "mql5"
        }

        extension = file_path.suffix.lower()
        if extension in extension_map:
            return extension_map[extension]

        # Fallback to content-based detection
        content_sample = self._read_file_sample(file_path)
        language, _, _ = await self._detect_language_from_content(content_sample)
        return language

    def _read_file_sample(self, file_path: Path, max_bytes: int = 1024) -> str:
        """Read first N bytes from file for language detection."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(max_bytes)
        except Exception:
            return ""

    async def _detect_language_from_content(self, content: str) -> tuple[str, float, List[str]]:
        """
        Detect programming language from content sample.

        Note: Very basic implementation. Production would use ML-based detection.
        """
        patterns = []

        # C/C++ patterns
        if any(pattern in content for pattern in ["#include", "std::", "namespace", "class ", "public:", "private:"]):
            patterns.extend(["#include", "std::", "class "])
            cpp_score = len(patterns) / 3.0
            if cpp_score > 0.6:
                return "cpp", min(cpp_score, 1.0), patterns

        # Python patterns
        if any(pattern in content for pattern in ["def ", "import ", "from ", "class ", "self.", "print(", "__init__"]):
            patterns.extend(["def ", "import ", "class "])
            py_score = len(patterns) / 3.0
            if py_score > 0.5:
                return "python", min(py_score, 1.0), patterns

        # JavaScript patterns
        if any(pattern in content for pattern in ["function ", "const ", "let ", "var ", "console.log", "=> {", "export ", "import "]):
            patterns.extend(["function ", "const ", "=> {"])
            js_score = len(patterns) / 3.0
            if js_score > 0.5:
                return "javascript", min(js_score, 1.0), patterns

        # MQL5 patterns
        if any(pattern in content for pattern in ["int OnInit", "void OnTick", "double ", "#property", "MQL5"]):
            patterns.extend(["int OnInit", "void OnTick", "#property"])
            mql5_score = len(patterns) / 3.0
            if mql5_score > 0.6:
                return "mql5", min(mql5_score, 1.0), patterns

        return "unknown", 0.0, patterns

    async def _extract_entities_from_file(self, file_path: Path, language: str) -> tuple[List[Dict], List[Dict]]:
        """
        Extract entities and relationships from a file.

        Note: This is a basic implementation. Production would use actual parsers.
        """
        entities = []
        relationships = []

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            if language == "cpp":
                entities, relationships = self._extract_cpp_entities(content, str(file_path))
            elif language == "python":
                entities, relationships = self._extract_python_entities(content, str(file_path))
            elif language == "javascript":
                entities, relationships = self._extract_javascript_entities(content, str(file_path))
            elif language == "mql5":
                entities, relationships = self._extract_mql5_entities(content, str(file_path))

        except Exception as e:
            logger.warning(f"Failed to extract entities from {file_path}: {e}")

        return entities, relationships

    def _extract_cpp_entities(self, content: str, file_path: str) -> tuple[List[Dict], List[Dict]]:
        """Extract C/C++ entities (basic implementation)"""
        entities = []
        relationships = []

        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Class extraction
            if line.startswith("class "):
                parts = line.split()
                if len(parts) > 1:
                    class_name = parts[1].split('{')[0].split(':')[0].strip()
                    entities.append({
                        "id": f"class_{class_name}",
                        "name": class_name,
                        "type": "class",
                        "language": "cpp",
                        "file": file_path,
                        "line": line_num,
                        "scope": "global"
                    })

            # Function extraction
            elif " " in line and "(" in line and ")" in line and not line.startswith("//"):
                # Very basic function detection
                if "::" in line or " " in line:
                    entities.append({
                        "id": f"function_line_{line_num}",
                        "name": f"function_at_line_{line_num}",
                        "type": "function",
                        "language": "cpp",
                        "file": file_path,
                        "line": line_num,
                        "scope": "global"
                    })

        return entities, relationships

    def _extract_python_entities(self, content: str, file_path: str) -> tuple[List[Dict], List[Dict]]:
        """Extract Python entities (basic implementation)"""
        entities = []
        relationships = []

        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Class extraction
            if line.startswith("class "):
                parts = line.split()
                if len(parts) > 1:
                    class_name = parts[1].split('(')[0].split(':')[0].strip()
                    entities.append({
                        "id": f"class_{class_name}",
                        "name": class_name,
                        "type": "class",
                        "language": "python",
                        "file": file_path,
                        "line": line_num,
                        "scope": "global"
                    })

            # Function extraction
            elif line.startswith("def "):
                func_part = line[4:].split('(')[0].strip()
                entities.append({
                    "id": f"function_{func_part}",
                    "name": func_part,
                    "type": "function",
                    "language": "python",
                    "file": file_path,
                    "line": line_num,
                    "scope": "global"
                })

        return entities, relationships

    def _extract_javascript_entities(self, content: str, file_path: str) -> tuple[List[Dict], List[Dict]]:
        """Extract JavaScript entities (basic implementation)"""
        entities = []
        relationships = []

        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Class extraction
            if line.startswith("class "):
                parts = line.split()
                if len(parts) > 1:
                    class_name = parts[1].split('{')[0].strip()
                    entities.append({
                        "id": f"class_{class_name}",
                        "name": class_name,
                        "type": "class",
                        "language": "javascript",
                        "file": file_path,
                        "line": line_num,
                        "scope": "global"
                    })

            # Function extraction
            elif line.startswith("function "):
                func_part = line[9:].split('(')[0].strip()
                entities.append({
                    "id": f"function_{func_part}",
                    "name": func_part,
                    "type": "function",
                    "language": "javascript",
                    "file": file_path,
                    "line": line_num,
                    "scope": "global"
                })

        return entities, relationships

    def _extract_mql5_entities(self, content: str, file_path: str) -> tuple[List[Dict], List[Dict]]:
        """Extract MQL5 entities (basic implementation)"""
        entities = []
        relationships = []

        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Function extraction (MQL5 specific)
            if ("int " in line or "void " in line or "double " in line) and "(" in line:
                if "OnInit" in line or "OnTick" in line or "OnDeinit" in line:
                    func_name = line.split('(')[0].split()[-1]
                    entities.append({
                        "id": f"function_{func_name}",
                        "name": func_name,
                        "type": "event_handler",
                        "language": "mql5",
                        "file": file_path,
                        "line": line_num,
                        "scope": "global"
                    })

        return entities, relationships


async def run_stdio_async():
    """Run the MCP server using stdio protocol."""
    server = CodeAnalysisServer()

    logger.info("CodeAnalysisServer MCP starting with stdio protocol...")

    # Basic MCP handshake and message loop
    # In production, this would use the official MCP library
    while True:
        try:
            # Read messages from stdin (JSON-RPC format)
            message = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not message:
                break

            # Parse and handle the message
            message_data = json.loads(message.strip())

            if "method" in message_data and message_data["method"] == "initialize":
                # Respond to initialization
                response = {
                    "jsonrpc": "2.0",
                    "id": message_data["id"],
                    "result": {
                        "protocolVersion": "0.1.0",
                        "capabilities": {
                            "tools": {
                                "listChanged": False
                            }
                        },
                        "serverInfo": {
                            "name": "code-analysis-server",
                            "version": "0.1.0"
                        }
                    }
                }
                print(json.dumps(response), flush=True)

            elif "method" in message_data and message_data["method"] == "tools/list":
                # List available tools
                response = {
                    "jsonrpc": "2.0",
                    "id": message_data["id"],
                    "result": {
                        "tools": [
                            {
                                "name": "analyze_codebase",
                                "description": "Analyze entire codebase for entity extraction",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "path": {"type": "string"},
                                        "languages": {"type": "array", "items": {"type": "string"}}
                                    },
                                    "required": ["path", "languages"]
                                }
                            },
                            {
                                "name": "extract_file_entities",
                                "description": "Extract entities from single file",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "file_path": {"type": "string"},
                                        "language": {"type": "string"}
                                    },
                                    "required": ["file_path", "language"]
                                }
                            },
                            {
                                "name": "detect_language",
                                "description": "Detect programming language from file content",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "file_path": {"type": "string"},
                                        "content_sample": {"type": "string"}
                                    },
                                    "required": ["file_path"]
                                }
                            }
                        ]
                    }
                }
                print(json.dumps(response), flush=True)

            elif "method" in message_data and message_data["method"] == "tools/call":
                # Handle tool calls
                params = message_data["params"]
                tool_name = params["name"]
                tool_args = params["arguments"]

                result = await server.handle_call_tool(tool_name, tool_args)

                response = {
                    "jsonrpc": "2.0",
                    "id": message_data["id"],
                    "result": result
                }
                print(json.dumps(response), flush=True)

        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            continue
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            continue


if __name__ == "__main__":
    asyncio.run(run_stdio_async())
