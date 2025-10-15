cmake_minimum_required(VERSION 3.21 FATAL_ERROR)

# Project configuration
project(TradingRagSystem
    VERSION 1.0.0
    DESCRIPTION "Trading Software Document Intelligence RAG System"
    LANGUAGES CXX
)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Enable all warnings
if(MSVC)
    add_compile_options(/W4 /permissive-)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find required packages
find_package(Threads REQUIRED)

# Find SQLite3 - try multiple methods
find_package(SQLite3 QUIET)
if(NOT SQLite3_FOUND)
    # Try finding sqlite3 directly
    find_path(SQLite3_INCLUDE_DIRS sqlite3.h
        PATHS
        "C:/Program Files/SQLite"
        "C:/SQLite"
        "C:/vcpkg/installed/x64-windows/include"
        "/usr/include"
        "/usr/local/include"
    )

    find_library(SQLite3_LIBRARIES sqlite3
        PATHS
        "C:/Program Files/SQLite"
        "C:/SQLite"
        "C:/vcpkg/installed/x64-windows/lib"
        "/usr/lib"
        "/usr/local/lib"
    )

    if(SQLite3_INCLUDE_DIRS AND SQLite3_LIBRARIES)
        set(SQLite3_FOUND TRUE)
        message(STATUS "Found SQLite3: ${SQLite3_LIBRARIES}")
    endif()
endif()

if(NOT SQLite3_FOUND)
    message(WARNING "SQLite3 not found - some features will be disabled")
    # Create a dummy target for now
    add_library(sqlite3 INTERFACE)
    target_include_directories(sqlite3 INTERFACE "")
    set(SQLite3_LIBRARIES sqlite3)
endif()

# Include directories
if(SQLite3_FOUND)
    include_directories(${SQLite3_INCLUDE_DIRS})
endif()
include_directories(include)
include_directories(third_party)

# Source files
set(SOURCES
    src/main.cpp
    src/rag_system.cpp
    src/document_ingestion.cpp
    src/document_parser.cpp
    src/chunking_engine.cpp
    src/embedding_engine.cpp
    src/vector_index.cpp
    src/storage_manager.cpp
    src/query_engine.cpp
    src/mcp_server.cpp
    src/toolbox.cpp
)

# Header files
set(HEADERS
    include/rag_system.h
    include/document_ingestion.h
    include/document_parser.h
    include/chunking_engine.h
    include/embedding_engine.h
    include/vector_index.h
    include/storage_manager.h
    include/query_engine.h
    include/mcp_server.h
    include/common_types.h
    include/performance_monitor.h
)

# Create executable
add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# Link libraries
target_link_libraries(${PROJECT_NAME}
    Threads::Threads
)

# Link SQLite3 if found
if(SQLite3_FOUND)
    target_link_libraries(${PROJECT_NAME} ${SQLite3_LIBRARIES})
endif()

# Set output directories
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
)

# Enable testing (if GTest is available)
option(ENABLE_TESTING "Enable testing" OFF)
if(ENABLE_TESTING)
    find_package(GTest REQUIRED)
    enable_testing()
    add_subdirectory(tests)
endif()

# Installation
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# Create data directories
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/data)
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/data/documents)
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/data/indexes)
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/data/temp)

# Print configuration summary
message(STATUS "=== TradingRagSystem Configuration ===")
message(STATUS "Version: ${PROJECT_VERSION}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Install Prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "Data Directory: ${CMAKE_BINARY_DIR}/data")
message(STATUS "Testing: ${ENABLE_TESTING}")
message(STATUS "=====================================")