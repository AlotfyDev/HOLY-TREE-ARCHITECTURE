
#ifndef __SFINANCIALASSET_MQH__
#define __SFINANCIALASSET_MQH__

 
#include "../Enums/ENUM_MARKET_SYMBOLS.mqh"
#include "../Enums/ENUM_ASSET_TYPE.mqh"
#include <Object.mqh>




class SFinancialAsset : public CObject
{
public:
    int serialNumber;      // الرقم التسلسلي
    ENUM_MARKET_SYMBOLS ESymbol;
    string assetName;      // اسم الأصل
    string normalizedName; // الاسم المقنن للإينام
    ENUM_ASSET_TYPE assetType; // نوع الأصل
    datetime timestamp;    // وقت الإضافة

    SFinancialAsset() :
        serialNumber(0),
        ESymbol(SYMBOL_UNKNOWN),
        assetName(""),
        normalizedName(""),
        assetType(ASSET_TYPE_UNKNOWN),
        timestamp(0)
    {}

    // Required for CObject containers - minimal implementation
    virtual int Compare(const CObject* node, const int mode=0) const override
    {
        return 0; // Equal for all (no meaningful comparison needed)
    }
};







#endif // __SFINANCIALASSET_MQH__
