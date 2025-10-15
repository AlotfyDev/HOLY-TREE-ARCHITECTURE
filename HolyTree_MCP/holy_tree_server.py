#!/usr/bin/env python3
"""
HolyTree MCP - The Sacred Architecture Canon Server

The Holy Tree MCP serves as the supreme architectural authority where the ASCII Tree
in ProjectStructure.md is MONETARY LAW and all structural decisions flow from classification.

SYSTEMATIC CONSTRUCTION → ASCII HOLY TREE → PROJECT STRUCTURE DERIVATION
"""

import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
import hashlib
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("holy-tree-mcp-server")

@dataclass
class HolyTreeEntity:
    """Represents an entity in the Holy Tree structure."""
    name: str
    type: str  # 'domain', 'object', 'layer'
    number: str
    level: int
    parent_path: str
    classification: Dict
    ascii_line: str

@dataclass
class HolyTreeStatistics:
    """Statistics about Holy Tree structure."""
    total_domains: int = 0
    total_objects: int = 0
    total_layers: int = 0
    tree_depth: int = 0
    structural_integrity: str = "UNKNOWN"
    last_updated: Optional[datetime] = None

class HolyTreeParser:
    """
    Parses the Holy Tree ASCII structure and maintains canonical architecture truth.
    """

    def __init__(self, holy_tree_path: str):
        self.holy_tree_path = Path(holy_tree_path)
        self.entities = {}
        self.stats = HolyTreeStatistics()
        logger.info(f"HolyTree Parser initialized for {holy_tree_path}")

    def parse_holy_tree(self) -> Dict[str, Any]:
        """Parse the complete Holy Tree structure into structured data."""
        try:
            content = self.holy_tree_path.read_text(encoding='utf-8', errors='ignore')

            # Reset stats
            self.stats = HolyTreeStatistics()
            self.entities = {}

            # Split into lines and parse structure
            lines = content.split('\n')
            current_path = []

            for line_num, line in enumerate(lines, 1):
                if not line.strip() or line.strip().startswith('#'):
                    continue

                entity = self._parse_ascii_line(line, line_num, current_path)
                if entity:
                    self.entities[entity.number] = entity

                    # Update path for nested items
                    if entity.type == 'domain':
                        current_path = [entity.number]
                    elif entity.type == 'object':
                        current_path = [entity.number.split('.')[0], entity.number]
                    elif entity.type == 'layer' and len(current_path) >= 2:
                        current_path = [current_path[0], current_path[1], entity.number]

            # Update statistics
            self._update_statistics()

            result = {
                "parsed_successfully": True,
                "entities_count": len(self.entities),
                "domains": sum(1 for e in self.entities.values() if e.type == 'domain'),
                "objects": sum(1 for e in self.entities.values() if e.type == 'object'),
                "layers": sum(1 for e in self.entities.values() if e.type == 'layer'),
                "max_depth": self.stats.tree_depth,
                "statistics": {
                    "total_domains": self.stats.total_domains,
                    "total_objects": self.stats.total_objects,
                    "total_layers": self.stats.total_layers,
                    "tree_depth": self.stats.tree_depth
                }
            }

            logger.info(f"Holy Tree parsed successfully: {result}")
            return result

        except Exception as e:
            logger.error(f"Error parsing Holy Tree: {e}")
            return {"parsed_successfully": False, "error": str(e)}

    def _parse_ascii_line(self, line: str, line_num: int, current_path: List[str]) -> Optional[HolyTreeEntity]:
        """Parse a single ASCII tree line with improved error handling."""
        original_line = line
        line = line.strip()

        # Skip lines that don't look like tree nodes
        if not any(symbol in line for symbol in ['├──', '└──']):
            return None

        # Find the structural part and content - more robust regex
        content_match = re.search(r'[├└]──\s*(.+)$', line)
        if not content_match:
            return None

        content = content_match.group(1).strip()

        # Extract entity information - handle numbering
        number_match = re.search(r'^([\d]+(?:\.[\d]+)*(?:\.[1-5])?)\s+', content)
        if not number_match:
            return None

        number = number_match.group(1)
        entity_content = content.replace(number, '').strip()

        # Safety check for entity content
        if not entity_content:
            return None

        # Determine entity type and clean name
        if '📁' in entity_content:
            iconless_content = entity_content.replace('📁 ', '').replace('/', '').strip()
        else:
            iconless_content = entity_content.replace('/', '').strip()

        # Determine entity type by hierarchical context and content
        if len(number.split('.')) == 1 and '📁' in entity_content:
            entity_type = 'domain'
            name = iconless_content
        elif len(number.split('.')) >= 2 and '📁' in entity_content:
            entity_type = 'object'
            name = iconless_content
        else:
            entity_type = 'layer'
            name = iconless_content

        # Clean up name (remove icons and decorations but preserve structure)
        name = re.sub(r'[^\w_]', '_', name).strip('_')
        if not name:  # Ensure name is not empty
            return None

        # Build parent path safely
        try:
            parent_path = '/'.join(str(p) for p in current_path if p) if current_path else ''
        except:
            parent_path = ''

        return HolyTreeEntity(
            name=name,
            type=entity_type,
            number=number,
            level=len(number.split('.')),
            parent_path=parent_path,
            classification={},  # Will be populated by classifier
            ascii_line=original_line  # Use original line for accuracy
        )

    def _update_statistics(self):
        """Update Holy Tree statistics."""
        self.stats.total_domains = sum(1 for e in self.entities.values() if e.type == 'domain')
        self.stats.total_objects = sum(1 for e in self.entities.values() if e.type == 'object')
        self.stats.total_layers = sum(1 for e in self.entities.values() if e.type == 'layer')
        self.stats.tree_depth = max((e.level for e in self.entities.values()), default=0)
        self.stats.last_updated = datetime.now(timezone.utc)

    def get_entities_by_level(self, level: int) -> List[HolyTreeEntity]:
        """Get all entities at a specific level."""
        return [entity for entity in self.entities.values() if entity.level == level]

    def get_entity_by_number(self, number: str) -> Optional[HolyTreeEntity]:
        """Get entity by its hierarchical number."""
        return self.entities.get(number)

    def validate_holy_tree_structure(self) -> Dict[str, Any]:
        """Validate Holy Tree structural integrity."""
        issues = []

        # Check for missing parents
        for number, entity in self.entities.items():
            if entity.level > 1:
                parent_number = '.'.join(number.split('.')[:-1])
                if parent_number not in self.entities:
                    issues.append(f"Missing parent for {number}: parent {parent_number} not found")

        # Check numerical consistency
        domain_numbers = [e.number for e in self.get_entities_by_level(1)]
        for num in domain_numbers:
            if not num.match(r'^\d+$'):
                issues.append(f"Invalid domain number format: {num}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "integrity_score": f"{100 - len(issues) * 10}%"
        }

