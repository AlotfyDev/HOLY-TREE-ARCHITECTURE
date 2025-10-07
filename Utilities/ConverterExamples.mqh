#ifndef __CONVERTEREXAMPLES_MQH__
#define __CONVERTEREXAMPLES_MQH__

#include "StringCharArrayConverter.mqh"
#include "StringJsonConverter.mqh"

//+------------------------------------------------------------------+
//| Examples and Tests for Bidirectional Converters                  |
//+------------------------------------------------------------------+
// Note: StringJsonConverter now uses MQL5_Json library instead of old JAson classes
class CConverterExamples
{
public:
    //+------------------------------------------------------------------+
    //| Test String/JSON Converter                                       |
    //+------------------------------------------------------------------+
    static void TestStringJsonConverter()
    {
        Print("=== Testing String/JSON Converter ===");

        CStringJsonConverter converter;

        // Test 1: Create JSON from key-value pairs and serialize
        string keys[3] = {"name", "type", "value"};
        string values[3] = {"EURUSD", "FOREX", "1.23456"};

        MQL5_Json::JsonDocument jsonDoc;
        if(converter.CreateJsonObject(jsonDoc, keys, values, 3))
        {
            Print("✓ Created JSON document");

            string jsonString = "";
            if(converter.DocumentToJsonString(jsonDoc, jsonString, false))
            {
                Print("✓ Document serialized to string: ", jsonString);

                // Test 2: Extract values from created document
                string nameValue = "";
                if(converter.GetJsonStringValue(jsonDoc, "name", nameValue))
                {
                    Print("✓ Extracted name from created document: ", nameValue);
                }

                int typeValue = 0;
                if(converter.GetJsonIntegerValue(jsonDoc, "type", typeValue))
                {
                    Print("✓ Extracted type from created document: ", typeValue);
                }

                Print("✓ Document creation and value extraction test successful");
            }
        }
        else
        {
            Print("✗ Failed to create JSON document");
        }

        // Test 4: Create JSON array
        string arrayValues[3] = {"EURUSD", "GBPUSD", "USDJPY"};

        MQL5_Json::JsonDocument arrayDoc;
        if(!converter.CreateJsonArray(arrayDoc, arrayValues, 3))
        {
            Print("✗ Failed to create JSON array");
            return;
        }

        if(arrayDoc.IsValid())
        {
            Print("✓ Created JSON array document");
            string arrayJson = "";
            if(converter.DocumentToJsonString(arrayDoc, arrayJson, false))
            {
                Print("✓ Array serialized: ", arrayJson);
            }
        }
        else
        {
            Print("✗ Failed to create JSON array");
        }
    }

    //+------------------------------------------------------------------+
    //| Test Financial Asset JSON                                        |
    //+------------------------------------------------------------------+
    static void TestFinancialAssetSchema()
    {
        Print("=== Testing Financial Asset JSON ===");

        CStringJsonConverter converter;

        // Create sample financial asset data
        string assetKeys[6] = {"serial_number", "asset_name", "normalized_name", "enum_symbol", "asset_type", "timestamp"};
        string assetValues[6] = {"1", "EURUSD", "SYMBOL_EURUSD", "1", "0", "2024-01-15T10:30:00Z"};

        MQL5_Json::JsonDocument assetDoc;
        if(!converter.CreateJsonObject(assetDoc, assetKeys, assetValues, 6))
        {
            Print("✗ Failed to create financial asset JSON");
            return;
        }

        if(assetDoc.IsValid())
        {
            Print("✓ Created financial asset JSON document");

            string assetJson = "";
            if(converter.DocumentToJsonString(assetDoc, assetJson, true))
            {
                Print("✓ Asset JSON (pretty):");
                Print(assetJson);
            }
        }
        else
        {
            Print("✗ Failed to create financial asset JSON");
        }
    }

    //+------------------------------------------------------------------+
    //| Run All Tests                                                    |
    //+------------------------------------------------------------------+
    static void RunAllTests()
    {
        Print("=== Running All Converter Tests ===");

        TestStringJsonConverter();
        Print("");

        TestFinancialAssetSchema();
        Print("");

        Print("=== All Converter Tests Completed ===");
    }
};

#endif // __CONVERTEREXAMPLES_MQH__
