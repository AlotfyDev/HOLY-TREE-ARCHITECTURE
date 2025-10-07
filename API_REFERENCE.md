# MQL5 Financial Assets Indexer - API Reference

## 📋 Complete API Documentation

This document provides comprehensive reference for all public methods, properties, and usage patterns of the CIndexer class.

## 🏗️ Core Class

### CIndexer

Main class for financial asset indexing and management.

#### Constructor

```mql
CIndexer()
```

**Description**: Initializes a new asset indexer instance and automatically discovers all available market symbols.

**Automatic Actions**:
- Scans all available symbols in the MetaTrader 5 market
- Classifies assets by type (FOREX, Stocks, Commodities, Crypto, Indices)
- Creates normalized enum-friendly names
- Builds internal asset database for fast lookup
- Generates comprehensive statistics

**Usage**:
```mql
CIndexer indexer();  // Automatically initializes with all market assets
```

## 🔧 Public Methods

### Asset Management

#### `bool InitializeAssets()`

**Description**: Manually triggers asset discovery and initialization process.

**Returns**:
- `true` - Initialization successful
- `false` - Initialization failed

**Usage**:
```mql
CIndexer indexer();
bool success = indexer.InitializeAssets();
if(success) {
    Print("Asset initialization completed");
}
```

#### `bool AddAsset(string symbolName)`

**Description**: Adds a specific asset to the indexer database.

**Parameters**:
- `symbolName` (string) - Symbol name to add (e.g., "EURUSD")

**Returns**:
- `true` - Asset added successfully
- `false` - Asset already exists or invalid symbol

**Usage**:
```mql
CIndexer indexer();
bool added = indexer.AddAsset("EURUSD");
if(added) {
    Print("EURUSD added to indexer");
}
```

### Asset Search and Retrieval

#### `SFinancialAsset* FindAssetByName(string name)`

**Description**: Finds an asset by its symbol name.

**Parameters**:
- `name` (string) - Symbol name to search for

**Returns**:
- `SFinancialAsset*` - Pointer to asset structure if found
- `NULL` - Asset not found

**Usage**:
```mql
CIndexer indexer();
SFinancialAsset* eurUsd = indexer.FindAssetByName("EURUSD");
if(eurUsd != NULL) {
    Print("Found EURUSD - Serial: " + IntegerToString(eurUsd.serialNumber));
}
```

#### `SFinancialAsset* FindAssetByEnum(ENUM_MARKET_SYMBOLS enumSymbol)`

**Description**: Finds an asset by its generated enum value.

**Parameters**:
- `enumSymbol` (ENUM_MARKET_SYMBOLS) - Enum value to search for

**Returns**:
- `SFinancialAsset*` - Pointer to asset structure if found
- `NULL` - Asset not found

**Usage**:
```mql
CIndexer indexer();
SFinancialAsset* asset = indexer.FindAssetByEnum(SYMBOL_EURUSD);
if(asset != NULL) {
    Print("Found by enum: " + asset.assetName);
}
```

### Data Export

#### `string ExportToJSON()`

**Description**: Exports all assets in comprehensive JSON format with full schema compliance.

**Returns**: Complete JSON string containing:
- Asset database with all properties
- Asset type statistics and metadata
- Enum definitions for cross-reference
- Schema compliance information
- Export timestamp and version data

**Usage**:
```mql
CIndexer indexer();
string jsonData = indexer.ExportToJSON();

// Save to file
int fileHandle = FileOpen("assets.json", FILE_WRITE|FILE_TXT);
if(fileHandle != INVALID_HANDLE) {
    FileWriteString(fileHandle, jsonData);
    FileClose(fileHandle);
}
```

