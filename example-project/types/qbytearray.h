#pragma once

#include <QByteArray>

void DemoQByteArray() {
    QByteArray a1;
    QByteArray a2(10, 'a');
    QByteArray a3;
    a3.reserve(100);
    a3.append('a');
    a3.append('b');
    a3.append('c');
    a3.append('d');
    a3.append('e');
    a3.append('f');

    auto it = a3.begin();
    auto cit = a3.constBegin();
}