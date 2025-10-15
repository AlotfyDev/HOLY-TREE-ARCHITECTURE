# Coding Standards and Implementation Guide

## 📋 Overview

This document establishes the **coding standards and implementation guidelines** for the Cross-Language Logging System. These standards ensure consistency, maintainability, and quality across all components and language integrations.

## 🏗️ **C++ Implementation Standards**

### **Layer 1 (Toolbox) Coding Standards**

#### **Namespace Organization:**
```cpp
// ✅ CORRECT: Organized toolbox namespaces
namespace FinancialLogging {
    namespace Toolbox {
        namespace Validation {
            bool IsValidLogLevel(const std::string& level);
            bool IsValidTimestamp(const std::string& timestamp);
        }

        namespace Calculation {
            size_t CalculateOptimalBufferSize(size_t base_size, size_t max_size);
            size_t CalculateSafeAccessSize(size_t buffer_size, size_t requested_size);
        }

        namespace Conversion {
            std::string StructToJson(const void* struct_ptr, const std::string& schema);
            bool JsonToStruct(const std::string& json, void* struct_ptr, const std::string& schema);
        }
    }
}

// ❌ INCORRECT: Poor namespace organization
namespace Utils {
    bool Validate(const std::string& input);  // Too generic
    size_t Calculate(size_t input);          // Too generic
}
```

#### **Function Signature Standards:**
```cpp
// ✅ CORRECT: Clear, descriptive function signatures
namespace BufferToolbox {
    // Pure calculation functions
    size_t CalculateOptimalBufferSize(
        size_t base_data_size,
        size_t max_buffer_size,
        double growth_factor = 1.5
    );

    // Validation functions
    bool IsBufferSizeValid(
        size_t requested_size,
        size_t min_size,
        size_t max_size
    );

    // Conversion functions
    ConversionResult ConvertStructToJson(
        const void* struct_ptr,
        const std::string& struct_type,
        const std::string& json_schema,
        std::string* output_json
    );
}

// ❌ INCORRECT: Poor function signatures
namespace BadToolbox {
    size_t calc(size_t a, size_t b);                    // Unclear names
    bool check(size_t x);                               // Unclear purpose
    void convert(const void* p, std::string& out);      // No error handling
}
```

### **Layer 2 (PODs) Coding Standards**

#### **Struct Definition Standards:**
```cpp
// ✅ CORRECT: Well-defined POD structures
#pragma pack(push, 1)
struct LogEntryStruct {
    // Mandatory universal header
    UniversalDataHeader header;

    // Struct-specific fields (alphabetical order)
    char correlation_id[64];
    char level[16];
    char logger_name[64];
    char message[1024];
    char session_id[64];
    char source_file[256];
    int32_t source_line;
    char thread_id[16];
    uint64_t nanoseconds;
};
#pragma pack(pop)

// Static assertions for size validation
static_assert(sizeof(LogEntryStruct) == 1376, "LogEntryStruct size must be exactly 1376 bytes");
static_assert(alignof(LogEntryStruct) == 1, "LogEntryStruct must be packed");

// ❌ INCORRECT: Poor POD design
struct BadStruct {
    int id;                    // Random field order
    std::string name;          // Non-POD type
    void Process() {}          // Behavior in POD
};
```

#### **Configuration POD Standards:**
```cpp
// ✅ CORRECT: Configuration POD with validation
struct LoggerConfig {
    // Constructor with parameter validation
    explicit LoggerConfig(
        const std::string& name = "default",
        LogLevel level = LogLevel::Info,
        const std::string& pattern = "%Y-%m-%d %H:%M:%S [%l] %v",
        size_t buffer_size = 4096,
        size_t max_file_size = 1024 * 1024,
        int max_files = 3
    );

    // Validation method
    bool IsValid() const;

    // Data members (const where possible)
    const std::string name_;
    const LogLevel level_;
    const std::string pattern_;
    const size_t buffer_size_;
    const size_t max_file_size_;
    const int max_files_;
};

// ❌ INCORRECT: Poor configuration design
struct BadConfig {
    std::string name = "default";  // Mutable, hardcoded default
    int level = 2;                 // Magic number
    // No validation
};
```

### **Layer 3 (Stateful) Coding Standards**

