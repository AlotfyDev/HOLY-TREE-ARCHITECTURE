# MQL5 Financial Assets Indexer - Workflow Documentation

## 📋 Table of Contents

- [Asset Discovery Workflow](#asset-discovery-workflow)
- [Classification Workflow](#classification-workflow)
- [Export Workflow](#export-workflow)
- [Integration Workflow](#integration-workflow)
- [Sequence Diagrams](#sequence-diagrams)
- [Class Diagrams](#class-diagrams)
- [State Diagrams](#state-diagrams)

## 🔄 Asset Discovery Workflow

### Phase 1: Initialization

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│             │    │              │    │             │
│  CIndexer   │───▶│  Constructor │───▶│  Initialize │
│  Creation   │    │              │    │  Assets()   │
│             │    │              │    │             │
└─────────────┘    └──────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│             │    │              │    │             │
│ Set Default │    │  Scan Market │    │  Get Symbol │
│ Parameters  │    │  Symbols     │    │  Count      │
└─────────────┘    └──────────────┘    └─────────────┘
```

### Phase 2: Symbol Processing

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │              │    │             │    │             │
│   Loop      │───▶│   Get        │───▶│  Asset      │───▶│   Asset     │
│   All       │    │   Symbol     │    │  Creation   │    │  Addition   │
│  Symbols    │    │   Name       │    │             │    │             │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │              │    │             │    │             │
│ Symbol Name │───▶│ Normalization│───▶│ Type        │───▶│ Serial      │
│ Validation  │    │              │    │ Detection   │    │ Assignment  │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
```

### Phase 3: Storage and Organization

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │              │    │             │    │             │
│   Asset     │───▶│   HashMap    │───▶│  Array      │───▶│ Statistics  │
│   Object    │    │   Storage    │    │  Storage    │    │ Generation  │
│             │    │              │    │             │    │             │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    �─────────────┐
│             │    │              │    │             │    │             │
│  Enum       │    │  Type        │    │  Timestamp  │    │  Validation │
│ Generation  │    │  Assignment  │    │  Creation   │    │  Complete   │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
```

## 🏷️ Classification Workflow

### Asset Type Detection Logic

```
Symbol Input ───▶ Normalization ───▶ Pattern Analysis ───▶ Type Assignment
     │                   │                   │                   │
     ▼                   ▼                   ▼                   ▼
┌──────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│ EURUSD   │───▶│ SYMBOL_      │───▶│ Currency    │───▶│ ASSET_TYPE_  │
│ XAUUSD   │    │ EURUSD       │    │ Check       │    │ FOREX        │
│ BTCUSD   │    │              │    │             │    │              │
│ AAPL     │    │              │    │ Commodity   │    │ COMMODITY    │
└──────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

### FOREX Detection Sub-Workflow

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │              │    │             │    │             │
│  Symbol     │───▶│  Currency    │───▶│  Pair       │───▶│  FOREX      │
│  Analysis   │    │  Code        │    │  Pattern    │    │  Assignment │
│             │    │  Detection   │    │  Validation │    │             │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │              │    │             │    │             │
│ USD Check   │───▶│ EUR Check    │───▶│ JPY Check   │───▶│ Multi-      │
│             │    │              │    │             │    │ Currency    │
│             │    │              │    │             │    │ Validation  │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
```

## 📤 Export Workflow

### JSON Export Process

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │              │    │             │    │             │
│ Export      │───▶│  Asset       │───▶│  JSON       │───▶│  Schema     │
│ Request     │    │  Iteration   │    │  Object     │    │  Addition   │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │              │    │             │    │             │
│ Root Doc    │───▶│  Assets      │───▶│  Metadata   │───▶│ Statistics  │
│ Creation    │    │  Array       │    │  Addition   │    │ Generation  │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
```

### Multi-Format Export Process

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │              │    │             │    │             │
│ Format      │───▶│  JSON        │───▶│  C          │───▶│  Complete   │
│ Selection   │    │  Export      │    │  Structure  │    │  Schema     │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │              │    │             │    │             │
│ JSON with   │    │  C/C++       │    │  Multi-     │    │  Final      │
│ Full Schema │    │ Structures   │    │  Language   │    │  Output     │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
```

## 🔗 Integration Workflow

### External System Integration

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │              │    │             │    │             │
│  CIndexer   │───▶│  Export      │───▶│  Format     │───▶│  External   │
│             │    │  Request     │    │  Selection  │    │  System     │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│             │    │              │    │             │    │             │
│ Asset Data  │───▶│  JSON        │───▶│  C Struct   │───▶│  Database   │
│ Collection  │    │  Schema      │    │             │    │  Import     │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
```

## 📊 Sequence Diagrams

### Asset Initialization Sequence

```
Participant "CIndexer" as CI
Participant "Market" as MKT
Participant "AssetsMap" as AM
Participant "AssetsArray" as AA

CI->MKT: SymbolsTotal(true)
activate MKT
MKT-->CI: total_symbols_count
deactivate MKT

loop for each symbol
    CI->MKT: SymbolName(i, true)
    activate MKT
    MKT-->CI: symbol_name
    deactivate MKT

    CI->CI: NormalizeName(symbol_name)
    activate CI
    CI->CI: DetectAssetType(symbol_name)
    CI-->CI: asset_type
    CI-->CI: normalized_name
    deactivate CI

    CI->AM: Add(symbol_name, asset)
    activate AM
    AM-->CI: success
    deactivate AM

    CI->AA: Add(asset)
    activate AA
    AA-->CI: success
    deactivate AA
end

CI->CI: PrintStatistics()
```

### Asset Search Sequence

```
Participant "Client" as C
Participant "CIndexer" as CI
Participant "AssetsMap" as AM
Participant "AssetsArray" as AA

C->CI: FindAssetByName("EURUSD")
activate CI

CI->AM: TryGetValue("EURUSD")
activate AM
AM-->CI: asset_found
deactivate AM

alt asset found in map
    CI-->C: asset_pointer
else asset not in map
    CI->AA: Search in array
    activate AA
    AA-->CI: asset_found
    deactivate AA

    CI-->C: asset_pointer
end

deactivate CI
```

### Export Process Sequence

```
Participant "Client" as C
Participant "CIndexer" as CI
Participant "JSON" as JSON
Participant "Schema" as SCH

C->CI: ExportToJSON()
activate CI

CI->CI: Create root document
CI->JSON: JsonNewObject()
activate JSON
JSON-->CI: root_document
deactivate JSON

CI->CI: Create assets array
CI->JSON: JsonNewArray()
activate JSON
JSON-->CI: assets_array
deactivate JSON

loop for each asset
    CI->CI: Create asset document
    CI->CI: Add asset properties
    CI->CI: Add to assets array
end

CI->CI: Add metadata
CI->CI: Add statistics
CI->SCH: Generate schema
activate SCH
SCH-->CI: schema_data
deactivate SCH

CI->CI: Compile final JSON
CI-->C: complete_json_string

deactivate CI
```

## 🏗️ Class Diagrams

### CIndexer Class Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                          CIndexer                               │
├─────────────────────────────────────────────────────────────────┤
│  - m_assetsMap: CHashMap<string, SFinancialAsset*>             │
│  - m_assetsArray: CArrayObj                                     │
│  - m_currentSerial: int                                         │
│  - m_exportSchema: string                                       │
├─────────────────────────────────────────────────────────────────┤
│  + CIndexer()                                                   │
│  + InitializeAssets(): bool                                     │
│  + AddAsset(symbolName: string): bool                          │
│  + FindAssetByName(name: string): SFinancialAsset*              │
│  + FindAssetByEnum(enumSymbol: ENUM_MARKET_SYMBOLS): SFinancialAsset* │
│  + ExportToJSON(): string                                       │
│  + ExportToCStruct(): string                                    │
│  + ExportCompleteSchema(): string                               │
│  + GenerateEnums(): string                                      │
│  + PrintStatistics(): void                                      │
│  + NormalizeName(name: string): string                          │
│  + DetectAssetType(symbolName: string): ENUM_ASSET_TYPE         │
│  + GetAssetTypeName(assetType: int): string                     │
└─────────────────────────────────────────────────────────────────┘
```

### Supporting Types Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                      SFinancialAsset                           │
├─────────────────────────────────────────────────────────────────┤
│  + serialNumber: int                                            │
│  + assetName: string                                            │
│  + normalizedName: string                                       │
│  + ESymbol: ENUM_MARKET_SYMBOLS                                 │
│  + assetType: ENUM_ASSET_TYPE                                   │
│  + timestamp: datetime                                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    ENUM_MARKET_SYMBOLS                          │
├─────────────────────────────────────────────────────────────────┤
│  + SYMBOL_UNKNOWN = 0                                           │
│  + SYMBOL_EURUSD = 1                                            │
│  + SYMBOL_GBPUSD = 2                                            │
│  + SYMBOL_USDJPY = 3                                            │
│  + ... (dynamically generated for all assets)                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      ENUM_ASSET_TYPE                            │
├─────────────────────────────────────────────────────────────────┤
│  + ASSET_TYPE_FOREX = 0                                         │
│  + ASSET_TYPE_STOCK = 1                                         │
│  + ASSET_TYPE_INDEX = 2                                         │
│  + ASSET_TYPE_COMMODITY = 3                                     │
│  + ASSET_TYPE_CRYPTO = 4                                        │
│  + ASSET_TYPE_UNKNOWN = 5                                       │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 State Diagrams

### CIndexer Lifecycle

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│             │    │              │    │             │    │              │
│   Created   │───▶│ Initialized  │───▶│  Assets     │───▶│   Ready for │
│             │    │              │    │  Loaded     │    │   Use        │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│             │    │              │    │             │    │              │
│ Export      │    │ Search       │    │ Statistics  │    │ Maintenance  │
│ Operations  │    │ Operations   │    │ Display     │    │ Mode         │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

### Asset Processing States

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│             │    │              │    │             │    │              │
│   Raw       │───▶│ Normalized   │───▶│ Classified  │───▶│   Stored     │
│  Symbol     │    │              │    │             │    │              │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│             │    │              │    │             │    │              │
│ Validation  │    │ Enum         │    │ HashMap     │    │ Array        │
│ Check       │    │ Generation   │    │ Storage     │    │ Storage      │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

## 📋 Workflow Integration

### With Trading Strategy

```
Strategy Development ───▶ Asset Universe ───▶ Classification ───▶ Strategy Implementation
       │                           │                   │                   │
       ▼                           ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│             │    │              │    │             │    │              │
│ Strategy    │───▶│  CIndexer    │───▶│  Asset      │───▶│  Trading     │
│ Design      │    │              │    │  Data       │    │  Logic       │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

### With Risk Management

```
Risk Assessment ───▶ Asset Analysis ───▶ Risk Calculation ───▶ Risk Reporting
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│             │    │              │    │             │    │              │
│ Risk        │───▶│  CIndexer    │───▶│  Portfolio  │───▶│  Risk        │
│ Framework   │    │              │    │  Analysis   │    │  Dashboard   │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

### With Market Analysis

```
Market Data ───▶ Asset Discovery ───▶ Analysis Engine ───▶ Reports & Insights
       │               │                   │                   │
       ▼               ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│             │    │              │    │             │    │              │
│ Data        │───▶│  CIndexer    │───▶│  Market     │───▶│  Analysis    │
│ Sources     │    │              │    │  Analytics  │    │  Platform    │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

## 🔧 Process Flow Details

### Asset Discovery Process Flow

1. **Initialization Phase**
   - Constructor called
   - Default parameters set
   - Asset discovery initiated

2. **Market Scanning Phase**
   - Query total symbol count
   - Loop through each symbol
   - Extract symbol names

3. **Asset Processing Phase**
   - Normalize symbol names
   - Detect asset types
   - Assign serial numbers
   - Create asset objects

4. **Storage Phase**
   - Add to HashMap for fast lookup
   - Add to Array for ordered access
   - Update statistics

5. **Completion Phase**
   - Generate final statistics
   - Display completion summary
   - Ready for use

### Export Process Flow

1. **Export Request Phase**
   - Determine export format
   - Initialize export structures
   - Prepare data collection

2. **Data Collection Phase**
   - Iterate through all assets
   - Extract required information
   - Format according to target schema

3. **Schema Generation Phase**
   - Create root document structure
   - Add metadata and statistics
   - Generate enum definitions

4. **Format-Specific Processing**
   - JSON: Create nested object structure
   - C Struct: Generate C code
   - Complete Schema: Multi-language templates

5. **Finalization Phase**
   - Validate export data
   - Add timestamps and version info
   - Return formatted result

## 📈 Performance Workflow

### Memory Management

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│             │    │              │    │             │    │              │
│  Memory     │───▶│  Asset       │───▶│  HashMap    │───▶│  Array       │
│ Allocation  │    │  Creation    │    │  Storage    │    │  Storage     │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│             │    │              │    │             │    │              │
│ Object      │    │ Pointer      │    │ Reference   │    │  Cleanup     │
│ Lifecycle   │    │ Management   │    │ Counting    │    │  Management  │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

### Optimization Points

1. **HashMap Storage**: O(1) lookup performance for asset searches
2. **Array Storage**: Ordered access for enumeration and iteration
3. **Lazy Loading**: Assets created only when needed
4. **Memory Reuse**: Efficient memory usage for large asset databases

## 🔍 Error Handling Workflow

### Exception Management

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│             │    │              │    │             │    │              │
│  Error      │───▶│  Detection   │───▶│  Logging    │───▶│  Recovery    │
│  Detection  │    │              │    │             │    │              │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│             │    │              │    │             │    │              │
│ Validation  │    │  User        │    │  Graceful   │    │  Continue    │
│ Checks      │    │  Notification│    │  Degradation│    │  Operation   │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
```

## 🚀 Deployment Workflow

### Development to Production

```
Development ───▶ Testing ───▶ Validation ───▶ Deployment ───▶ Monitoring
     │               │              │              │              │
     ▼               ▼              ▼              ▼              ▼
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌─────────┐    ┌────────────┐
│         │    │          │    │         │    │         │    │            │
│ Local   │───▶│  Meta-   │───▶│ Asset   │───▶│ Live    │───▶│ Production │
│ Testing │    │  Editor  │    │  Data   │    │  Trading│    │  Monitoring│
└─────────┘    └──────────┘    └─────────┘    └─────────┘    └────────────┘
```

---

## 📞 **Need More Details?**

For detailed implementation information, see:
- **[README.md](README.md)** - Comprehensive project overview
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Detailed usage instructions
- **[Examples.mqh](Examples.mqh)** - Practical code examples
- **[IMPORTANCE.md](IMPORTANCE.md)** - Project significance and use cases

---

**This workflow documentation provides a complete understanding of how the MQL5 Financial Assets Indexer operates internally and integrates with external systems.**