#pragma once

#include <QString>
#include <QSharedPointer>

void DemoQSharedPointer() {
    const QSharedPointer<QString> qspStr(new QString("Shared pointer string"));
    const QWeakPointer<QString> weakRef = qspStr.toWeakRef();
}