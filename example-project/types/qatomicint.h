#pragma once

#include <QAtomicInt>

void DemoQAtomicInt() {
    QAtomicInt i1;
    i1 = 10;
    QAtomicInt i2;
    i2.fetchAndStoreAcquire(-100);
}