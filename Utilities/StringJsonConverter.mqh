#ifndef __STRINGJSONCONVERTER_MQH__
#define __STRINGJSONCONVERTER_MQH__

#include <Strings/String.mqh>
#include <Json/JsonLib.mqh>


//+------------------------------------------------------------------+
//| Bidirectional String/JSON Converter                              |
//+------------------------------------------------------------------+
// Note: Use MQL5_Json::JsonParse(), MQL5_Json::JsonNewObject(), MQL5_Json::JsonNewArray()
// for parsing. This converter provides utility methods for working with JsonDocument objects.
class CStringJsonConverter
{
private:
    // No serializer member needed with new JSON library

public:
    // Constructor
    CStringJsonConverter()
    {
    }

    //+------------------------------------------------------------------+
    //| Convert Document to JSON String                                  |
    //+------------------------------------------------------------------+
    bool DocumentToJsonString(MQL5_Json::JsonDocument &jsonDoc, string &jsonString, bool pretty = false)
    {
        if(!jsonDoc.IsValid())
        {
            jsonString = "{}";
            return true;
        }

        jsonString = jsonDoc.ToString(pretty);
        return true;
    }

    //+------------------------------------------------------------------+
    //| Create JSON Object from Key-Value Pairs                          |
    //+------------------------------------------------------------------+
    bool CreateJsonObject(MQL5_Json::JsonDocument &doc, const string &keys[], const string &values[], const int count)
    {
        doc = MQL5_Json::JsonNewObject();

        for(int i = 0; i < count; i++)
        {
            doc.GetRoot().Set(keys[i], values[i]);
        }

        return true;
    }

    //+------------------------------------------------------------------+
    //| Create JSON Array from String Array                              |
    //+------------------------------------------------------------------+
    bool CreateJsonArray(MQL5_Json::JsonDocument &doc, const string &values[], const int count)
    {
        doc = MQL5_Json::JsonNewArray();

        for(int i = 0; i < count; i++)
        {
            doc.GetRoot().Add(values[i]);
        }

        return true;
    }

    //+------------------------------------------------------------------+
    //| Extract String Value from JSON Document                          |
    //+------------------------------------------------------------------+
    bool GetJsonStringValue(MQL5_Json::JsonDocument &jsonDoc, const string key, string &value)
    {
        if(!jsonDoc.IsValid() || !jsonDoc.GetRoot().IsObject())
        {
            return false;
        }

        value = jsonDoc.GetRoot().Get(key).AsString("");
        return true;
    }

    //+------------------------------------------------------------------+
    //| Extract Integer Value from JSON Document                         |
    //+------------------------------------------------------------------+
    bool GetJsonIntegerValue(MQL5_Json::JsonDocument &jsonDoc, const string key, int &value)
    {
        if(!jsonDoc.IsValid() || !jsonDoc.GetRoot().IsObject())
        {
            return false;
        }

        value = (int)jsonDoc.GetRoot().Get(key).AsInt(0);
        return true;
    }

    //+-------------------------------------------------------------------+
    //| Extract Boolean Value from JSON Document                         |
    //+-------------------------------------------------------------------+
    bool GetJsonBooleanValue(MQL5_Json::JsonDocument &jsonDoc, const string key, bool &value)
    {
        if(!jsonDoc.IsValid() || !jsonDoc.GetRoot().IsObject())
        {
            return false;
        }

        value = jsonDoc.GetRoot().Get(key).AsBool(false);
        return true;
    }

    // Optional methods removed to resolve compilation issues
};

#endif // __STRINGJSONCONVERTER_MQH__