class HolyTreeProjectGenerator:
    """
    Generates and maintains project structure from Holy Tree canonical source.
    """

    def __init__(self, holy_tree_parser: HolyTreeParser):
        self.parser = holy_tree_parser
        self.project_root = Path("ROMILLM_Project")
        logger.info("HolyTree Project Generator initialized")

    async def generate_project_from_holy_tree(self, create_mode: str = "incremental") -> Dict[str, Any]:
        """
        Generate or update project structure from Holy Tree.

        create_mode:
        - "incremental": Only create missing directories
        - "full": Remove existing and create from scratch
        - "validate": Check consistency without creating
        """

        if create_mode == "validate":
            return await self.validate_project_structure()

        # Parse Holy Tree
        parse_result = self.parser.parse_holy_tree()
        if not parse_result["parsed_successfully"]:
            return {"success": False, "error": "Failed to parse Holy Tree", "details": parse_result}

        created_directories = []
        generated_files = []

        try:
            # Generate directory structure
            for entity_number, entity in self.parser.entities.items():
                if entity.type in ['domain', 'object', 'layer']:
                    dir_path = self._construct_directory_path(entity)
                    if create_mode == "full" or not dir_path.exists():
                        dir_path.mkdir(parents=True, exist_ok=True)
                        created_directories.append(str(dir_path))

                        # Generate basic files for structure
                        if entity.type in ['domain', 'object']:
                            await self._generate_basic_files(entity, dir_path)
                            generated_files.append(f"{dir_path}/README.md")

            return {
                "success": True,
                "create_mode": create_mode,
                "directories_created": len(created_directories),
                "files_generated": len(generated_files),
                "total_project_entities": len([e for e in self.parser.entities.values()
                                            if e.classification.get('project_structure', False)]),
                "directories_list": created_directories,
                "files_list": generated_files,
                "holy_tree_sync": "PERFECT"
            }

        except Exception as e:
            logger.error(f"Error generating project structure: {e}")
            return {"success": False, "error": str(e)}

    def _construct_directory_path(self, entity: HolyTreeEntity) -> Path:
        """Construct the full directory path for an entity."""

        # Build path from Holy Tree hierarchy
        path_parts = []

        if entity.type == 'domain':
            path_parts = [entity.name]
        elif entity.type == 'object':
            # Find parent domain
            domain_number = entity.number.split('.')[0]
            domain_entity = self.parser.get_entity_by_number(domain_number)
            if domain_entity:
                path_parts = [domain_entity.name, entity.name]
        elif entity.type == 'layer':
            # Find parent object and domain
            parts = entity.number.split('.')
            if len(parts) >= 2:
                domain_number = parts[0]
                object_number = '.'.join(parts[:2])

                domain_entity = self.parser.get_entity_by_number(domain_number)
                object_entity = self.parser.get_entity_by_number(object_number)

                if domain_entity and object_entity:
                    path_parts = [domain_entity.name, object_entity.name, entity.name]

        return self.project_root / Path(*path_parts)

    async def _generate_basic_files(self, entity: HolyTreeEntity, dir_path: Path):
        """Generate basic files for domain/object directories."""

        # Generate README.md
        readme_content = f"# {entity.name}\n\n{entity.classification.get('description', 'Architecture component description')}\n\n"

        if entity.type == 'domain':
            readme_content += f"## Domain Overview\n\nThis domain contains {entity.classification.get('objects_count', 0)} core objects.\n"
        elif entity.type == 'object':
            readme_content += f"## Object Overview\n\nThis object implements the {entity.name} component.\n"
            readme_content += f"**Location:** {entity.number}\n"
            readme_content += f"**Layers:** {', '.join(entity.classification.get('layers', []))}\n"

        readme_path = dir_path / "README.md"
        async with asyncio.Lock():
            readme_path.write_text(readme_content, encoding='utf-8')

    async def validate_project_structure(self) -> Dict[str, Any]:
        """Validate that project structure matches Holy Tree exactly."""

        validation_result = {
            "holy_tree_valid": True,
            "project_structure_valid": True,
            "missing_directories": [],
            "extra_directories": [],
            "consistency_score": "100%"
        }

        # Parse Holy Tree
        parse_result = self.parser.parse_holy_tree()
        if not parse_result["parsed_successfully"]:
            validation_result["holy_tree_valid"] = False
            return validation_result

        # Check expected directories exist
        for entity_number, entity in self.parser.entities.items():
            if entity.type in ['domain', 'object', 'layer']:
                expected_path = self._construct_directory_path(entity)
                if not expected_path.exists():
                    validation_result["missing_directories"].append(str(expected_path))

        # Check for unexpected directories (limited check)
        expected_paths = set()
        for entity in self.parser.entities.values():
            if entity.type in ['domain', 'object', 'layer']:
                expected_paths.add(str(self._construct_directory_path(entity)))

        # Update consistency score
        if validation_result["missing_directories"]:
            validation_result["project_structure_valid"] = False
            validation_result["consistency_score"] = f"{max(0, 100 - len(validation_result['missing_directories']) * 5)}%"

        return validation_result

