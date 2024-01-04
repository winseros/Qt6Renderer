#pragma once

#include <QString>
#include <QSharedPointer>
#include <QPointer>

struct BaseStruct {
    int baseProp;
};

struct InheritedStruct: public BaseStruct {
    int inheritedProp;
};

void DemoQSharedPointer() {
    const QSharedPointer<QObject> qspNull(nullptr);
    const QWeakPointer<QObject> weakRefNull = qspNull.toWeakRef();

    const QSharedPointer<QString> qspStr(new QString("Shared pointer string"));
    const QWeakPointer<QString> weakRef = qspStr.toWeakRef();

    const QSharedPointer<BaseStruct> qspInh(new InheritedStruct{1, 2});

    const QSharedPointer<QObject> qspObj(new QObject);
    const QPointer<QObject> qpObj = qspObj.data();
}