**JSON Structure**:
```json
{
  "financial_assets": [
    {
      "serial_number": 1,
      "asset_name": "EURUSD",
      "normalized_name": "SYMBOL_EURUSD",
      "enum_symbol": 1,
      "asset_type": 0,
      "asset_type_name": "FOREX",
      "timestamp": "2024-01-01 00:00:00",
      "properties": {}
    }
  ],
  "total_assets": 2847,
  "export_date": "2024-01-01 12:00:00",
  "enum_definitions": {
    "SYMBOL_EURUSD": 1,
    "SYMBOL_GBPUSD": 2
  },
  "metadata": {
    "version": "1.0.0",
    "exporter": "MQL5 Financial Assets Indexer",
    "asset_types": {
      "forex_pairs": 128,
      "stocks": 2340,
      "indices": 200,
      "commodities": 23,
      "cryptocurrencies": 156,
      "unknown": 0
    }
  }
}
```

#### `string ExportToCStruct()`

**Description**: Exports assets as ready-to-use C/C++ structure definition.

**Returns**: Complete C code with:
- Structure definition for FinancialAsset
- Array of all assets with their properties
- Total asset count constant

**Usage**:
```mql
CIndexer indexer();
string cCode = indexer.ExportToCStruct();

// Generated C code example:
// typedef struct {
//     int serial_number;
//     char asset_name[64];
//     char normalized_name[64];
//     int asset_type;
//     time_t timestamp;
// } FinancialAsset;
//
// FinancialAsset assets[] = {
//     {1, "EURUSD", "SYMBOL_EURUSD", 0, 1234567890},
//     {2, "XAUUSD", "SYMBOL_XAUUSD", 3, 1234567890}
// };
// const int TOTAL_ASSETS = 2847;
```

#### `string ExportCompleteSchema()`

**Description**: Exports complete schema for multiple programming languages.

**Returns**: Comprehensive schema including:
- C/C++ structures and enums
- C# classes and enums
- Python class definitions
- JavaScript object structures
- Usage examples for each language

**Usage**:
```mql
CIndexer indexer();
string schema = indexer.ExportCompleteSchema();

// Use in external applications
// Copy the generated code to your target language project
```

### Analytics and Information

#### `void PrintStatistics()`

**Description**: Displays comprehensive asset statistics to the terminal.

**Output Includes**:
- Total number of assets
- Count by asset type (FOREX, Stocks, Commodities, Crypto, Indices)
- Asset distribution percentages
- Discovery and update timestamps

**Usage**:
```mql
CIndexer indexer();
indexer.PrintStatistics();

// Output:
// === Index Statistics ===
// Total Assets: 2847
// Forex Pairs: 128
// Commodities: 23
// Cryptocurrencies: 156
// Stocks: 2340
// Indices: 200
```

#### `string GetAssetTypeName(int assetType)`

**Description**: Converts asset type enumeration to human-readable string.

**Parameters**:
- `assetType` (int) - Asset type enum value

**Returns**:
- `string` - Human-readable asset type name

**Usage**:
```mql
CIndexer indexer();
string typeName = indexer.GetAssetTypeName(ASSET_TYPE_FOREX);
// Returns: "FOREX"

string typeName = indexer.GetAssetTypeName(ASSET_TYPE_COMMODITY);
// Returns: "COMMODITY"
```

### Utility Methods

#### `string NormalizeName(string name)`

**Description**: Normalizes symbol names for enum-friendly format.

**Parameters**:
- `name` (string) - Original symbol name

**Returns**:
- `string` - Normalized name with SYMBOL_ prefix

**Usage**:
```mql
CIndexer indexer();
string normalized = indexer.NormalizeName("EURUSD");
// Returns: "SYMBOL_EURUSD"
```

#### `ENUM_ASSET_TYPE DetectAssetType(string symbolName)`

**Description**: Detects asset type based on symbol name patterns.

**Parameters**:
- `symbolName` (string) - Symbol name to classify

**Returns**:
- `ENUM_ASSET_TYPE` - Detected asset type

**Usage**:
```mql
CIndexer indexer();
ENUM_ASSET_TYPE type = indexer.DetectAssetType("XAUUSD");
// Returns: ASSET_TYPE_COMMODITY
```

## 📊 Data Structures

### SFinancialAsset Structure

Complete structure containing all asset information:

