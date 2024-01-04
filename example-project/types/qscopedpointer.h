#pragma once

#include <QString>
#include <QScopedPointer>


void DemoQScopedPointer() {
    const QScopedPointer<QObject> qspNull(nullptr);

    const QScopedPointer<QString> qspStr(new QString("Scoped pointer string"));
}