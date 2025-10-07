#ifndef __CINDEXER_MQH__
#define __CINDEXER_MQH__

// Basic MQL5 includes for standard functions
#include <Object.mqh>
#include <Arrays/ArrayObj.mqh>
#include <Generic/HashMap.mqh>
#include <Strings/String.mqh>
#include <Json/JsonLib.mqh>
#include <Logify/Logify.mqh>

// Global Logify instance for logging
CLogify Logify;

#include "../SupportingTypes/Structs/SFinancialAsset.mqh"
#include "../SupportingTypes/Enums/ENUM_MARKET_SYMBOLS.mqh"
#include "../SupportingTypes/Enums/ENUM_ASSET_TYPE.mqh"
#include "../Utilities/StringJsonConverter.mqh"




//+------------------------------------------------------------------+
//| Asset Manager Class                               |
//+------------------------------------------------------------------+
class CIndexer
{
private:
    CHashMap<string, SFinancialAsset*> m_assetsMap;          // Assets map
    CArrayObj m_assetsArray;              // Assets array
    int m_currentSerial;                  // Serial counter
    string m_exportSchema;                // Export schema

public:
    //+------------------------------------------------------------------+
    //| Constructor                                       |
    //+------------------------------------------------------------------+
    CIndexer()
    {
        m_currentSerial = 0;
        m_exportSchema = "JSON";
        InitializeAssets();
    }

    //+------------------------------------------------------------------+
    //| Initialize Assets                                 |
    //+------------------------------------------------------------------+
    bool InitializeAssets()
    {
        Logify.Debug("InitializeAssets called");

        // Get all available symbols in the market
        int totalSymbols = SymbolsTotal(true);
        Logify.Debug("Found " + IntegerToString(totalSymbols) + " total symbols in market");

        int processedCount = 0;
        for(int i = 0; i < totalSymbols; i++)
        {
            string symbolName = SymbolName(i, true);
            Logify.Debug("Processing symbol " + IntegerToString(i) + ": " + symbolName);

            if(AddAsset(symbolName)) {
                processedCount++;
            }
        }

        Logify.Debug("Successfully processed " + IntegerToString(processedCount) + " out of " + IntegerToString(totalSymbols) + " symbols");
        Logify.Info("Successfully initialized " + IntegerToString(m_assetsArray.Total()) + " assets");
        return true;
    }

    //+------------------------------------------------------------------+
    //| Add New Asset                                     |
    //+------------------------------------------------------------------+
    bool AddAsset(const string symbolName)
    {
        Logify.Debug("AddAsset called with symbol: " + symbolName);

        if(m_assetsMap.ContainsKey(symbolName)) {
            Logify.Debug("Asset " + symbolName + " already exists, skipping");
            return false;
        }

        SFinancialAsset* asset = new SFinancialAsset();
        asset.serialNumber = ++m_currentSerial;
        asset.assetName = symbolName;
        asset.normalizedName = NormalizeName(symbolName);
        asset.assetType = DetectAssetType(symbolName);
        asset.timestamp = TimeCurrent();

        // FIX: Properly set the enum symbol to match the serial number
        // This creates the link between enum values and asset data
        asset.ESymbol = (ENUM_MARKET_SYMBOLS)asset.serialNumber;

        // Log the fix: enum vs string field consistency
        Logify.Debug("Asset created - serial: " + IntegerToString(asset.serialNumber) + ", name: " + asset.assetName + ", normalized: " + asset.normalizedName + ", enum: " + IntegerToString(asset.ESymbol) + ", type: " + IntegerToString(asset.assetType));
        Logify.Info("FIXED: ESymbol field now properly set to match serial number");

        m_assetsMap.Add(symbolName, asset);
        m_assetsArray.Add(asset);

        Logify.Debug("Asset " + symbolName + " added successfully");
        return true;
    }

