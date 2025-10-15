#!/usr/bin/env python3
"""
Documentation MCP Server - Real-Time Hyperlinked Entity Documentation System

Creates a live, hyperlinked documentation system that connects entity mentions in documents
to Knowledge Graph nodes, providing real-time architectural navigation and cross-referencing.

This server transforms ROMILLM documentation into a living, breathing intelligence system.
"""

import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
import time
import hashlib
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("documentation-mcp-server")

# MCP Protocol Implementation (Simplified)
class MCPClient:
    """Simplified MCP client for communicating with Knowledge Graph server."""

    def __init__(self, server_uri: str):
        self.server_uri = server_uri
        logger.info(f"Initialized MCP client for {server_uri}")

        # Entity Classification System - Core Reference for Structural Decisions
        self.entity_classifications = {
            # Category A: Core Objects (Require Project Structure + 5-Layer Architecture)
            "ROMILLM": {
                "type": "core_object", "classification": "ROMILLM_Architecture",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "layers": ["Config", "Toolbox", "Core", "Api", "Tests"],
                "description": "Root cognitive intelligence system"
            },
            "Ingestion_Pipeline": {
                "type": "core_object", "classification": "ROMILLM_Domain",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": 2,
                "description": "Document parsing & entity extraction"
            },
            "Document_Parser": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "2.1",
                "description": "Multi-format document processing"
            },
            "Entity_Extractor": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "2.2",
                "description": "NLP entity recognition & classification"
            },
            "Content_Chunker": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "2.3",
                "description": "Semantic text segmentation"
            },
            "Pipeline_Manager": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "1.1",
                "description": "End-to-end processing coordination"
            },
            "Memory_Manager": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "1.2",
                "description": "Resource allocation & optimization"
            },
            "Graph_Constructor": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "3.1",
                "description": "Entity-relationship knowledge building"
            },
            "Graph_Algorithms": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "3.2",
                "description": "Centrality, clustering, path finding"
            },
            "Relationship_Fusion": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "3.3",
                "description": "Multi-source relationship integration"
            },
            "Intent_Classifier": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "4.1",
                "description": "Query intent analysis & categorization"
            },
            "Processing_Router": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "4.2",
                "description": "Deterministic routing based on intent"
            },
            "Content_Filter": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "4.3",
                "description": "Query-relevant content filtering"
            },
            "Template_Generator": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "5.1",
                "description": "Deterministic response template creation"
            },
            "Response_Builder": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "5.2",
                "description": "Structured response assembly"
            },
            "Format_Optimizer": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "5.3",
                "description": "Response formatting & performance tuning"
            },
            "Vector_Retriever": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "6.1",
                "description": "Semantic similarity search"
            },
            "Graph_Traverser": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "6.2",
                "description": "Relationship-based retrieval"
            },
            "Result_Fusion": {
                "type": "core_object", "classification": "ROMILLM_Object",
                "project_structure": True, "ascii_tree": True,
                "hyperlink": True, "domain_number": "6.3",
                "description": "Hybrid search result combination"
            },
            "Base_Types": {
                "type": "core_object", "classification": "ROMILLM_Infrastructure",
                "project_structure": True, "ascii_tree": False,  # Infrastructure objects don't get ASCII tree entries
                "hyperlink": True, "layers": ["Config", "Toolbox", "Core", "Api", "Tests"],
                "description": "Core type definitions & interfaces"
            },
            "Error_Handling": {
                "type": "core_object", "classification": "ROMILLM_Infrastructure",
                "project_structure": True, "ascii_tree": False,
                "hyperlink": True, "layers": ["Config", "Toolbox", "Core", "Api", "Tests"],
                "description": "Comprehensive error management"
            },
            "Performance_Monitor": {
                "type": "core_object", "classification": "ROMILLM_Infrastructure",
                "project_structure": True, "ascii_tree": False,
                "hyperlink": True, "layers": ["Config", "Toolbox", "Core", "Api", "Tests"],
                "description": "System performance tracking"
            },
            "Communication_Protocol": {
                "type": "core_object", "classification": "ROMILLM_Infrastructure",
                "project_structure": True, "ascii_tree": False,
                "hyperlink": True, "layers": ["Config", "Toolbox", "Core", "Api", "Tests"],
                "description": "Inter-component messaging"
            },

            # Category B: Conceptual Entities (Documentation Only, No Project Structure)
            "GraphRAG": {
                "type": "conceptual_entity", "classification": "Documentation_Concept",
                "project_structure": False, "ascii_tree": False,
                "hyperlink": True, "reason": "Represents alternative RAG approach, not ROMILLM structural object"
            },
            "DSPy": {
                "type": "conceptual_entity", "classification": "External_Framework",
                "project_structure": False, "ascii_tree": False,
                "hyperlink": True, "reason": "External LLM programming framework"
            },
            "Ollama": {
                "type": "conceptual_entity", "classification": "External_Tool",
                "project_structure": False, "ascii_tree": False,
                "hyperlink": True, "reason": "External local LLM execution tool"
            },

            # Category C: Waitlist Entities (Future Structural, Flagged for Later)
            "Automated_Documentation_Generator": {
                "type": "waitlist_entity", "classification": "Future_Component",
                "project_structure": False, "ascii_tree": False,
                "hyperlink": True, "reason": "Planned component for automated doc generation"
            },

            # Category D: Blacklist Entities (External/Non-ROMILLM, Limited Linking)
            "LangChain": {
                "type": "blacklist_entity", "classification": "External_Framework",
                "project_structure": False, "ascii_tree": False,
                "hyperlink": False, "reason": "External framework, not core to ROMILLM"
            }
        }

    async def query_graph_node(self, entity_name: str) -> Optional[Dict]:
        """Query Knowledge Graph for entity details with classification."""
        # Return classification-based entity information
        classification = self.entity_classifications.get(entity_name)
        if classification:
            return {
                "name": entity_name,
                "classification": classification.get("classification", "Unknown"),
                "type": classification.get("type", "unknown"),
                "description": classification.get("description", "Entity description"),
                "project_structure_required": classification.get("project_structure", False),
                "ascii_tree_included": classification.get("ascii_tree", False),
                "domain_number": classification.get("domain_number", "N/A"),
                "layers": classification.get("layers", []),
                "reason": classification.get("reason", "")
            }

        return None

    def get_entity_classification(self, entity_name: str) -> Dict:
        """Get detailed classification information for an entity."""
        return self.entity_classifications.get(entity_name, {
            "type": "unknown",
            "project_structure": False,
            "ascii_tree": False,
            "hyperlink": False,
            "classification": "Unclassified",
            "reason": "Entity not found in classification system"
        })

    def is_structural_entity(self, entity_name: str) -> bool:
        """Determine if entity requires project structure."""
        classification = self.get_entity_classification(entity_name)
        return classification.get("project_structure", False)

    def is_hyperlinkable(self, entity_name: str) -> bool:
        """Determine if entity should be hyperlinked."""
        classification = self.get_entity_classification(entity_name)
        return classification.get("hyperlink", False)

