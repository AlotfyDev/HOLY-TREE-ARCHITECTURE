# MQL5 Financial Assets Indexer - Usage Guide

## 📋 Table of Contents

- [Basic Usage](#basic-usage)
- [Asset Discovery](#asset-discovery)
- [Search and Find](#search-and-find)
- [Export Functions](#export-functions)
- [Analytics and Statistics](#analytics-and-statistics)
- [Integration Examples](#integration-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## 🚀 Basic Usage

### Simple Initialization

```mql
// Include the indexer in your MQL5 file
#include "AssetsSymbolsIndex/Indexer/CIndexer.mqh"

// Create indexer instance - automatically discovers all market assets
CIndexer indexer();

// The constructor automatically:
// - Scans all available symbols in the market
// - Classifies assets by type (FOREX, Stocks, Commodities, Crypto, Indices)
// - Creates normalized enum names
// - Builds internal asset database
```

### Check Initialization

```mql
int OnInit() {
    // Display comprehensive statistics
    indexer.PrintStatistics();

    // Output example:
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

## 🔍 Asset Discovery

### Automatic Asset Detection

The indexer automatically discovers and classifies all available financial instruments:

#### FOREX Pairs
- **Pattern**: Currency pairs like EURUSD, GBPJPY, AUDCAD
- **Detection**: Contains currency codes (USD, EUR, JPY, GBP, CHF, CAD, AUD, NZD, etc.)
- **Examples**: EURUSD, USDJPY, GBPCHF, AUDCAD

#### Commodities
- **Pattern**: Precious metals, energy, agriculture
- **Detection**: Contains commodity codes (XAU, XAG, XPT, OIL, CORN, WHEAT, etc.)
- **Examples**: XAUUSD (Gold), XAGUSD (Silver), BRENT (Oil), CORN (Corn)

#### Cryptocurrencies
- **Pattern**: Digital currencies and tokens
- **Detection**: Contains crypto codes (BTC, ETH, LTC, XRP, ADA, etc.)
- **Examples**: BTCUSD (Bitcoin), ETHUSD (Ethereum), ADAUSD (Cardano)

#### Stocks
- **Pattern**: Equity instruments, typically 1-6 characters
- **Detection**: Short codes not matching other patterns
- **Examples**: AAPL (Apple), GOOGL (Google), MSFT (Microsoft)

#### Indices
- **Pattern**: Market indices and benchmarks
- **Detection**: Contains index codes (SPX, NASDAQ, FTSE, DAX, INDEX, etc.)
- **Examples**: SPX500 (S&P 500), NAS100 (NASDAQ), FTSE100, DAX30

## 🔎 Search and Find

### Find Assets by Name

```mql
// Find specific assets by symbol name
SFinancialAsset* eurUsd = indexer.FindAssetByName("EURUSD");
if(eurUsd != NULL) {
    Print("EURUSD Details:");
    Print("  Serial Number: " + IntegerToString(eurUsd.serialNumber));
    Print("  Asset Type: " + indexer.GetAssetTypeName(eurUsd.assetType));
    Print("  Normalized Name: " + eurUsd.normalizedName);
    Print("  Enum Symbol: " + eurUsd.normalizedName);
}
```

### Find Assets by Enum

```mql
// Find assets using the generated enum values
SFinancialAsset* asset = indexer.FindAssetByEnum(SYMBOL_EURUSD);
if(asset != NULL) {
    Print("Found: " + asset.assetName);
    Print("Type: " + indexer.GetAssetTypeName(asset.assetType));
}
```

### Asset Information Structure

Each discovered asset contains:

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

## 📤 Export Functions

### JSON Export

```mql
// Export all assets in comprehensive JSON format
string jsonData = indexer.ExportToJSON();

// The JSON includes:
// - Complete asset database
// - Asset type statistics
// - Enum definitions
// - Schema compliance information
// - Metadata and version info

// Save to file
int fileHandle = FileOpen("assets.json", FILE_WRITE|FILE_TXT);
if(fileHandle != INVALID_HANDLE) {
    FileWriteString(fileHandle, jsonData);
    FileClose(fileHandle);
}
```

### C Structure Export

```mql
// Export assets as C/C++ structure
string cStruct = indexer.ExportToCStruct();

// Generates ready-to-use C code:
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
//     {2, "XAUUSD", "SYMBOL_XAUUSD", 3, 1234567890},
//     // ... all assets
// };
```

### Complete Schema Export

```mql
// Export complete schema for multiple programming languages
string schema = indexer.ExportCompleteSchema();

// Generates comprehensive schema including:
// - C/C++ structures and enums
// - C# classes and enums
// - Python class definitions
// - JavaScript object structures
// - Usage examples for each language
```

## 📊 Analytics and Statistics

### Comprehensive Statistics

```mql
// Get detailed asset statistics
indexer.PrintStatistics();

// Output includes:
// - Total number of assets
// - Count by asset type (FOREX, Stocks, etc.)
// - Asset distribution percentages
// - Discovery timestamp
```

### Asset Type Information

```mql
// Get asset type name
string typeName = indexer.GetAssetTypeName(ASSET_TYPE_FOREX);
// Returns: "FOREX"

string typeName = indexer.GetAssetTypeName(ASSET_TYPE_COMMODITY);
// Returns: "COMMODITY"
```

### Custom Analytics

```mql
// Build custom analytics based on asset data
int forexCount = 0;
int cryptoCount = 0;

// Access all assets for custom analysis
for(int i = 0; i < indexer.GetAssetCount(); i++) {
    SFinancialAsset* asset = indexer.GetAssetByIndex(i);
    if(asset != NULL) {
        switch(asset.assetType) {
            case ASSET_TYPE_FOREX:
                forexCount++;
                break;
            case ASSET_TYPE_CRYPTO:
                cryptoCount++;
                break;
        }
    }
}
```

## 💡 Integration Examples

### Example 1: Multi-Asset Portfolio Manager

```mql
class CPortfolioManager {
private:
    CIndexer m_indexer;
    SFinancialAsset* m_portfolio[];

public:
    void Initialize() {
        // Add major assets to portfolio
        AddAssetToPortfolio("EURUSD");
        AddAssetToPortfolio("XAUUSD");
        AddAssetToPortfolio("BTCUSD");
        AddAssetToPortfolio("SPX500");
    }

    void AddAssetToPortfolio(string symbolName) {
        SFinancialAsset* asset = m_indexer.FindAssetByName(symbolName);
        if(asset != NULL) {
            // Add to portfolio array
            Print("Added " + symbolName + " to portfolio");
        }
    }

    void AnalyzeDiversification() {
        // Analyze asset type distribution
        // Calculate correlation metrics
        // Generate risk assessments
    }
};
```

### Example 2: Dynamic Strategy Universe

```mql
class CStrategyUniverse {
private:
    CIndexer m_indexer;

public:
    void DefineUniverse() {
        // Create universe of liquid FOREX pairs
        string liquidForex[] = {"EURUSD", "GBPUSD", "USDJPY", "AUDUSD"};

        for(int i = 0; i < ArraySize(liquidForex); i++) {
            SFinancialAsset* asset = m_indexer.FindAssetByName(liquidForex[i]);
            if(asset != NULL) {
                // Add to strategy universe
                Print("Strategy asset: " + asset.assetName);
            }
        }
    }
};
```

### Example 3: Risk Management Integration

```mql
class CRiskManager {
private:
    CIndexer m_indexer;

public:
    void AssessPortfolioRisk() {
        // Get asset type distribution
        m_indexer.PrintStatistics();

        // Analyze concentration risks
        // Calculate diversification ratios
        // Generate risk recommendations
    }
};
```

## 🛠️ Advanced Usage

### Custom Asset Classification

```mql
// The indexer provides intelligent classification, but you can also:
// - Add custom asset types
// - Override automatic classification
// - Create specialized asset categories
// - Implement custom detection rules
```

### Real-Time Asset Monitoring

```mql
// Monitor for new assets in real-time
void OnTimer() {
    // Re-scan for new symbols
    // Compare with existing database
    // Alert on new asset discovery
    // Update asset statistics
}
```

### Integration with Market Data

```mql
// Combine with price data for enhanced analytics
SFinancialAsset* asset = indexer.FindAssetByName("EURUSD");
if(asset != NULL) {
    double currentPrice = SymbolInfoDouble("EURUSD", SYMBOL_BID);
    // Combine asset metadata with price data
    // Generate trading signals
    // Update position sizing
}
```

## 📋 Best Practices

### ✅ **Recommended Practices**

1. **Initialize Once**: Create the indexer once in `OnInit()` and reuse
2. **Cache Results**: Store frequently accessed assets in local variables
3. **Error Handling**: Always check for NULL returns when searching for assets
4. **Memory Management**: The indexer handles its own memory - no manual cleanup needed
5. **Performance**: Asset discovery happens automatically - no need to call manually

### ❌ **Avoid These Patterns**

1. **Don't recreate the indexer** in every function call
2. **Don't manually manage asset memory** - the indexer handles this
3. **Don't assume all symbols exist** - always check return values
4. **Don't ignore asset types** - use the classification for better organization

### 🚀 **Performance Tips**

1. **Batch Operations**: Find multiple assets in a single operation when possible
2. **Use Enums**: Prefer enum-based searches over string-based when possible
3. **Cache Statistics**: Store frequently accessed statistics in local variables
4. **Selective Export**: Only export data in the format you actually need

## 🔧 Troubleshooting

### Common Issues

#### Issue: Asset Not Found
```mql
SFinancialAsset* asset = indexer.FindAssetByName("EURUSD");
if(asset == NULL) {
    Print("Asset not found - check if symbol exists in Market Watch");
    Print("Available symbols: ", SymbolsTotal(true));
}
```

#### Issue: Incorrect Asset Type
```mql
SFinancialAsset* asset = indexer.FindAssetByName("XAUUSD");
if(asset != NULL) {
    Print("Asset type: " + indexer.GetAssetTypeName(asset.assetType));
    // Should return "COMMODITY" for gold
}
```

#### Issue: Export Data Too Large
```mql
// For large export files, consider:
string jsonData = indexer.ExportToJSON();
// Process in chunks or save to file directly
```

### Debug Information

```mql
// Enable detailed logging for troubleshooting
Logify.Debug("Asset indexer initialization started");
Logify.Debug("Total symbols found: " + IntegerToString(SymbolsTotal(true)));
Logify.Debug("Asset discovery completed");

// Check specific asset details
SFinancialAsset* asset = indexer.FindAssetByName("EURUSD");
if(asset != NULL) {
    Logify.Debug("Asset details:");
    Logify.Debug("  Name: " + asset.assetName);
    Logify.Debug("  Normalized: " + asset.normalizedName);
    Logify.Debug("  Type: " + IntegerToString(asset.assetType));
    Logify.Debug("  Serial: " + IntegerToString(asset.serialNumber));
}
```

## 📞 Support

For additional help:

1. **Check the README.md** for comprehensive documentation
2. **Review the Examples.mqh** for practical usage patterns
3. **Examine the API documentation** for detailed method signatures
4. **Test in MetaEditor** for the best compilation experience

---

## 🎯 **Quick Reference**

| Method | Purpose | Example |
|--------|---------|---------|
| `FindAssetByName()` | Find by symbol | `FindAssetByName("EURUSD")` |
| `FindAssetByEnum()` | Find by enum | `FindAssetByEnum(SYMBOL_EURUSD)` |
| `ExportToJSON()` | JSON export | `string json = ExportToJSON()` |
| `ExportToCStruct()` | C structure export | `string c = ExportToCStruct()` |
| `PrintStatistics()` | Show statistics | `PrintStatistics()` |
| `GetAssetTypeName()` | Get type string | `GetAssetTypeName(FOREX)` |

**Happy Trading!** 🚀📈