```cpp
struct SFinancialAsset {
    int serialNumber;           // Unique sequential identifier (1, 2, 3, ...)
    string assetName;           // Original symbol name ("EURUSD")
    string normalizedName;      // Enum-friendly name ("SYMBOL_EURUSD")
    ENUM_MARKET_SYMBOLS ESymbol; // Corresponding enum value
    ENUM_ASSET_TYPE assetType;  // Asset classification
    datetime timestamp;         // Discovery timestamp
};
```

### Enumeration Types

#### ENUM_MARKET_SYMBOLS
Dynamically generated enumeration for all discovered assets:

```cpp
enum ENUM_MARKET_SYMBOLS {
    SYMBOL_UNKNOWN = 0,      // Default/unknown asset
    SYMBOL_EURUSD = 1,       // EURUSD asset
    SYMBOL_GBPUSD = 2,       // GBPUSD asset
    SYMBOL_USDJPY = 3,       // USDJPY asset
    // ... dynamically generated for all assets
};
```

#### ENUM_ASSET_TYPE
Asset classification enumeration:

```cpp
enum ENUM_ASSET_TYPE {
    ASSET_TYPE_FOREX = 0,     // Currency pairs
    ASSET_TYPE_STOCK = 1,     // Equity instruments
    ASSET_TYPE_INDEX = 2,     // Market indices
    ASSET_TYPE_COMMODITY = 3, // Commodities and futures
    ASSET_TYPE_CRYPTO = 4,    // Cryptocurrencies
    ASSET_TYPE_UNKNOWN = 5    // Unclassified assets
};
```

## 🔧 Advanced Usage Patterns

### Batch Asset Processing

```mql
// Process multiple assets efficiently
CIndexer indexer();

void ProcessAssetBatch() {
    // Get all FOREX assets
    for(int i = 0; i < indexer.GetAssetCount(); i++) {
        SFinancialAsset* asset = indexer.GetAssetByIndex(i);
        if(asset != NULL && asset.assetType == ASSET_TYPE_FOREX) {
            // Process FOREX asset
            ProcessForexAsset(asset);
        }
    }
}
```

### Custom Asset Filtering

```mql
// Filter assets by custom criteria
SFinancialAsset* GetHighVolumeAssets() {
    SFinancialAsset* filteredAssets[];

    for(int i = 0; i < indexer.GetAssetCount(); i++) {
        SFinancialAsset* asset = indexer.GetAssetByIndex(i);
        if(asset != NULL && IsHighVolume(asset)) {
            // Add to filtered list
        }
    }

    return filteredAssets;
}
```

### Integration with Trading Systems

```mql
// Integrate with existing trading systems
class CTradingSystem {
private:
    CIndexer m_indexer;

public:
    void Initialize() {
        // Use indexer for asset management
        SFinancialAsset* asset = m_indexer.FindAssetByName("EURUSD");
        if(asset != NULL) {
            // Configure trading parameters based on asset type
            ConfigureTradingParameters(asset);
        }
    }
};
```

## 📋 Method Signatures

### Complete Method Reference

| Method | Signature | Description |
|--------|-----------|-------------|
| Constructor | `CIndexer()` | Initialize with automatic asset discovery |
| Initialize | `bool InitializeAssets()` | Manual initialization trigger |
| Add Asset | `bool AddAsset(string symbolName)` | Add specific asset |
| Find by Name | `SFinancialAsset* FindAssetByName(string name)` | Search by symbol name |
| Find by Enum | `SFinancialAsset* FindAssetByEnum(ENUM_MARKET_SYMBOLS enumSymbol)` | Search by enum value |
| JSON Export | `string ExportToJSON()` | Full JSON schema export |
| C Struct Export | `string ExportToCStruct()` | C/C++ structure export |
| Complete Schema | `string ExportCompleteSchema()` | Multi-language schema |
| Statistics | `void PrintStatistics()` | Display asset statistics |
| Type Name | `string GetAssetTypeName(int assetType)` | Get type string |
| Normalize | `string NormalizeName(string name)` | Normalize symbol name |
| Detect Type | `ENUM_ASSET_TYPE DetectAssetType(string symbolName)` | Classify asset type |