    //+------------------------------------------------------------------+
    //| Normalize Asset Name for Enum                     |
    //+------------------------------------------------------------------+
    string NormalizeName(const string name)
    {
        Logify.Debug("NormalizeName called with: " + name);

        string result = name;

        // Remove unwanted characters
        StringReplace(result, ".", "");
        StringReplace(result, "-", "_");
        StringReplace(result, " ", "_");
        StringReplace(result, "/", "_");

        // Convert to uppercase
        StringToUpper(result);

        // Add prefix if necessary
        if(StringLen(result) > 0 && (result[0] >= '0' && result[0] <= '9'))
            result = "SYMBOL_" + result;

        string finalResult = "SYMBOL_" + result;
        Logify.Debug("NormalizeName result: " + name + " -> " + finalResult);

        return finalResult;
    }

    //+------------------------------------------------------------------+
    //| Detect Asset Type                                 |
    //+------------------------------------------------------------------+
    ENUM_ASSET_TYPE DetectAssetType(const string symbolName)
    {
        Logify.Debug("DetectAssetType called with: " + symbolName);

        string upperName = symbolName;
        StringToUpper(upperName);

        Logify.Debug("Checking asset type for: " + symbolName + " (upper: " + upperName + ")");

        // Enhanced FOREX detection - check for currency pairs
        if(StringFind(upperName, "USD") >= 0 ||
           StringFind(upperName, "EUR") >= 0 ||
           StringFind(upperName, "JPY") >= 0 ||
           StringFind(upperName, "GBP") >= 0 ||
           StringFind(upperName, "CHF") >= 0 ||
           StringFind(upperName, "CAD") >= 0 ||
           StringFind(upperName, "AUD") >= 0 ||
           StringFind(upperName, "NZD") >= 0 ||
           StringFind(upperName, "SEK") >= 0 ||
           StringFind(upperName, "NOK") >= 0 ||
           StringFind(upperName, "DKK") >= 0 ||
           StringFind(upperName, "PLN") >= 0 ||
           StringFind(upperName, "ZAR") >= 0 ||
           StringFind(upperName, "TRY") >= 0 ||
           StringFind(upperName, "MXN") >= 0 ||
           StringFind(upperName, "SGD") >= 0 ||
           StringFind(upperName, "HKD") >= 0 ||
           StringFind(upperName, "CNH") >= 0 ||
           StringFind(upperName, "INR") >= 0 ||
           StringFind(upperName, "RUB") >= 0 ||
           StringFind(upperName, "BRL") >= 0) {
            Logify.Debug("Detected FOREX asset: " + symbolName);
             return ASSET_TYPE_FOREX;
         }

         // Enhanced COMMODITY detection
         else if(StringFind(upperName, "XAU") >= 0 ||  // Gold
                 StringFind(upperName, "XAG") >= 0 ||  // Silver
                 StringFind(upperName, "XPT") >= 0 ||  // Platinum
                 StringFind(upperName, "XPD") >= 0 ||  // Palladium
                 StringFind(upperName, "OIL") >= 0 ||  // Oil
                 StringFind(upperName, "BRENT") >= 0 || // Brent Oil
                 StringFind(upperName, "WTI") >= 0 ||  // WTI Oil
                 StringFind(upperName, "NG") >= 0 ||   // Natural Gas
                 StringFind(upperName, "GAS") >= 0 ||  // Gas
                 StringFind(upperName, "CORN") >= 0 || // Corn
                 StringFind(upperName, "WHEAT") >= 0 || // Wheat
                 StringFind(upperName, "SOY") >= 0 ||  // Soybean
                 StringFind(upperName, "SUGAR") >= 0 || // Sugar
                 StringFind(upperName, "COFFEE") >= 0 || // Coffee
                 StringFind(upperName, "COTTON") >= 0 || // Cotton
                 StringFind(upperName, "COPPER") >= 0 || // Copper
                 StringFind(upperName, "ALUMINIUM") >= 0 || // Aluminium
                 StringFind(upperName, "ZINC") >= 0 ||  // Zinc
                 StringFind(upperName, "NICKEL") >= 0 || // Nickel
                 StringFind(upperName, "LEAD") >= 0) {  // Lead
             Logify.Debug("Detected COMMODITY asset: " + symbolName);
             return ASSET_TYPE_COMMODITY;
         }

        // Enhanced CRYPTO detection
        else if(StringFind(upperName, "BTC") >= 0 ||  // Bitcoin
                StringFind(upperName, "ETH") >= 0 ||  // Ethereum
                StringFind(upperName, "LTC") >= 0 ||  // Litecoin
                StringFind(upperName, "XRP") >= 0 ||  // Ripple
                StringFind(upperName, "ADA") >= 0 ||  // Cardano
                StringFind(upperName, "DOT") >= 0 ||  // Polkadot
                StringFind(upperName, "LINK") >= 0 || // Chainlink
                StringFind(upperName, "XLM") >= 0 ||  // Stellar
                StringFind(upperName, "BCH") >= 0 ||  // Bitcoin Cash
                StringFind(upperName, "BNB") >= 0 ||  // Binance Coin
                StringFind(upperName, "XMR") >= 0 ||  // Monero
                StringFind(upperName, "DASH") >= 0 || // Dash
                StringFind(upperName, "NEO") >= 0 ||  // NEO
                StringFind(upperName, "ETC") >= 0 ||  // Ethereum Classic
                StringFind(upperName, "ZEC") >= 0 ||  // Zcash
                StringFind(upperName, "XTZ") >= 0 ||  // Tezos
                StringFind(upperName, "ATOM") >= 0 || // Cosmos
                StringFind(upperName, "ALGO") >= 0 || // Algorand
                StringFind(upperName, "VET") >= 0 ||  // VeChain
                StringFind(upperName, "THETA") >= 0 || // Theta
                StringFind(upperName, "AVAX") >= 0 || // Avalanche
                StringFind(upperName, "MATIC") >= 0 || // Polygon
                StringFind(upperName, "SOL") >= 0 ||  // Solana
                StringFind(upperName, "UNI") >= 0 ||  // Uniswap
                StringFind(upperName, "AAVE") >= 0 || // Aave
                StringFind(upperName, "COMP") >= 0 || // Compound
                StringFind(upperName, "MKR") >= 0 ||  // Maker
                StringFind(upperName, "SNX") >= 0 ||  // Synthetix
                StringFind(upperName, "SUSHI") >= 0 || // SushiSwap
                StringFind(upperName, "YFI") >= 0 ||  // Yearn Finance
                StringFind(upperName, "CRV") >= 0) {  // Curve
            Logify.Debug("Detected CRYPTO asset: " + symbolName);
            return ASSET_TYPE_CRYPTO;
        }

        // STOCK detection - typically 3-4 letter codes, sometimes with exchange suffix
        else if(StringLen(symbolName) >= 3 && StringLen(symbolName) <= 6) {
            // Check if it looks like a stock symbol (not containing common forex/crypto patterns)
            if(StringFind(upperName, "USD") == -1 &&
               StringFind(upperName, "EUR") == -1 &&
               StringFind(upperName, "JPY") == -1 &&
               StringFind(upperName, "BTC") == -1 &&
               StringFind(upperName, "ETH") == -1 &&
               StringFind(upperName, "XAU") == -1) {
                Logify.Debug("Detected STOCK asset: " + symbolName);
                return ASSET_TYPE_STOCK;
            }
        }

        // INDEX detection - typically ends with index suffix or contains "INDEX"
        else if(StringFind(upperName, "INDEX") >= 0 ||
                StringFind(upperName, "NDX") >= 0 ||   // NASDAQ 100
                StringFind(upperName, "SPX") >= 0 ||   // S&P 500
                StringFind(upperName, "DJI") >= 0 ||   // Dow Jones
                StringFind(upperName, "FTSE") >= 0 ||  // FTSE 100
                StringFind(upperName, "DAX") >= 0 ||   // DAX
                StringFind(upperName, "CAC") >= 0 ||   // CAC 40
                StringFind(upperName, "NKY") >= 0 ||   // Nikkei
                StringFind(upperName, "HSI") >= 0 ||   // Hang Seng
                StringFind(upperName, "ASX") >= 0 ||   // ASX 200
                StringFind(upperName, "VIX") >= 0) {   // Volatility Index
            Logify.Debug("Detected INDEX asset: " + symbolName);
            return ASSET_TYPE_INDEX;
        }

        Logify.Debug("Asset type UNKNOWN for: " + symbolName);
        return ASSET_TYPE_UNKNOWN;
    }