#### **Class Design Standards:**
```cpp
// ✅ CORRECT: Well-designed stateful class
class Logger : public ILogger {
public:
    // Constructor with dependency injection
    explicit Logger(
        std::shared_ptr<spdlog::logger> spdlog_impl,
        const LoggerConfig& config,
        std::unique_ptr<ICache> cache = nullptr,
        std::unique_ptr<IComplianceManager> compliance = nullptr
    );

    // RAII compliance
    ~Logger() override;  // Proper cleanup

    // No copy/move if managing resources
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    // Clear, descriptive method names
    bool ConfigureLogger(const LoggerConfig& new_config);
    bool AttachCache(std::unique_ptr<ICache> cache);
    bool EnableComplianceLogging(const std::string& policy);

private:
    // Private helper methods for complex operations
    bool ValidateNewConfiguration(const LoggerConfig& config);
    bool ApplyConfiguration(const LoggerConfig& config);
    void CleanupResources();

    // Resource management
    std::shared_ptr<spdlog::logger> spdlog_impl_;
    std::unique_ptr<ICache> cache_;
    std::unique_ptr<IComplianceManager> compliance_;
};

// ❌ INCORRECT: Poor stateful class design
class BadLogger {
public:
    BadLogger() { /* No dependency injection */ }
    ~BadLogger() { /* No cleanup */ }

    // Copy allowed (resource leaks!)
    BadLogger(const BadLogger& other) = default;

    // Unclear method names
    void setup(const std::string& s);  // Unclear purpose
    bool do(const std::string& s);     // Unclear purpose
};
```

### **Layer 4 (Composition) Coding Standards**

#### **System Composition Standards:**
```cpp
// ✅ CORRECT: Well-composed system
class LoggingSystem {
public:
    // Factory method pattern for controlled creation
    static std::unique_ptr<LoggingSystem> Create(const SystemConfig& config);

    // Configuration-based initialization
    bool InitializeWithConfig(const SystemConfig& config);
    bool ReconfigureSystem(const SystemConfig& new_config);

    // Dependency injection for testing
    explicit LoggingSystem(
        std::unique_ptr<BufferManager> buffer_manager,
        std::unique_ptr<ReferenceResolver> reference_resolver,
        const SystemConfig& config
    );

    // Clear lifecycle management
    void Shutdown();
    bool IsShutdown() const;

private:
    // Composed components
    std::unique_ptr<BufferManager> buffer_manager_;
    std::unique_ptr<ReferenceResolver> reference_resolver_;
    std::unique_ptr<SystemHealthMonitor> health_monitor_;

    // Configuration
    SystemConfig current_config_;
};

// ❌ INCORRECT: Poor system composition
class BadSystem {
public:
    BadSystem() { /* Global initialization */ }
    void init() { /* Unclear initialization */ }

    // Global state (taboo!)
    static BadSystem& GetInstance() { return instance_; }
};
```

## 🌐 **Cross-Language Integration Standards**

### **C# Integration Standards**

#### **Marshaling Standards:**
```csharp
// ✅ CORRECT: Proper C# marshaling
[StructLayout(LayoutKind.Sequential, Pack = 1, CharSet = CharSet.Ansi)]
public struct LogEntryStruct
{
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
    public string timestamp;

    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
    public string status;

    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 16)]
    public string level;

    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 64)]
    public string loggerName;

    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 1024)]
    public string message;
}

// ✅ CORRECT: Safe P/Invoke usage
[DllImport("LoggingDLL.dll", CallingConvention = CallingConvention.Cdecl,
           CharSet = CharSet.Ansi, BestFitMapping = false, ThrowOnUnmappableChar = true)]
[return: MarshalAs(UnmanagedType.U1)]
private static extern bool WriteLogEntry(
    IntPtr loggerHandle,
    ref LogEntryStruct entry,
    [MarshalAs(UnmanagedType.LPStr)] StringBuilder errorMessage);

// ❌ INCORRECT: Poor marshaling
[StructLayout(LayoutKind.Auto)]  // Wrong layout
public struct BadStruct {
    public string name;  // Wrong marshaling
}
```

### **Python Integration Standards**

#### **ctypes Integration Standards:**
```python
# ✅ CORRECT: Proper ctypes usage
class LogEntryStruct(ctypes.Structure):
    _pack_ = 1  # Match C++ packing

    _fields_ = [
        # Universal header
        ("timestamp", ctypes.c_char * 32),
        ("status", ctypes.c_char * 32),
        ("data_type", ctypes.c_char * 32),
        ("version", ctypes.c_char * 8),
        ("sequence_number", ctypes.c_uint32),
        ("correlation_id", ctypes.c_char * 64),

        # Log-specific fields
        ("level", ctypes.c_char * 16),
        ("logger_name", ctypes.c_char * 64),
        ("message", ctypes.c_char * 1024),
        ("thread_id", ctypes.c_char * 16),
    ]

# ✅ CORRECT: Safe DLL usage
class LoggingDLL:
    def __init__(self, dll_path: str):
        self.dll = ctypes.CDLL(dll_path)
        self._setup_function_signatures()
        self._local_error_buffer = ctypes.create_string_buffer(256)

    def _setup_function_signatures(self):
        """Setup proper ctypes signatures"""
        self.dll.WriteLogEntry.argtypes = [
            ctypes.c_void_p,  # Logger handle
            ctypes.POINTER(LogEntryStruct),  # Log entry
            ctypes.POINTER(ctypes.c_char)    # Error message
        ]
        self.dll.WriteLogEntry.restype = ctypes.c_bool

# ❌ INCORRECT: Poor ctypes usage
class BadDll:
    def __init__(self, dll_path):
        self.dll = ctypes.CDLL(dll_path)
        # No signature setup - dangerous!
```

