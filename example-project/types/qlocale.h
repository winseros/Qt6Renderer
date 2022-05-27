#pragma once

#include <QLocale>

void DemoQLocale() {
    QLocale l1{QLocale::Language::Russian, QLocale::Script::CyrillicScript, QLocale::Country::Russia};
    QLocale l2{"en_US"};
    QLocale l3{"de"};
}