#pragma once

#include <QFile>
#include <QDir>
#include <QTemporaryFile>
#include <QDebug>

void DemoQFile() {
    QFile f1;
    QFile f2{"/tmp/ptr1"};

    QTemporaryFile tf;
    tf.open();
    tf.close();
    QFile f3{tf.fileName(), nullptr};
    auto f3Ptr = &f3;
}