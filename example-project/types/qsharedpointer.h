#pragma once

#include <QString>
#include <QSharedPointer>
#include <QPointer>

void DemoQSharedPointer() {
    const QSharedPointer<QString> qspStr(new QString("Shared pointer string"));
    const QWeakPointer<QString> weakRef = qspStr.toWeakRef();

    const QSharedPointer<QObject> qspObj(new QObject);
    const QPointer<QObject> qpObj = qspObj.data();
}