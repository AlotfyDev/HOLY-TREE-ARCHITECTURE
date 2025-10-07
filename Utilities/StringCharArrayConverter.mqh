#ifndef __STRINGCHARARRAYCONVERTER_MQH__
#define __STRINGCHARARRAYCONVERTER_MQH__

#include <Arrays/ArrayChar.mqh>
#include <Strings/String.mqh>

//+------------------------------------------------------------------+
//| Bidirectional String/Char Array Converter                        |
//+------------------------------------------------------------------+
class CStringCharArrayConverter
{
private:
    // Internal buffer for conversions
    CArrayChar m_charBuffer;

public:
    // Constructor
    CStringCharArrayConverter()
    {
        m_charBuffer.Resize(1024); // Initial buffer size
    }

    //+------------------------------------------------------------------+
    //| Convert String to Char Array                                     |
    //+------------------------------------------------------------------+
    bool StringToCharArray(const string source, uchar &target[])
    {
        // Clear the target array
        ArrayResize(target, 0);

        // Get string length
        int length = StringLen(source);
        if(length == 0)
        {
            return true; // Empty string is valid
        }

        // Resize target array
        if(ArrayResize(target, length) == -1)
        {
            return false; // Failed to resize
        }

        // Copy characters
        for(int i = 0; i < length; i++)
        {
            target[i] = (uchar)StringGetCharacter(source, i);
        }

        return true;
    }

    //+------------------------------------------------------------------+
    //| Convert Char Array to String                                     |
    //+------------------------------------------------------------------+
    bool CharArrayToString(const uchar &source[], string &target)
    {
        int length = ArraySize(source);
        if(length == 0)
        {
            target = "";
            return true; // Empty array is valid
        }

        // Build string from char array
        target = "";
        for(int i = 0; i < length; i++)
        {
            target += (char)source[i];
        }

        return true;
    }

    //+------------------------------------------------------------------+
    //| Convert String to Fixed Char Array (with padding)                |
    //+------------------------------------------------------------------+
    bool StringToFixedCharArray(const string source, uchar &target[], const int fixedSize, const uchar padding = 0)
    {
        int sourceLength = StringLen(source);

        // Resize target array to fixed size
        if(ArrayResize(target, fixedSize) == -1)
        {
            return false;
        }

        // Clear array first
        ArrayFill(target, 0, fixedSize, padding);

        // Copy string characters
        int copyLength = MathMin(sourceLength, fixedSize);
        for(int i = 0; i < copyLength; i++)
        {
            target[i] = (uchar)StringGetCharacter(source, i);
        }

        return true;
    }

    //+------------------------------------------------------------------+
    //| Convert Fixed Char Array to String (trim padding)                |
    //+------------------------------------------------------------------+
    bool FixedCharArrayToString(const uchar &source[], string &target, const uchar padding = 0)
    {
        int size = ArraySize(source);
        target = "";

        for(int i = 0; i < size; i++)
        {
            uchar charValue = source[i];
            if(charValue == padding)
            {
                break; // Stop at first padding character
            }
            target += (char)charValue;
        }

        return true;
    }

    //+------------------------------------------------------------------+
    //| Get Required Buffer Size for String                              |
    //+------------------------------------------------------------------+
    int GetBufferSizeForString(const string source)
    {
        return StringLen(source) + 1; // +1 for null terminator if needed
    }

    //+------------------------------------------------------------------+
    //| Validate Char Array                                               |
    //+------------------------------------------------------------------+
    bool IsValidCharArray(const uchar &array[])
    {
        return ArraySize(array) >= 0; // Basic validation
    }

    //+------------------------------------------------------------------+
    //| Clear Converter                                                  |
    //+------------------------------------------------------------------+
    void Clear()
    {
        m_charBuffer.Clear();
        m_charBuffer.Resize(1024);
    }
};

#endif // __STRINGCHARARRAYCONVERTER_MQH__