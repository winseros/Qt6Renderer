#pragma once

#include <QObject>
#include <QModelIndex>
#include <QStringListModel>
#include <QStringList>

void DemoQModelIndex() {
    QStringList items;
    items.append("s1");
    items.append("s2");
    items.append("s3");
    QStringListModel model(items);
    QModelIndex index1 = model.index(1, 0);
    QModelIndex index2 = model.index(0, 1);
}