#pragma once

#include <QList>
#include <QString>
#include <QSharedPointer>

void DemoQList() {
    QList<QString> list1({QString("s1"), QString("s2"), QString("s3")});
    QList<qint64> list2({1, 2, 3, 4, 5});
    QList<QSharedPointer<QString>> list3({
        QSharedPointer<QString>(new QString("s1")),
        QSharedPointer<QString>(new QString("s2")),
        QSharedPointer<QString>(new QString("s3")),
    });
    QList<qint64> list4;

    auto it = list1.begin();
    const auto cit = list1.constBegin();
}