## 🔍 Error Handling

### Return Value Patterns

#### Asset Search Methods
- **Success**: Returns valid `SFinancialAsset*` pointer
- **Not Found**: Returns `NULL` pointer
- **Error**: Returns `NULL` pointer

#### Boolean Methods
- **Success**: Returns `true`
- **Failure**: Returns `false`

#### String Methods
- **Success**: Returns valid string with content
- **Error**: Returns empty string `""`

### Exception Safety

- All methods are exception-safe
- No memory leaks in error conditions
- Graceful degradation on invalid input
- Comprehensive error logging with Logify integration

## 🚀 Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Asset Search (by name) | O(1) | HashMap lookup |
| Asset Search (by enum) | O(n) | Array iteration |
| Asset Addition | O(1) | HashMap + Array insert |
| Statistics Generation | O(n) | Single array pass |
| Export Operations | O(n) | Process all assets |

### Memory Usage

- **Base Memory**: ~1KB for CIndexer instance
- **Per Asset**: ~100-200 bytes depending on string lengths
- **HashMap Overhead**: ~50% of asset data size
- **Array Storage**: Direct asset storage
- **Total Estimate**: ~500KB for 2000 assets

## 📋 Best Practices

### ✅ **Recommended Usage**

1. **Single Instance**: Create one CIndexer per application
2. **Early Initialization**: Initialize in OnInit() for best performance
3. **Null Checking**: Always check return values for asset searches
4. **Error Handling**: Implement proper error handling for all operations
5. **Resource Management**: No manual cleanup required - handled internally

### ❌ **Avoid These Patterns**

1. **Multiple Instances**: Don't create multiple indexers unnecessarily
2. **Late Initialization**: Don't initialize during trading operations
3. **Ignore Return Values**: Always check if asset searches succeed
4. **Manual Memory Management**: Don't attempt to manage indexer memory
5. **Synchronous Export**: Don't export large datasets during active trading

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue: Asset Not Found
```mql
// Problem: Asset search returns NULL
SFinancialAsset* asset = indexer.FindAssetByName("EURUSD");
if(asset == NULL) {
    // Check if symbol exists in Market Watch
    Print("Available symbols: " + IntegerToString(SymbolsTotal(true)));
    // Verify symbol name spelling
    Print("Checking symbol: EURUSD");
}
```

#### Issue: Incorrect Asset Type
```mql
// Problem: Asset classified incorrectly
SFinancialAsset* asset = indexer.FindAssetByName("XAUUSD");
if(asset != NULL) {
    Print("Asset type: " + indexer.GetAssetTypeName(asset.assetType));
    // Should return "COMMODITY" for gold
    // If incorrect, may need manual classification
}
```

#### Issue: Export Data Issues
```mql
// Problem: Export functions return empty data
string jsonData = indexer.ExportToJSON();
if(StringLen(jsonData) == 0) {
    // Check if assets were loaded
    indexer.PrintStatistics();
    // Verify initialization completed
}
```

## 📞 Support

For additional API information:

- **[README.md](README.md)** - Project overview and setup
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Detailed usage instructions
- **[WORKFLOW.md](WORKFLOW.md)** - Internal workflow documentation
- **[IMPORTANCE.md](IMPORTANCE.md)** - Project significance and use cases

---

## 🎯 **API Summary**

| Category | Methods | Purpose |
|----------|---------|---------|
| **Initialization** | `CIndexer()`, `InitializeAssets()` | Setup and asset discovery |
| **Search** | `FindAssetByName()`, `FindAssetByEnum()` | Asset lookup and retrieval |
| **Export** | `ExportToJSON()`, `ExportToCStruct()`, `ExportCompleteSchema()` | Data export in multiple formats |
| **Analytics** | `PrintStatistics()`, `GetAssetTypeName()` | Statistics and information |
| **Utility** | `NormalizeName()`, `DetectAssetType()` | Asset processing and classification |

**The CIndexer API is designed for simplicity, performance, and comprehensive asset management capabilities.**