### **MQL5 Integration Standards**

#### **MetaTrader Integration Standards:**
```mql
// ✅ CORRECT: Proper MQL5 struct definition
#import "LoggingDLL.dll"

// Buffer management
struct BufferPlan {
    ulong requiredSizeBytes;
    ulong alignmentRequirement;
    string accessPattern;
    string bufferType;
    ulong estimatedElementCount;
    ulong elementSizeBytes;
    bool threadSafeAccess;
    ulong estimatedLifetimeMs;
};

// Universal header (matches C++ exactly)
struct UniversalDataHeader {
    uchar timestamp[32];
    uchar status[32];
    uchar dataType[32];
    uchar version[8];
    uint sequenceNumber;
    uchar correlationId[64];
    uchar sourceComponent[32];
    uchar targetSystem[32];
};

// Log entry struct (matches C++ exactly)
struct LogEntryStruct {
    UniversalDataHeader header;
    uchar level[16];
    uchar loggerName[64];
    uchar message[1024];
    uchar threadId[16];
    uchar sourceFile[256];
    int sourceLine;
    uchar sessionId[64];
    ulong nanoseconds;
};

// DLL function declarations with proper types
bool CalculateBufferPlan(string operationType, ulong estimatedDataSize, BufferPlan& plan);
void* AllocateBuffer(BufferPlan& plan, string& errorMessage);
bool WriteLogEntry(void* loggerHandle, LogEntryStruct& entry, string& errorMessage);

#import

// ✅ CORRECT: Safe MQL5 usage
class MQL5LoggingClient {
private:
    void* logger_handle_;

public:
    bool Initialize() {
        BufferPlan plan;
        if (!CalculateBufferPlan("MQL5_LOGGING", 1000, plan)) {
            return false;
        }

        string error_msg;
        logger_handle_ = AllocateBuffer(plan, error_msg);
        return logger_handle_ != NULL;
    }
};

// ❌ INCORRECT: Poor MQL5 usage
#import "LoggingDLL.dll"
bool WriteLog(string message);  // Wrong signature
#import
```

## 📋 **Error Handling Standards**

### **Consistent Error Handling Pattern:**
```cpp
// ✅ CORRECT: Comprehensive error handling
class ErrorAwareComponent {
public:
    // Operations return Result<T>
    Result<LoggerHandle> CreateLogger(const LoggerConfig& config) {
        // Validate configuration
        if (!ValidateConfig(config)) {
            return Result<LoggerHandle>::Error("Invalid configuration: " + GetValidationErrors());
        }

        // Attempt creation
        try {
            auto logger = AttemptCreateLogger(config);
            if (!logger) {
                return Result<LoggerHandle>::Error("Logger creation failed");
            }

            return Result<LoggerHandle>::Success(logger);
        }
        catch (const std::exception& ex) {
            return Result<LoggerHandle>::Error("Exception during creation: " + std::string(ex.what()));
        }
    }

private:
    bool ValidateConfig(const LoggerConfig& config) {
        return !config.name.empty() &&
               config.level != LogLevel::Off &&
               !config.pattern.empty();
    }
};

// ❌ INCORRECT: Poor error handling
class BadComponent {
public:
    bool CreateLogger(const std::string& name) {
        if (name.empty()) {
            // No error reporting!
            return false;
        }
        // No exception safety!
        return true;
    }
};
```

## ✅ **Quality Assurance Standards**

### **Code Quality Gates:**
- [ ] Zero static analysis warnings
- [ ] Zero compiler warnings
- [ ] 100% interface compliance
- [ ] No hardcoded values
- [ ] No nested logic deeper than 3 levels

### **Documentation Standards:**
- [ ] Every public method documented
- [ ] Complex algorithms explained
- [ ] Performance characteristics documented
- [ ] Thread-safety guarantees stated

### **Testing Standards:**
- [ ] Unit tests for all Layer 1 functions
- [ ] Integration tests for Layer 3 components
- [ ] Cross-language compatibility tests
- [ ] Performance benchmarks

## 📚 **Related Documents**

- **Core Principles** - NoHardcodedValues, HelperMethodsOverNestedLogic, MultiTierArchitecture
- **Implementation Tasks** - Detailed implementation guides
- **API Contracts** - Interface specifications
- **Schema Definitions** - Data structure specifications

---

**Standards Version**: 1.0 | **Last Updated**: 2025-10-10 | **Status**: ✅ Active