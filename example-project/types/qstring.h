#pragma once

#include <QString>
#include <QSharedPointer>

void DemoQString() {
    QString str1("String data ");
    str1.reserve(100);
    str1.append("123");

    const QString str2("String data 2");

    const QSharedPointer<QString> qspStr(new QString("Shared pointer string"));
    const QString *pStr = qspStr.data();
}