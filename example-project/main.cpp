#include "types/pointer.h"
#include "types/qatomicint.h"
#include "types/qbitarray.h"
#include "types/qbytearray.h"
#include "types/qchar.h"
#include "types/qdate.h"
#include "types/qdatetime.h"
#include "types/qdir.h"
#include "types/qevent.h"
#include "types/qfile.h"
#include "types/qfileinfo.h"
#include "types/qflags.h"
#include "types/qhash.h"
#include "types/qhostaddress.h"
#include "types/qlist.h"
#include "types/qlocale.h"
#include "types/qmap.h"
#include "types/qmodelindex.h"
#include "types/qstring.h"
#include "types/qtemporarydir.h"
#include "types/qsharedpointer.h"
#include "types/qtime.h"
#include "types/qtimezone.h"
#include "types/qurl.h"
#include "types/quuid.h"
#include "types/qvariant.h"

int main()
{
    DemoPointer();
    DemoQAtomicInt();
    DemoQBitArray();
    DemoQByteArray();
    DemoQChar();
    DemoQDate();
    DemoQDateTime();
    DemoQDir();
    DemoQEvent();
    DemoQFile();
    DemoQFileInfo();
    DemoQFlags();
    DemoQHash();
    DemoQHostAddress();
    DemoQList();
    DemoQLocale();
    DemoQMap();
    DemoQModelIndex();
    DemoQString();
    DemoQTemporaryDir();
    DemoQSharedPointer();
    DemoQTime();
    DemoQTimeZone();
    DemoQUrl();
    DemoQUuid();
    DemoQVariant();
    return 0;
}
