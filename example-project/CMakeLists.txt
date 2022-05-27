cmake_minimum_required(VERSION 3.20)
project(QTTypesExample VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_FIND_DEBUG_MODE FALSE)
find_package(QT NAMES Qt6 CONFIG COMPONENTS Widgets Network Gui Test REQUIRED)
find_package(Qt${QT_VERSION_MAJOR} COMPONENTS Widgets Network Gui Test REQUIRED)

qt_add_executable(QTTypesExample main.cpp)
target_link_libraries(QTTypesExample PRIVATE Qt${QT_VERSION_MAJOR}::Core Qt${QT_VERSION_MAJOR}::Network Qt${QT_VERSION_MAJOR}::Gui)


