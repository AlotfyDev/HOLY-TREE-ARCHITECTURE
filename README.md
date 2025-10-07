# MQL5 Financial Assets Indexer

[![MQL5](https://img.shields.io/badge/MQL5-5.0+-blue.svg)](https://www.mql5.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/supernova/mql5-indexer)

## 📋 Table of Contents

- [Overview](#overview)
- [🎯 Problem Statement](#-problem-statement)
- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick Start](#-quick-start)
- [📖 Usage Examples](#-usage-examples)
- [🔧 API Reference](#-api-reference)
- [📊 Workflow](#-workflow)
- [🔍 Use Cases](#-use-cases)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 📖 Overview

The **MQL5 Financial Assets Indexer** is a comprehensive solution for automated financial asset management and indexing in MetaTrader 5. This powerful library provides traders, developers, and financial institutions with a robust system to:

- **Automatically discover and catalog** all available financial instruments in the market
- **Create dynamic enumeration systems** for easy asset referencing
- **Export asset data** in multiple formats (JSON, C Structure, Complete Schema)
- **Maintain asset type classification** (FOREX, Stocks, Indices, Commodities, Crypto)
- **Provide real-time asset statistics** and analytics

## 🎯 Problem Statement

In modern algorithmic trading and financial application development, developers frequently face these challenges:

### ❌ Common Issues
- **Manual asset management** - Hard to maintain updated lists of financial instruments
- **Inconsistent asset referencing** - No standardized way to reference assets across different systems
- **Time-consuming enumeration** - Manual creation and maintenance of asset enums
- **Data export limitations** - Difficulty exporting asset data in usable formats
- **Asset type detection** - No automated way to classify financial instruments

### ✅ Our Solution
The MQL5 Financial Assets Indexer solves these problems by providing:

- **Automated asset discovery** and cataloging
- **Dynamic enum generation** with consistent naming
- **Multi-format data export** (JSON, C Struct, Complete Schema)
- **Intelligent asset classification** with 5 asset types
- **Real-time statistics** and asset analytics

## ✨ Key Features

### 🔍 **Automated Asset Discovery**
- Scans all available symbols in the MetaTrader 5 market
- Automatically detects and catalogs financial instruments
- Real-time asset count and availability tracking

### 📊 **Dynamic Enumeration System**
- Auto-generates `ENUM_MARKET_SYMBOLS` for all discovered assets
- Consistent naming convention with `SYMBOL_` prefix
- Maintains serial number mapping for easy reference

### 🎨 **Multi-Format Export**
- **JSON Export**: Schema-compliant JSON with metadata and statistics
- **C Structure Export**: Ready-to-use C/C++ structures
- **Complete Schema Export**: Language-agnostic schema for cross-platform use

### 🏷️ **Intelligent Asset Classification**
- **FOREX**: Currency pairs (EURUSD, GBPJPY, etc.)
- **COMMODITIES**: Precious metals, energy, agriculture (XAU, OIL, CORN, etc.)
- **CRYPTO**: Digital currencies (BTC, ETH, ADA, etc.)
- **STOCKS**: Equity instruments with exchange codes
- **INDICES**: Market indices (SPX, NASDAQ, FTSE, etc.)

### 📈 **Advanced Analytics**
- Asset type distribution statistics
- Total asset count tracking
- Export timestamp and version control
- Schema compliance validation

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    CIndexer Class                           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Private Members                        │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  • CHashMap<string, SFinancialAsset*> m_assetsMap   │   │
│  │  • CArrayObj m_assetsArray                          │   │
│  │  • int m_currentSerial                              │   │
│  │  • string m_exportSchema                            │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Public Methods                         │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  • Constructor & Initialization                     │   │
│  │  • Asset Management (Add, Find, Search)             │   │
│  │  • Data Export (JSON, C Struct, Schema)            │   │
│  │  • Asset Classification & Analytics                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Data Structures

#### SFinancialAsset Structure
```cpp
struct SFinancialAsset {
    int serialNumber;           // Unique sequential identifier
    string assetName;           // Original symbol name
    string normalizedName;      // Normalized enum-friendly name
    ENUM_MARKET_SYMBOLS ESymbol; // Corresponding enum value
    ENUM_ASSET_TYPE assetType;  // Asset classification
    datetime timestamp;         // Creation/update timestamp
};
```

## 🚀 Quick Start

### Installation

1. **Copy Files to MetaTrader 5**
   ```bash
   # Copy to your MetaTrader 5 installation
   cp -r AssetsSymbolsIndex/ "C:\Users\YourUser\AppData\Roaming\MetaQuotes\Terminal\YourTerminal\MQL5\Libraries\"
   ```

2. **Include in Your Project**
   ```mql
   #include "AssetsSymbolsIndex/Indexer/CIndexer.mqh"

   // Create indexer instance
   CIndexer indexer();
   ```

3. **Initialize Asset Database**
   ```mql
   // Constructor automatically initializes all available assets
   CIndexer indexer();

   // Access asset statistics
   indexer.PrintStatistics();
   ```

### Basic Usage Example

```mql
//+------------------------------------------------------------------+
//| Example Expert Advisor using CIndexer                           |
//+------------------------------------------------------------------+
#include "AssetsSymbolsIndex/Indexer/CIndexer.mqh"

CIndexer indexer;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit() {
    // Indexer automatically discovers and catalogs all market assets
    Print("Asset indexer initialized with ", indexer.GetAssetCount(), " assets");

    // Export asset data in different formats
    string jsonData = indexer.ExportToJSON();
    string cStruct = indexer.ExportToCStruct();
    string schema = indexer.ExportCompleteSchema();

    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Find specific assets                                             |
//+------------------------------------------------------------------+
void ExampleUsage() {
    // Find asset by name
    SFinancialAsset* eurUsd = indexer.FindAssetByName("EURUSD");
    if(eurUsd) {
        Print("EURUSD Serial: ", eurUsd.serialNumber);
        Print("EURUSD Type: ", eurUsd.assetType);
    }

    // Find asset by enum
    SFinancialAsset* asset = indexer.FindAssetByEnum(SYMBOL_EURUSD);
}
```

## 📖 Usage Examples

### Example 1: Asset Discovery and Statistics

```mql
CIndexer indexer();

int OnInit() {
    // Get comprehensive statistics
    indexer.PrintStatistics();

    // Output:
    // === Index Statistics ===
    // Total Assets: 2847
    // Forex Pairs: 128
    // Commodities: 23
    // Cryptocurrencies: 156
    // Stocks: 2340
    // Indices: 200

    return(INIT_SUCCEEDED);
}
```

### Example 2: Dynamic Enum Generation

```mql
CIndexer indexer();

string enumDefinition = indexer.GenerateEnums();
// Generates:
// enum ENUM_MARKET_SYMBOLS {
//     SYMBOL_UNKNOWN = 0,
//     SYMBOL_EURUSD = 1,
//     SYMBOL_GBPUSD = 2,
//     SYMBOL_USDJPY = 3,
//     // ... all discovered symbols
// };
```

### Example 3: JSON Export with Full Schema

```mql
CIndexer indexer();

string jsonSchema = indexer.ExportToJSON();
// Exports comprehensive JSON including:
// - Asset metadata and statistics
// - Enum definitions
// - Asset type breakdowns
// - Schema compliance information
```

### Example 4: Cross-Language Schema Export

```mql
CIndexer indexer();

string completeSchema = indexer.ExportCompleteSchema();
// Generates complete schema for:
// - C/C++ structures
// - C# enums and classes
// - Python classes
// - JavaScript objects
// - Usage examples for each language
```

## 🔧 API Reference

### Constructor
```mql
CIndexer()  // Automatically initializes asset discovery
```

### Asset Management Methods

#### `bool InitializeAssets()`
- **Description**: Scans and catalogs all available market symbols
- **Returns**: `true` if successful, `false` otherwise

#### `bool AddAsset(string symbolName)`
- **Description**: Adds a specific asset to the index
- **Parameters**: `symbolName` - Symbol to add (e.g., "EURUSD")
- **Returns**: `true` if added, `false` if already exists

#### `SFinancialAsset* FindAssetByName(string name)`
- **Description**: Finds asset by symbol name
- **Returns**: Pointer to `SFinancialAsset` or `NULL` if not found

#### `SFinancialAsset* FindAssetByEnum(ENUM_MARKET_SYMBOLS enumSymbol)`
- **Description**: Finds asset by enum value
- **Returns**: Pointer to `SFinancialAsset` or `NULL` if not found

### Export Methods

#### `string ExportToJSON()`
- **Description**: Exports all assets in JSON format with full schema
- **Returns**: Complete JSON string with metadata and statistics

#### `string ExportToCStruct()`
- **Description**: Exports assets as C/C++ structure definition
- **Returns**: Ready-to-use C structure code

#### `string ExportCompleteSchema()`
- **Description**: Exports complete schema for multiple programming languages
- **Returns**: Multi-language schema with usage examples

### Analytics Methods

#### `void PrintStatistics()`
- **Description**: Prints comprehensive asset statistics to terminal
- **Output**: Asset counts by type, total assets, etc.

#### `string GetAssetTypeName(int assetType)`
- **Description**: Converts asset type enum to readable string
- **Returns**: String representation of asset type

## 📊 Workflow

### Asset Discovery Process

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│   Market    │───▶│   Symbol     │───▶│   Asset     │───▶│   Export     │
│   Scanner   │    │   Detection  │    │   Creation  │    │   Formats    │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│  SymbolsTotal│    │  Asset Type  │    │  Serial     │    │  JSON Schema │
│  Discovery  │    │  Detection   │    │  Assignment │    │  Generation  │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

### Asset Classification Logic

```
Symbol Name ───▶ Normalization ───▶ Type Detection ───▶ Classification
     │                 │                   │                   │
     ▼                 ▼                   ▼                   ▼
┌─────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│ EURUSD  │───▶│ SYMBOL_     │───▶│ Currency    │───▶│ FOREX        │
│ XAUUSD  │    │ EURUSD      │    │ Check       │    │              │
│ BTCUSD  │    │             │    │             │    │ COMMODITY    │
│ AAPL    │    │             │    │ CRYPTO      │    │              │
└─────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

## 🔍 Use Cases

### 🎯 **For Algorithmic Traders**
- **Multi-asset portfolio management**
- **Dynamic asset allocation strategies**
- **Cross-market correlation analysis**
- **Automated position sizing based on asset types**

### 🏢 **For Financial Institutions**
- **Risk management system integration**
- **Asset inventory and compliance reporting**
- **Real-time asset monitoring and alerts**
- **Regulatory reporting automation**

### 💻 **For MQL5 Developers**
- **Rapid prototyping with known asset universe**
- **Consistent asset referencing across projects**
- **Automated enum generation for type safety**
- **Schema-compliant data export for external systems**

### 📊 **For Market Analysts**
- **Asset universe analysis and reporting**
- **Market coverage assessment**
- **Asset type distribution studies**
- **Export data for external analysis tools**

## 🔄 Sequence Diagram

### Asset Initialization Sequence

```
┌─────────┐    ┌─────────────┐    ┌────────────┐    ┌─────────────┐
│         │    │             │    │            │    │             │
│ CIndexer│───▶│InitializeAssets│───▶│SymbolsTotal│───▶│  Asset     │
│         │    │             │    │            │    │  Creation  │
└─────────┘    └─────────────┘    └────────────┘    └─────────────┘
     │                 │                   │                   │
     ▼                 ▼                   ▼                   ▼
┌─────────┐    ┌─────────────┐    ┌────────────┐    ┌─────────────┐
│         │    │             │    │            │    │             │
│  Loop   │───▶│  Asset      │───▶│  Type      │───▶│   Asset    │
│  All    │    │  Detection  │    │  Detection │    │   Storage  │
│ Symbols │    │             │    │            │    │             │
└─────────┘    └─────────────┘    └────────────┘    └─────────────┘
```

### Asset Export Sequence

```
┌─────────┐    ┌─────────────┐    ┌────────────┐    ┌─────────────┐
│         │    │             │    │            │    │             │
│ Export  │───▶│  Asset      │───▶│  JSON      │───▶│  Schema    │
│ Request │    │  Iteration  │    │  Creation  │    │  Addition  │
└─────────┘    └─────────────┘    └────────────┘    └─────────────┘
     │                 │                   │                   │
     ▼                 ▼                   ▼                   ▼
┌─────────┐    ┌─────────────┐    ┌────────────┐    ┌─────────────┐
│         │    │             │    │            │    │             │
│ Format  │───▶│  Metadata   │───▶│ Statistics │───▶│  Final     │
│Selection│    │  Addition   │    │ Generation │    │  Export    │
└─────────┘    └─────────────┘    └────────────┘    └─────────────┘
```

## 📊 Class Diagram

### CIndexer Class Structure

```
┌─────────────────────────────────────────────────────────────┐
│                        CIndexer                             │
├─────────────────────────────────────────────────────────────┤
│  - m_assetsMap: CHashMap<string, SFinancialAsset*>         │
│  - m_assetsArray: CArrayObj                                 │
│  - m_currentSerial: int                                     │
│  - m_exportSchema: string                                   │
├─────────────────────────────────────────────────────────────┤
│  + CIndexer()                                               │
│  + InitializeAssets(): bool                                 │
│  + AddAsset(symbolName: string): bool                      │
│  + FindAssetByName(name: string): SFinancialAsset*          │
│  + FindAssetByEnum(enumSymbol: ENUM_MARKET_SYMBOLS): SFinancialAsset* │
│  + ExportToJSON(): string                                   │
│  + ExportToCStruct(): string                                │
│  + ExportCompleteSchema(): string                           │
│  + GenerateEnums(): string                                  │
│  + PrintStatistics(): void                                  │
│  + NormalizeName(name: string): string                      │
│  + DetectAssetType(symbolName: string): ENUM_ASSET_TYPE     │
│  + GetAssetTypeName(assetType: int): string                 │
└─────────────────────────────────────────────────────────────┘
```

### Supporting Types

```
┌─────────────────────────────────────────────────────────────┐
│                    SFinancialAsset                          │
├─────────────────────────────────────────────────────────────┤
│  + serialNumber: int                                        │
│  + assetName: string                                        │
│  + normalizedName: string                                   │
│  + ESymbol: ENUM_MARKET_SYMBOLS                             │
│  + assetType: ENUM_ASSET_TYPE                               │
│  + timestamp: datetime                                      │
└─────────────────────────────────────────────────────────────┘
```

## 🤝 Contributing

We welcome contributions to the MQL5 Financial Assets Indexer! Here's how you can help:

### Development Setup

1. **Clone or download** the project files
2. **Copy to MetaTrader 5** Libraries directory
3. **Test compilation** in MetaEditor
4. **Submit improvements** via pull requests

### Contribution Areas

- **Asset Type Detection**: Improve classification algorithms
- **Export Formats**: Add new export formats (XML, CSV, etc.)
- **Performance**: Optimize asset discovery and storage
- **Documentation**: Enhance examples and guides
- **Testing**: Add comprehensive test cases

### Code Standards

- Follow MQL5 best practices and naming conventions
- Include comprehensive comments for all public methods
- Test all changes in MetaEditor before submitting
- Update documentation for any API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Libraries

- **MQL5 Json Library**: Used for JSON export functionality
- **Logify**: Used for comprehensive logging capabilities

---

## 📞 Support & Contact

For questions, issues, or contributions, please:

- **Open an issue** on GitHub for bug reports
- **Submit a pull request** for improvements
- **Contact the maintainers** for collaboration opportunities

---

**Happy Trading!** 🚀📈