    //+------------------------------------------------------------------+
    //| Get Asset Type Name                              |
    //+------------------------------------------------------------------+
    string GetAssetTypeName(int assetType)
    {
        switch(assetType)
        {
            case ASSET_TYPE_FOREX: return "FOREX";
            case ASSET_TYPE_STOCK: return "STOCK";
            case ASSET_TYPE_INDEX: return "INDEX";
            case ASSET_TYPE_COMMODITY: return "COMMODITY";
            case ASSET_TYPE_CRYPTO: return "CRYPTO";
            default: return "UNKNOWN";
        }
    }

    //+------------------------------------------------------------------+
    //| Export to JSON                                    |
    //+------------------------------------------------------------------+
    string ExportToJSON()
    {
        Logify.Debug("ExportToJSON called for " + IntegerToString(m_assetsArray.Total()) + " assets");

        CStringJsonConverter converter;

        // Create root document as object
        MQL5_Json::JsonDocument rootDoc = MQL5_Json::JsonNewObject();

        // Create assets array document as object containing array of assets
        MQL5_Json::JsonDocument assetsArrayDoc = MQL5_Json::JsonNewArray();

        for(int i = 0; i < m_assetsArray.Total(); i++)
        {
            CObject* obj = m_assetsArray.At(i);
            SFinancialAsset* asset = obj ? (SFinancialAsset*)obj : NULL;
            if(!asset) continue;

            // Create individual asset object (schema-compliant with asset_type_name and properties)
            MQL5_Json::JsonDocument assetDoc;
            string assetKeys[8] = {"serial_number", "asset_name", "normalized_name", "enum_symbol", "asset_type", "asset_type_name", "timestamp", "properties"};
            string assetValuesStr[7] = {
                IntegerToString(asset.serialNumber), asset.assetName, asset.normalizedName,
                IntegerToString((int)asset.ESymbol), IntegerToString(asset.assetType), GetAssetTypeName(asset.assetType), TimeToString(asset.timestamp)
            };

            // Create base asset object
            if(converter.CreateJsonObject(assetDoc, assetKeys, assetValuesStr, 7))
            {
                // Add empty properties object (schema compliance)
                MQL5_Json::JsonDocument propsDoc = MQL5_Json::JsonNewObject();
                assetDoc.GetRoot().Set("properties", propsDoc.GetRoot());

                assetsArrayDoc.GetRoot().Add(assetDoc.GetRoot());
                Logify.Debug("Exported schema-compliant asset: " + asset.assetName + " -> enum: " + IntegerToString(asset.ESymbol));
            }
        }

        // Set the assets array in root document
        rootDoc.GetRoot().Set("financial_assets", assetsArrayDoc.GetRoot());

        // Add other fields to root
        MQL5_Json::JsonDocument totalAssetsDoc = MQL5_Json::JsonNewObject();
        totalAssetsDoc.GetRoot().Set("value", (long)m_assetsArray.Total());
        rootDoc.GetRoot().Set("total_assets", totalAssetsDoc.GetRoot());
        rootDoc.GetRoot().Set("export_date", TimeToString(TimeCurrent()));

        // Create enum definitions object
        MQL5_Json::JsonDocument enumsDoc;
        const int enumCount = m_assetsArray.Total();
        string enumKeys[];
        string enumValues[];
        ArrayResize(enumKeys, enumCount);
        ArrayResize(enumValues, enumCount);

        for(int i = 0; i < m_assetsArray.Total(); i++)
        {
            CObject* obj = m_assetsArray.At(i);
            SFinancialAsset* asset = obj ? (SFinancialAsset*)obj : NULL;
            if(asset) {
                enumKeys[i] = asset.normalizedName;
                enumValues[i] = IntegerToString((int)asset.ESymbol);
            }
        }

        if(converter.CreateJsonObject(enumsDoc, enumKeys, enumValues, enumCount))
        {
            rootDoc.GetRoot().Set("enum_definitions", enumsDoc.GetRoot());
        }

        // Add JSON Schema reference (makes the JSON self-describing)
        MQL5_Json::JsonDocument schemaDoc = MQL5_Json::JsonNewObject();
        schemaDoc.GetRoot().Set("value", "https://github.com/supernova/mql5-indexer/financial-assets-schema.json");
        rootDoc.GetRoot().Set("$schema", schemaDoc.GetRoot());

        // Add schema-compliant metadata section
        MQL5_Json::JsonDocument metadataDoc = MQL5_Json::JsonNewObject();
        MQL5_Json::JsonDocument versionDoc = MQL5_Json::JsonNewObject();
        versionDoc.GetRoot().Set("value", "1.0.0");
        metadataDoc.GetRoot().Set("version", versionDoc.GetRoot());
        MQL5_Json::JsonDocument exporterDoc = MQL5_Json::JsonNewObject();
        exporterDoc.GetRoot().Set("value", "MQL5 Financial Assets Indexer");
        metadataDoc.GetRoot().Set("exporter", exporterDoc.GetRoot());

        // Add asset type statistics
        MQL5_Json::JsonDocument statsDoc = MQL5_Json::JsonNewObject();

        int typeCount[6] = {0};
        for(int i = 0; i < m_assetsArray.Total(); i++)
        {
            CObject* obj = m_assetsArray.At(i);
            SFinancialAsset* asset = obj ? (SFinancialAsset*)obj : NULL;
            if(asset) {
                typeCount[asset.assetType]++;
            }
        }

        MQL5_Json::JsonDocument forexDoc = MQL5_Json::JsonNewObject();
        forexDoc.GetRoot().Set("value", (long)(typeCount[ASSET_TYPE_FOREX]));
        statsDoc.GetRoot().Set("forex_pairs", forexDoc.GetRoot());
        MQL5_Json::JsonDocument stocksDoc = MQL5_Json::JsonNewObject();
        stocksDoc.GetRoot().Set("value", (long)(typeCount[ASSET_TYPE_STOCK]));
        statsDoc.GetRoot().Set("stocks", stocksDoc.GetRoot());
        MQL5_Json::JsonDocument indicesDoc = MQL5_Json::JsonNewObject();
        indicesDoc.GetRoot().Set("value", (long)(typeCount[ASSET_TYPE_INDEX]));
        statsDoc.GetRoot().Set("indices", indicesDoc.GetRoot());
        MQL5_Json::JsonDocument commoditiesDoc = MQL5_Json::JsonNewObject();
        commoditiesDoc.GetRoot().Set("value", (long)(typeCount[ASSET_TYPE_COMMODITY]));
        statsDoc.GetRoot().Set("commodities", commoditiesDoc.GetRoot());
        MQL5_Json::JsonDocument cryptoDoc = MQL5_Json::JsonNewObject();
        cryptoDoc.GetRoot().Set("value", (long)(typeCount[ASSET_TYPE_CRYPTO]));
        statsDoc.GetRoot().Set("cryptocurrencies", cryptoDoc.GetRoot());
        MQL5_Json::JsonDocument unknownDoc = MQL5_Json::JsonNewObject();
        unknownDoc.GetRoot().Set("value", (long)(typeCount[ASSET_TYPE_UNKNOWN]));
        statsDoc.GetRoot().Set("unknown", unknownDoc.GetRoot());

        metadataDoc.GetRoot().Set("asset_types", statsDoc.GetRoot());
        rootDoc.GetRoot().Set("metadata", metadataDoc.GetRoot());

        string result = "";
        converter.DocumentToJsonString(rootDoc, result, true); // Pretty print

        Logify.Debug("JSON schema export completed with " + IntegerToString(m_assetsArray.Total()) + " assets, enum definitions, and metadata");
        return result;
    }

