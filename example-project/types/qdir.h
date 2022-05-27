#pragma once

#include <QFile>
#include <QDir>
#include <QTemporaryDir>
#include <QDebug>

void DemoQDir() {
    QDir d1;
    QDir d2{"/not-existing"};

    QTemporaryDir td;
    QDir d3{td.path()};
}