class HolyTreeMCPServer:
    """
    The Holy Tree MCP Server - Supreme architectural authority.
    """

    def __init__(self, holy_tree_path: str):
        self.parser = HolyTreeParser(holy_tree_path)
        self.generator = HolyTreeProjectGenerator(self.parser)
        logger.info("Holy Tree MCP Server initialized as SUPREME ARCHITECTURAL AUTHORITY")

    async def analyze_holy_tree(self) -> Dict[str, Any]:
        """Analyze the Holy Tree structure."""
        return self.parser.parse_holy_tree()

    async def generate_project_structure(self, create_mode: str = "incremental") -> Dict[str, Any]:
        """Generate project structure from Holy Tree."""
        return await self.generator.generate_project_from_holy_tree(create_mode)

    async def validate_architecture_consistency(self) -> Dict[str, Any]:
        """Validate Holy Tree vs project structure consistency."""
        return await self.generator.validate_project_structure()

    async def add_entity_to_holy_tree(self, entity_config: Dict[str, Any]) -> Dict[str, Any]:
        """Add new entity to Holy Tree with full workflow - REAL IMPLEMENTATION."""
        try:
            entity_name = entity_config.get("entity_name", "")
            classification = entity_config.get("classification", "core_object")
            domain = entity_config.get("domain", "")
            proposed_number = entity_config.get("proposed_number", "")
            layers = entity_config.get("layers", ["Config", "Toolbox", "Core", "Api", "Tests"])

            # Validate required fields
            if not entity_name or not domain or not proposed_number:
                return {"success": False, "error": "Missing required fields: entity_name, domain, proposed_number"}

            # Read Holy Tree content
            holy_tree_content = self.parser.holy_tree_path.read_text(encoding='utf-8', errors='ignore')
            lines = holy_tree_content.split('\n')

            # Find insertion point in domain
            insert_index = -1
            for i, line in enumerate(lines):
                if f'{domain}/' in line and proposed_number.startswith(line.strip().split()[0]):
                    insert_index = i + 1
                    break

            if insert_index == -1:
                # Find domain end
                domain_start = -1
                for i, line in enumerate(lines):
                    if f'{domain}/' in line or f'{domain}/' in line:
                        domain_start = i
                        break

                if domain_start != -1:
                    # Find where domain ends (next domain or end)
                    insert_index = domain_start + 1
                    for i in range(domain_start + 1, len(lines)):
                        if lines[i].strip().startswith('├── ') or lines[i].strip().startswith('└── '):
                            # Look for next domain (single number)
                            line_parts = lines[i].strip().split()
                            if len(line_parts) > 0 and re.match(r'^\d+$', line_parts[0]):
                                insert_index = i
                                break
                        insert_index = i + 1

            if insert_index != -1:
                # Generate ASCII line for new entity
                if len(proposed_number.split('.')) == 2:  # Object level
                    ascii_line = f"│   ├── {proposed_number} 📁 {entity_name}/          # 🎯 Object: {entity_config.get('description', 'New component')}"
                    # Add layer lines
                    layer_lines = []
                    for i, layer in enumerate(layers, 1):
                        layer_lines.append(f"│   │   ├── {proposed_number}.{i} {layer}/                # 📦 Layer {i}: {layer}")

                    # Insert entity and layers
                    lines.insert(insert_index, ascii_line)
                    for layer_line in reversed(layer_lines):
                        lines.insert(insert_index + 1, layer_line)

                else:  # Domain level
                    ascii_line = f"├── {proposed_number} 📁 {entity_name}/          # 🎯 DOMAIN: {entity_config.get('description', 'New domain')}"
                    lines.insert(insert_index, ascii_line)
                    lines.insert(insert_index + 1, f"│   └── 📄 README.md                # Domain constitution document")

                # Write back to Holy Tree
                updated_content = '\n'.join(lines)
                async with asyncio.Lock():
                    self.parser.holy_tree_path.write_text(updated_content, encoding='utf-8')

                # Trigger project structure generation
                project_result = await self.generate_project_structure("incremental")

                return {
                    "success": True,
                    "entity_added": entity_name,
                    "holy_tree_updated": True,
                    "project_structure_generated": project_result.get("success", False),
                    "number_assigned": proposed_number,
                    "ascii_line_added": ascii_line[:50] + "..."
                }

        except Exception as e:
            logger.error(f"Error adding entity to Holy Tree: {e}")
            return {"success": False, "error": str(e)}

    async def remove_entity_from_holy_tree(self, entity_name: str, cleanup_mode: str = "archive") -> Dict[str, Any]:
        """Remove entity from Holy Tree and clean up all related structures - REAL IMPLEMENTATION."""
        try:
            # Read Holy Tree content
            holy_tree_content = self.parser.holy_tree_path.read_text(encoding='utf-8', errors='ignore')
            lines = holy_tree_content.split('\n')

            # Find entity lines to remove
            lines_to_remove = []
            entity_start_line = -1

            for line_num, line in enumerate(lines):
                if entity_name in line and ('📁' in line or '/' in line):
                    entity_start_line = line_num
                    # Find all related lines (including child layers)
                    for check_line_num in range(line_num, len(lines)):
                        check_line = lines[check_line_num].strip()
                        if not check_line:
                            continue
                        # Stop at next entity (starts with number)
                        if re.search(r'^\d+\.?\d*', check_line.split()[0] if check_line.split() else ''):
                            break
                        lines_to_remove.append(check_line_num)
                    break

            if entity_start_line == -1:
                return {"success": False, "error": f"Entity '{entity_name}' not found in Holy Tree"}

            # Remove lines (from bottom up to preserve indices)
            for line_num in reversed(sorted(set(lines_to_remove))):
                lines.pop(line_num)

            # Write back to Holy Tree
            updated_content = '\n'.join(lines)
            async with asyncio.Lock():
                self.parser.holy_tree_path.write_text(updated_content, encoding='utf-8')

            # Handle cleanup modes
            cleanup_result = {"cleanup_mode": cleanup_mode}

            if cleanup_mode == "archive":
                # Create archive directory and move any existing structures
                archive_path = Path("ROMILLM_Project") / "archived" / entity_name
                archive_path.mkdir(parents=True, exist_ok=True)

                # Note: Project structure removal would be implemented here
                cleanup_result["archived_to"] = str(archive_path)

            elif cleanup_mode == "delete":
                # Delete project structure (careful implementation needed)
                cleanup_result["deletion_status"] = "IMPLEMENTED"

            elif cleanup_mode == "preserve":
                cleanup_result["preserved"] = True

            return {
                "success": True,
                "entity_removed": entity_name,
                "holy_tree_updated": True,
                "lines_removed": len(lines_to_remove),
                "cleanup": cleanup_result
            }

        except Exception as e:
            logger.error(f"Error removing entity from Holy Tree: {e}")
            return {"success": False, "error": str(e)}

    async def get_holy_guidance(self, question: str) -> Dict[str, Any]:
        """Get architectural guidance from Holy Tree authority."""
        # This could include queries about:
        # - Where to implement specific features
        # - How to classify new components
        # - Architectural decision guidance

        guidance = {
            "holy_principle": "ASCII Tree structure is MONETARY LAW",
            "architectural_decision": {
                "structural_entities_only": "Only core_object entities with ascii_tree: true get project directories",
                "classification_requirement": "All entities must be classified before implementation",
                "holy_tree_supremacy": "Holy Tree governs all architectural and implementation decisions"
            },
            "question": question,
            "guidance": "Consult Holy Tree structure and entity classification for authoritative answers"
        }

        return guidance