    //+------------------------------------------------------------------+
    //| Export to C Structure                             |
    //+------------------------------------------------------------------+
    string ExportToCStruct()
    {
        string result = "// Financial Assets Structure\n";
        result += "// Generated on: " + TimeToString(TimeCurrent()) + "\n\n";
        
        result += "typedef struct {\n";
        result += "    int serial_number;\n";
        result += "    char asset_name[64];\n";
        result += "    char normalized_name[64];\n";
        result += "    int asset_type;\n";
        result += "    time_t timestamp;\n";
        result += "} FinancialAsset;\n\n";
        
        result += "FinancialAsset assets[] = {\n";
        
        for(int i = 0; i < m_assetsArray.Total(); i++)
        {
            CObject* obj = m_assetsArray.At(i);
            SFinancialAsset* asset = obj ? (SFinancialAsset*)obj : NULL;
            if(!asset) continue;

            result += StringFormat("    {%d, \"%s\", \"%s\", %d, %d}",
                                  asset.serialNumber,
                                  asset.assetName,
                                  asset.normalizedName,
                                  asset.assetType,
                                  asset.timestamp);

            if(i < m_assetsArray.Total() - 1)
                result += ",\n";
            else
                result += "\n";
        }
        
        result += "};\n";
        result += StringFormat("const int TOTAL_ASSETS = %d;", m_assetsArray.Total());
        
        return result;
    }

