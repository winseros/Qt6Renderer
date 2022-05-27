#pragma once

#include <QFileInfo>
#include <QDir>
#include <QTemporaryFile>
#include <QDebug>

void DemoQFileInfo() {
    QFileInfo fi1;
    QFileInfo fi2{QDir::tempPath()};

    QTemporaryFile tf;
    tf.open();
    tf.close();
    QFileInfo fi3{tf.fileName()};
}