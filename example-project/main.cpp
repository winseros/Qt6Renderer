#include "types/pointer.h"
#include "types/qatomicint.h"
#include "types/qbitarray.h"
#include "types/qbytearray.h"
#include "types/qchar.h"
#include "types/qdate.h"
#include "types/qdatetime.h"
#include "types/qlist.h"
#include "types/qmap.h"
#include "types/qmodelindex.h"
#include "types/qstring.h"
#include "types/qsharedpointer.h"
#include "types/qtime.h"
#include "types/qtimezone.h"

int main()
{
    DemoPointer();
    DemoQAtomicInt();
    DemoQBitArray();
    DemoQByteArray();
    DemoQChar();
    DemoQDate();
    DemoQDateTime();
    DemoQList();
    DemoQMap();
    DemoQModelIndex();
    DemoQString();
    DemoQSharedPointer();
    DemoQTime();
    DemoQTimeZone();
    return 0;
}