    //+------------------------------------------------------------------+
    //| Generate Dynamic Enums                            |
    //+------------------------------------------------------------------+
    string GenerateEnums()
    {
        Logify.Debug("GenerateEnums called, processing " + IntegerToString(m_assetsArray.Total()) + " assets");

        string result = "// ENUM_MARKET_SYMBOLS - Auto-generated enum for market symbols\n";
        result += "// Generated on: " + TimeToString(TimeCurrent()) + "\n\n";
        result += "enum ENUM_MARKET_SYMBOLS {\n";
        result += "    SYMBOL_UNKNOWN = 0,\n";

        Logify.Debug("Generated enum values:");
        for(int i = 0; i < m_assetsArray.Total(); i++)
        {
            CObject* obj = m_assetsArray.At(i);
            SFinancialAsset* asset = obj ? (SFinancialAsset*)obj : NULL;
            if(asset) {
                string enumLine = "    " + asset.normalizedName + " = " + IntegerToString(asset.serialNumber);
                result += enumLine;

                Logify.Debug("  " + enumLine);

                if(i < m_assetsArray.Total() - 1)
                    result += ",\n";
                else
                    result += "\n";
            }
        }

        result += "};\n\n";
        result += "// Usage example:\n";
        result += "// ENUM_MARKET_SYMBOLS symbol = SYMBOL_EURUSD; // Use normalized name as enum value\n";

        Logify.Debug("Generated enum with " + IntegerToString(m_assetsArray.Total()) + " symbols");
        return result;
    }