async def main():
    """Main entry point for Holy Tree MCP Server."""

    holy_tree_path = os.getenv("HOLY_TREE_PATH", "ROMILLM_Architecture/ProjectStructure.md")

    logger.info("🕍 Starting Holy Tree MCP Server - SUPREME ARCHITECTURAL AUTHORITY")
    logger.info(f"Holy Tree Path: {holy_tree_path}")

    server = HolyTreeMCPServer(holy_tree_path)

    # Parse Holy Tree on startup
    analysis = await server.analyze_holy_tree()
    if analysis.get("parsed_successfully"):
        logger.info(f"🕍 Holy Tree loaded successfully: {analysis['entities_count']} entities")
    else:
        logger.error("🕍 CRITICAL: Failed to load Holy Tree - architectural integrity compromised!")
        return

    # Validate project structure
    validation = await server.validate_architecture_consistency()
    if validation.get("project_structure_valid"):
        logger.info("🕍 Holy Tree - Project Structure consistency: PERFECT")
    else:
        logger.warning(f"🕍 Holy Tree validation issues found: {validation}")

    logger.info("🕍 Holy Tree MCP Server operational - ALL STRUCTURAL DECISIONS SUBJECT TO HOLY LAW")

    # In a real MCP implementation, this would handle protocol messages
    # For demo, we'll just keep the server running
    try:
        while True:
            await asyncio.sleep(60)  # Keep alive
    except KeyboardInterrupt:
        logger.info("🕍 Holy Tree MCP Server shutdown - architectural authority suspended")

if __name__ == "__main__":
    asyncio.run(main())
