# Hardcoded Values Hunter Protocol

## 🔍 **AUTOMATED HARDCODED VALUES DETECTION & ERADICATION PROTOCOL**

### **Mission Objective**
**Zero Tolerance for Hardcoded Values in Layer 1** - Complete architectural purity through systematic automated detection and elimination.

---

### **📊 CURRENT THREAT ASSESSMENT (Latest Scan Results)**

**Total Layer 1 Violations:** 628 ❌
- **Float Literals:** 379 (60% of violations) - Algorithm constants embedded in code
- **String Literals:** 163 (26% of violations) - Hardcoded text/assets in pure logic
- **Integer Literals:** 86 (14% of violations) - Magic numbers and defaults

### **🎯 HIGH-PRIORITY TARGET FILES**

| **File** | **Violations** | **Status** | **Next Action** |
|----------|----------------|------------|-----------------|
| `TemporalQueryToolbox.hpp` | 129 | ⚠️ **RED ALERT** | Immediate parameter extraction required |
| `TemporalCalculationToolbox.hpp` | 99 | ⚠️ **CRITICAL** | Header function signature updates |
| `TemporalQueryToolbox.cpp` | 76 | 🔴 **BLOCKED** | Implementation purge needed |
| `TemporalCalculationToolbox.cpp` | ~~36~~ | ✅ **CLEARED** | Previously purified during crusade |
| `Other Layer 1 files` | Remaining | 🚨 **PENDING** | Systematic sweeps required |

---

### **🔧 AUTOMATED DETECTION TOOL: `hardcoded_values_scanner.py`**

**Capabilities:**
- **Pattern Recognition:** Integer, float, string literal detection with C++ context
- **Layer 1 Focus:** Prioritizes toolbox files with strict "No Hardcoded Values" taboo
- **Severity Classification:** High-severity for Layer 1 violations
- **Tabular Output:** Sortable by violation count for efficient triage
- **JSON Export:** Allows integration with CI/CD quality gates

**Usage:**
```bash
# Quick scan of Layer 1
python hardcoded_values_scanner.py --path src/Layer1/ --format tab

# Full project scan with violations exported
python hardcoded_values_scanner.py --path src/ --output violations.json --format json
```

---

### **🎯 ERADICATION STRATEGY BY VIOLATION TYPE**

#### **1. Float Literals Strategy (379 violations - 60%)**
```cpp
// ❌ VIOLATION PATTERN
double CalculateEfficiency(double input, size_t count) {
    return std::log10(input) / 10.0;  // Magic 10.0
}

// ✅ CORRECTION PROTOCOL
double CalculateEfficiency(double input, size_t count, double scaling_factor) {
    return std::log10(input) / scaling_factor;  // Parameterized
}
```

**Template for Float Eradication:**
1. **Function Signature:** Add `double [parameter_name] = [current_value]` parameter
2. **Usage Update:** Replace hardcoded value with parameter
3. **Default Preservation:** Maintain working code with same default behavior

#### **2. String Literals Strategy (163 violations - 26%)**
```cpp
// ❌ VIOLATION PATTERN
std::string result = calculate() + "ms";  // Magic string

// ✅ CORRECTION PROTOCOL
std::string result = calculate() + time_unit_suffix;  // Parameterized suffix
```

**String Eradication Protocol:**
1. **Mode Analysis:** Determine if string is format, constant, or content
2. **Parameter Introduction:** Add string parameter when string varies
3. **Layer Evaluation:** Only eradicate if string represents domain logic

#### **3. Integer Literals Strategy (86 violations - 14%)**
```cpp
// ❌ VIOLATION PATTERN
if (count > 100) return true;  // Magic threshold

// ✅ CORRECTION PROTOCOL
if (count > threshold) return true;  // Configurable threshold
```

---

### **🚀 SYSTEMATIC ERADICATION WORKFLOW**

#### **Phase 1: Header File Cleanup (129 violations in TemporalQueryToolbox.hpp)**
```bash
# Step 1: Identify function signatures needing parameters
python hardcoded_values_scanner.py --path src/Layer1/TemporalQueryToolbox.hpp --format json

# Step 2: Add parameters systematically
# Pattern: Find violating line -> Add parameter to function signature -> Default to current value

# Step 3: Validate header compilation
g++ -fsyntax-only src/Layer1/TemporalQueryToolbox.hpp
```

#### **Phase 2: Implementation File Purge (76 violations in TemporalQueryToolbox.cpp)**
```bash
# Step 1: Update function implementations to use new parameters
# Pattern: Match hardcoded value -> Replace with parameter reference

# Step 2: Unit test preservation (function still works with defaults)
# Step 3: Compilation validation
```

#### **Phase 3: Cross-File Consistency**
```bash
# Step 1: Scan all files referencing updated functions
# Step 2: Update call sites (may need to pass existing values)
# Step 3: Regression testing
```

---

### **📋 VIOLATIONS ERADICATION CHECKLIST**

- [ ] **TemporalQueryToolbox.hpp** (129 violations) - Function signature updates
- [ ] **TemporalCalculationToolbox.hpp** (99 violations) - Header cleanup phase 2
- [ ] **TemporalQueryToolbox.cpp** (76 violations) - Implementation purge
- [ ] **BufferCalculationToolbox.* ** (Pending) - Architecture scan required
- [ ] **ConversionToolbox.* ** (Pending) - Architecture scan required
- [ ] **TimeConversionToolbox.* ** (Pending) - Architecture scan required
- [ ] **TimestampParsingToolbox.* ** (Pending) - Architecture scan required
- [ ] **PerformanceToolbox.* ** (Pending) - Architecture scan required
- [ ] **ValidationToolbox.* ** (Pending) - Architecture scan required
- [ ] **Cross-File References** - Update all callers of modified functions

---

### **🏆 SUCCESS METRICS**

**Target State:** Zero "High Severity" violations in Layer 1 files

**Measure of Success:**
- Scanner reports: "Total Layer 1 Violations: 0"
- Code review: No hardcoded values in pure logic functions
- Architecture validation: Layer 1 functions are truly stateless and configurable

---

### **🚨 EMERGENCY INTERVENTION PROTOCOL**

**If violation count increases:**
1. **Immediate freeze** on new Layer 1 development
2. **Root cause analysis** - identify introduction point
3. **Code review audit** - prevent future violations

**If compilation breaks from removals:**
1. **Conservative defaults** - temporarily preserve functioning code
2. **Incremental approach** - fix one function at a time
3. **Partner coordination** - ensure Layer 2/3 can absorb new parameters

---

### **🛠️ QUALITY ASSURANCE INTEGRATION**

**CI/CD Pipeline Integration:**
```yaml
# In build pipeline
- name: "Scan for Hardcoded Values"
  run: python hardcoded_values_scanner.py --path src/Layer1/ --format json
  continue-on-error: false

- name: "Enforce Zero Violations"
  run: |
    violations=$(python hardcoded_values_scanner.py --path src/Layer1/ --format json | jq '.layer1_violations')
    if [ "$violations" -gt 0 ]; then
      echo "CRITICAL: $violations hardcoded value violations in Layer 1"
      exit 1
    fi
```

---

**Status:** ⚠️ **Active Crusade** | **Progress:** 0% Layer 1 Purity Achieved | **Target:** 100% Purity

**Next Target:** `TemporalQueryToolbox.hpp` - 129 violations elimination