    //+------------------------------------------------------------------+
    //| Export Complete Schema for Other Languages        |
    //+------------------------------------------------------------------+
    string ExportCompleteSchema()
    {
        Logify.Debug("ExportCompleteSchema called for " + IntegerToString(m_assetsArray.Total()) + " assets");

        string result = "/*\n";
        result += " * Financial Assets Index Schema\n";
        result += " * Generated on: " + TimeToString(TimeCurrent()) + "\n";
        result += " * Total Assets: " + IntegerToString(m_assetsArray.Total()) + "\n";
        result += " *\n";
        result += " * This schema can be used by other languages (C#, Python, JavaScript, etc.)\n";
        result += " */\n\n";

        // Add enum definition
        result += GenerateEnums() + "\n";

        // Add type definitions
        result += "/* Asset Type Definitions */\n";
        result += "enum ENUM_ASSET_TYPE {\n";
        result += "    ASSET_TYPE_FOREX = 0,\n";
        result += "    ASSET_TYPE_STOCK = 1,\n";
        result += "    ASSET_TYPE_INDEX = 2,\n";
        result += "    ASSET_TYPE_COMMODITY = 3,\n";
        result += "    ASSET_TYPE_CRYPTO = 4,\n";
        result += "    ASSET_TYPE_UNKNOWN = 5\n";
        result += "};\n\n";

        // Add C structure definition
        result += "/* C/C++ Structure Definition */\n";
        result += "typedef struct {\n";
        result += "    int serial_number;\n";
        result += "    char asset_name[64];\n";
        result += "    char normalized_name[64];\n";
        result += "    int enum_symbol;\n";
        result += "    int asset_type;\n";
        result += "    char timestamp[32];\n";
        result += "} FinancialAsset;\n\n";

        // Add asset data array
        result += "/* Asset Data Array */\n";
        result += "FinancialAsset assets[] = {\n";

        for(int i = 0; i < m_assetsArray.Total(); i++)
        {
            CObject* obj = m_assetsArray.At(i);
            SFinancialAsset* asset = obj ? (SFinancialAsset*)obj : NULL;
            if(!asset) continue;

            result += StringFormat("    {%d, \"%s\", \"%s\", %d, %d, \"%s\"}",
                                  asset.serialNumber,
                                  asset.assetName,
                                  asset.normalizedName,
                                  asset.ESymbol,
                                  asset.assetType,
                                  TimeToString(asset.timestamp));

            if(i < m_assetsArray.Total() - 1)
                result += ",\n";
            else
                result += "\n";
        }

        result += "};\n";
        result += StringFormat("const int TOTAL_ASSETS = %d;\n\n", m_assetsArray.Total());

        // Add usage examples for different languages
        result += "/*\n";
        result += " * Usage Examples:\n";
        result += " *\n";
        result += " * C/C++:\n";
        result += " *   ENUM_MARKET_SYMBOLS symbol = SYMBOL_EURUSD;\n";
        result += " *\n";
        result += " * C#:\n";
        result += " *   public enum MarketSymbols { SYMBOL_EURUSD = 1, SYMBOL_GOLD = 2 }\n";
        result += " *\n";
        result += " * Python:\n";
        result += " *   class MarketSymbols:\n";
        result += " *       SYMBOL_EURUSD = 1\n";
        result += " *       SYMBOL_GOLD = 2\n";
        result += " *\n";
        result += " * JavaScript:\n";
        result += " *   const MarketSymbols = {\n";
        result += " *     SYMBOL_EURUSD: 1,\n";
        result += " *     SYMBOL_GOLD: 2\n";
        result += " *   }\n";
        result += " */\n";

        Logify.Debug("Complete schema export finished");
        return result;
    }

