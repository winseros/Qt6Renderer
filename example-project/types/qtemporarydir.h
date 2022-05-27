#pragma once

#include <QTemporaryDir>

void DemoQTemporaryDir() {
    QTemporaryDir td1;
    QTemporaryDir td2;
    td2.setAutoRemove(false);
}