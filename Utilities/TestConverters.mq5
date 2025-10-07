//+------------------------------------------------------------------+
//| Test File for Bidirectional Converters                           |
//+------------------------------------------------------------------+
#property copyright "AssetsSymbolsIndex"
#property version   "1.00"

#include "StringCharArrayConverter.mqh"
#include "ConverterExamples.mqh"

//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   Print("=== Testing Bidirectional Converters ===");

// Test String/Char Array Converter
   TestCharArrayConverter();

// Test String/JSON Converter
   CConverterExamples::RunAllTests();

   Print("=== Converter Tests Completed ===");
  }

//+------------------------------------------------------------------+
//| Test Char Array Converter                                        |
//+------------------------------------------------------------------+
void TestCharArrayConverter()
  {
   Print("Testing String/Char Array Converter...");

   CStringCharArrayConverter charConverter;

// Test 1: String to Char Array
   string testString = "EURUSD";
   uchar charArray[];

   if(charConverter.StringToCharArray(testString, charArray))
     {
      Print("✓ String to Char Array: SUCCESS");
      Print("  Original: ", testString);
      Print("  Array size: ", ArraySize(charArray));

      // Test 2: Char Array back to String
      string resultString = "";
      if(charConverter.CharArrayToString(charArray, resultString))
        {
         Print("✓ Char Array to String: SUCCESS");
         Print("  Result: ", resultString);

         if(testString == resultString)
           {
            Print("✓ Round-trip conversion: SUCCESS");
           }
         else
           {
            Print("✗ Round-trip conversion: FAILED");
           }
        }
      else
        {
         Print("✗ Char Array to String: FAILED");
        }
     }
   else
     {
      Print("✗ String to Char Array: FAILED");
     }
  }

// JSON tests now run from CConverterExamples::RunAllTests()

//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