    //+------------------------------------------------------------------+
    //| Get Nested Map for Assets                         |
    //+------------------------------------------------------------------+
    // NOTE: This method was commented out due to migration from CMapStringToPtr to CHashMap
    // CHashMap<string, CHashMap<string, void*>*> would be complex to implement
    // Consider reimplementing if this functionality is required
    // CMapStringToPtr* GetNestedMap()
    // {
    //     CMapStringToPtr* nestedMap = new CMapStringToPtr();
    //
    //     for(int i = 0; i < m_assetsArray.Total(); i++)
    //     {
    //         SFinancialAsset* asset = m_assetsArray.At(i);
    //
    //         // Create sub-map for each asset
    //         CMapStringToPtr* assetMap = new CMapStringToPtr();
    //         assetMap.Add("serial", (void*)asset.serialNumber);
    //         assetMap.Add("name", (void*)&asset.assetName);
    //         assetMap.Add("normalized", (void*)&asset.normalizedName);
    //         assetMap.Add("type", (void*)asset.assetType);
    //         assetMap.Add("timestamp", (void*)asset.timestamp);
    //
    //         nestedMap.Add(asset.assetName, assetMap);
    //     }
    //
    //     return nestedMap;
    // }

    //+------------------------------------------------------------------+
    //| Search in Index                                   |
    //+------------------------------------------------------------------+
    SFinancialAsset* FindAssetByName(const string name)
    {
        SFinancialAsset* asset = NULL;
        if(m_assetsMap.TryGetValue(name, asset))
            return asset;
        return NULL;
    }