@dataclass
class EntityMention:
    """Represents a detected entity mention in documentation."""
    name: str
    line: int
    start_pos: int
    end_pos: int
    context: str
    surrounding_text: str

@dataclass
class Hyperlink:
    """Represents a generated hyperlink for an entity."""
    text: str
    href: str
    line: int
    context: str
    entity_details: Dict

class DocumentationMCPServer:
    """
    Real-time documentation server with hyperlinked entities.

    Continuously monitors documentation files, detects entity mentions,
    maps them to Knowledge Graph nodes, and maintains live hyperlinks.
    """

    def __init__(self, doc_root: str, kg_server_uri: str, update_interval: int = 5):
        self.doc_root = Path(doc_root)
        self.update_interval = update_interval
        self.kg_client = MCPClient(kg_server_uri)
        self.document_hashes = {}  # Track file changes
        self.hyperlinked_docs = {}  # Store generated hyperlinked versions

        logger.info(f"Documentation MCP Server initialized with doc_root: {doc_root}")

    async def run_server(self):
        """Main server loop - continuously monitors and updates documentation."""
        logger.info("Starting real-time documentation server...")

        while True:
            try:
                await self.update_documentation_cycle()
                await asyncio.sleep(self.update_interval)
            except Exception as e:
                logger.error(f"Error in documentation update cycle: {e}")
                await asyncio.sleep(1)  # Brief pause before retry

    async def update_documentation_cycle(self):
        """One complete cycle of documentation monitoring and updating."""

        # Find all markdown files
        markdown_files = list(self.doc_root.glob("**/*.md"))
        logger.debug(f"Found {len(markdown_files)} markdown files to process")

        # Check for changes and update hyperlinks
        for doc_path in markdown_files:
            if await self.has_document_changed(doc_path):
                await self.update_document_hyperlinks(doc_path)
                logger.debug(f"Updated hyperlinks for {doc_path}")

    async def has_document_changed(self, doc_path: Path) -> bool:
        """Check if document has changed since last processing."""
        try:
            current_content = doc_path.read_text(encoding='utf-8', errors='ignore')
            current_hash = hashlib.md5(current_content.encode()).hexdigest()

            previous_hash = self.document_hashes.get(str(doc_path))
            if previous_hash != current_hash:
                self.document_hashes[str(doc_path)] = current_hash
                return True

            return False
        except Exception as e:
            logger.warning(f"Error checking changes for {doc_path}: {e}")
            return False

    async def update_document_hyperlinks(self, doc_path: Path):
        """Update hyperlinks in a specific document."""
        try:
            # Read document
            content = doc_path.read_text(encoding='utf-8', errors='ignore')

            # Extract entities
            entities = await self.extract_entities_from_document(doc_path, content)

            # Generate hyperlinks
            hyperlinks = await self.generate_hyperlinks(entities)

            # Insert hyperlinks into content
            updated_content = self.insert_hyperlinks(content, hyperlinks)

            # Save hyperlinked version
            self.save_hyperlinked_document(doc_path, updated_content)

            logger.debug(f"Generated {len(hyperlinks)} hyperlinks for {doc_path}")

        except Exception as e:
            logger.error(f"Error updating hyperlinks for {doc_path}: {e}")

    async def extract_entities_from_document(self, doc_path: Path, content: str) -> List[EntityMention]:
        """Extract entity mentions from document content."""

        entities = []

        # Define entity patterns (expand as needed)
        entity_patterns = [
            r'\b(Injection_Pipeline|Knowledge_Graph_Processing|Deterministic_Routing_Engine|Template_Generation_System|Hybrid_Search_Fusion_Engine|Core_Orchestration_Framework)\b',
            r'\b(Doc(ument_)?Parser|Entity_Extractor|Content_Chunker)\b',
            r'\b(Graph_Constructor|Graph_Algorithms|Relationship_Fusion)\b',
            r'\b(Intent_Classifier|Processing_Router|Content_Filter)\b',
            r'\b(Template_Generator|Response_Builder|Format_Optimizer)\b',
            r'\b(Vector_Retriever|Graph_Traverser|Result_Fusion)\b',
            r'\b(Pipeline_Manager|Memory_Manager)\b',
            r'\b(ROMILLM|ROMILLM_Architecture)\b',
        ]

        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for pattern in entity_patterns:
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    # Check if not already inside a link
                    if not self.is_inside_markdown_link(line, match.start(), match.end()):
                        entity = EntityMention(
                            name=match.group(),
                            line=line_num,
                            start_pos=match.start(),
                            end_pos=match.end(),
                            context=self.determine_context(line, match.group()),
                            surrounding_text=line[max(0, match.start()-50):min(len(line), match.end()+50)]
                        )
                        entities.append(entity)

        return entities

    def is_inside_markdown_link(self, line: str, start: int, end: int) -> bool:
        """Check if match is already inside a Markdown link."""
        # Check if within [text](url) pattern
        link_start = line.rfind('[', 0, start)
        link_end = line.find(')', start, len(line))

        if link_start != -1 and link_end != -1 and start < link_end:
            # Check for closing ) that comes before an opening [
            if link_start < end:
                return True

        return False

    def determine_context(self, line: str, entity: str) -> str:
        """Determine context of entity mention."""
        line_lower = line.lower()

        if "contains" in line_lower or "includes" in line_lower or "has" in line_lower:
            return "composition"
        elif "uses" in line_lower or "calls" in line_lower or "depends on" in line_lower:
            return "usage"
        elif "layer" in line_lower or "component" in line_lower or "object" in line_lower:
            return "definition"
        elif "manages" in line_lower or "coordinates" in line_lower or "orchestrates" in line_lower:
            return "orchestration"
        else:
            return "reference"

    async def generate_hyperlinks(self, entities: List[EntityMention]) -> List[Hyperlink]:
        """Generate hyperlinks for detected entities."""
        hyperlinks = []

        for entity in entities:
            # Query Knowledge Graph for entity details
            node_details = await self.kg_client.query_graph_node(entity.name)

            if node_details:
                hyperlink = Hyperlink(
                    text=entity.name,
                    href=f"graph://{entity.name}",
                    line=entity.line,
                    context=entity.context,
                    entity_details=node_details
                )
                hyperlinks.append(hyperlink)

        return hyperlinks

    def insert_hyperlinks(self, content: str, hyperlinks: List[Hyperlink]) -> str:
        """Insert hyperlinks into document content."""
        lines = content.split('\n')
        hyperlink_by_line = {}

        # Group hyperlinks by line
        for link in hyperlinks:
            if link.line not in hyperlink_by_line:
                hyperlink_by_line[link.line] = []
            hyperlink_by_line[link.line].append(link)

        # Process each line
        for line_num, line in enumerate(lines, 1):  # 1-indexed
            if line_num in hyperlink_by_line:
                line_hyperlinks = sorted(hyperlink_by_line[line_num], key=lambda x: x.text.count(' '), reverse=True)  # Process longer names first

                for hyperlink in line_hyperlinks:
                    # Skip if already a hyperlink
                    if self.is_inside_markdown_link(line, 0, len(line)):
                        continue

                    # Create Markdown link
                    link_text = f"[{hyperlink.text}]({hyperlink.href})"

                    # Replace first occurrence of the entity name
                    # Use word boundaries to avoid partial replacements
                    pattern = r'\b' + re.escape(hyperlink.text) + r'\b'

                    # Replace only if not already in a link
                    if f"[{hyperlink.text}](" not in line:
                        line = re.sub(pattern, link_text, line, count=1)

                lines[line_num - 1] = line

        return '\n'.join(lines)

    def save_hyperlinked_document(self, doc_path: Path, content: str):
        """Save the hyperlinked version of the document."""
        # Create hyperlinked_docs directory if it doesn't exist
        hyperlinked_dir = Path("hyperlinked_docs")
        hyperlinked_dir.mkdir(exist_ok=True)

        # Mirror the document structure
        relative_path = doc_path.relative_to(self.doc_root)
        hyperlinked_path = hyperlinked_dir / relative_path

        # Create subdirectories if needed
        hyperlinked_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the hyperlinked document
        hyperlinked_path.write_text(content, encoding='utf-8')

        # Store reference
        self.hyperlinked_docs[str(doc_path)] = str(hyperlinked_path)

        logger.info(f"Saved hyperlinked document: {hyperlinked_path}")

async def main():
    """Main entry point with MCP protocol support."""

    doc_root = os.getenv("DOC_ROOT", "ROMILLM_Architecture/")
    kg_server = os.getenv("KG_SERVER", "github.com/modelcontextprotocol/servers/tree/main/src/memory")
    update_interval = int(os.getenv("UPDATE_INTERVAL", "5"))

    logger.info(f"Starting Documentation MCP Server")
    logger.info(f"Document Root: {doc_root}")
    logger.info(f"Knowledge Graph Server: {kg_server}")
    logger.info(f"Update Interval: {update_interval}s")

    server = DocumentationMCPServer(doc_root, kg_server, update_interval)

    # In a real implementation, this would handle MCP protocol messages
    # For now, run the server in continuous mode
    await server.run_server()

if __name__ == "__main__":
    asyncio.run(main())
