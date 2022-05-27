#pragma once

#include <QHash>

void DemoQHash()
{
    QHash<QString, QString> h1;
    h1.insert("k1", "v1");
    h1.insert("k2", "v2");
    h1.insert("k3", "v3");
    h1.insert("k4", "v4");
    h1.insert("k5", "v5");
    h1.insert("k6", "v6");
    h1.insert("k7", "v7");
    h1.insert("k8", "v8");
    h1.insert("k9", "v9");
    h1.insert("k10", "v10");

    QHash<char, int> h2;
    h2.insert('a', 1);
    h2.insert('b', 2);
    h2.insert('c', 3);

    QHash<short, char> h3;
    h3.insert(0, 'a');
    h3.insert(1, 'b');
    h3.insert(2, 'c');

    QHash<short, short> h4;
    h4.insert(0, 1);
    h4.insert(2, 3);
    h4.insert(4, 5);

    QHash<char, char> h5;
    h5.insert('a', 'b');
    h5.insert('c', 'd');
    h5.insert('e', 'f');

    auto it1 = h1.begin();
    while (it1 != h1.end())
        ++it1;
    auto it2 = h1.keyBegin();
    auto it3 = h1.keyValueBegin();
    auto it4 = h1.constBegin();
    auto it5 = h1.constKeyValueBegin();
}