    SFinancialAsset* FindAssetBySerial(const int serial)
    {
        for(int i = 0; i < m_assetsArray.Total(); i++)
        {
            CObject* obj = m_assetsArray.At(i);
            SFinancialAsset* asset = obj ? (SFinancialAsset*)obj : NULL;
            if(asset && asset.serialNumber == serial)
                return asset;
        }
        return NULL;
    }

    //+------------------------------------------------------------------+
    //| Search by Enum                                    |
    //+------------------------------------------------------------------+
    SFinancialAsset* FindAssetByEnum(ENUM_MARKET_SYMBOLS enumSymbol)
    {
        int serial = (int)enumSymbol;
        Logify.Debug("FindAssetByEnum called with: " + IntegerToString(enumSymbol));

        for(int i = 0; i < m_assetsArray.Total(); i++)
        {
            CObject* obj = m_assetsArray.At(i);
            SFinancialAsset* asset = obj ? (SFinancialAsset*)obj : NULL;
            if(asset && asset.ESymbol == enumSymbol)
            {
                Logify.Debug("Found asset by enum " + IntegerToString(enumSymbol) + ": " + asset.assetName);
                return asset;
            }
        }

        Logify.Debug("No asset found for enum: " + IntegerToString(enumSymbol));
        return NULL;
    }

    //+------------------------------------------------------------------+
    //| Index Statistics                                  |
    //+------------------------------------------------------------------+
    void PrintStatistics()
    {
        int typeCount[6] = {0};

        for(int i = 0; i < m_assetsArray.Total(); i++)
        {
            CObject* obj = m_assetsArray.At(i);
            SFinancialAsset* asset = obj ? (SFinancialAsset*)obj : NULL;
            if(asset) {
                typeCount[asset.assetType]++;
            }
        }

        Logify.Info("=== Index Statistics ===");
        Logify.Info("Total Assets: " + IntegerToString(m_assetsArray.Total()));
        Logify.Info("Forex Pairs: " + IntegerToString(typeCount[ASSET_TYPE_FOREX]));
        Logify.Info("Commodities: " + IntegerToString(typeCount[ASSET_TYPE_COMMODITY]));
        Logify.Info("Cryptocurrencies: " + IntegerToString(typeCount[ASSET_TYPE_CRYPTO]));
        Logify.Info("Stocks: " + IntegerToString(typeCount[ASSET_TYPE_STOCK]));
        Logify.Info("Indices: " + IntegerToString(typeCount[ASSET_TYPE_INDEX]));
        Logify.Info("Unknown: " + IntegerToString(typeCount[ASSET_TYPE_UNKNOWN]));
    }
};





















#endif // __CINDEXER_MQH__
