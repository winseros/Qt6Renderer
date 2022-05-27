#pragma once

#include <QLocale>

void DemoQFlags(){
    QLocale::NumberOptions opts1{QLocale::NumberOption::IncludeTrailingZeroesAfterDot | QLocale::NumberOption::RejectGroupSeparator};
    QLocale::NumberOptions opts2;
}