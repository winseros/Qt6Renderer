#pragma once

#include <QMap>
#include <QString>
#include <QSharedPointer>

void DemoQMap() {
    QMap<int, int> map0;
    QMap<QString, QString> map1({{"k1", "v1"},
                                 {"k2", "v2"},
                                 {"k3", "v3"}});

    QMap<qint64, qint64> map2({{1, 2},
                               {3, 4},
                               {5, 6},
                               {7, 8},
                               {9, 10}});

    QMap<qint64, QSharedPointer<QString>> map3({{1, QSharedPointer<QString>(new QString("s1"))},
                                                {2, QSharedPointer<QString>(new QString("s2"))},
                                                {3, QSharedPointer<QString>(new QString("s3"))}});

    QMap<qint64, qint64> map4;
    map4[1] = 10;
}