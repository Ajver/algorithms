# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.30

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib/build

# Include any dependencies generated for this target.
include CMakeFiles/hello_library.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/hello_library.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/hello_library.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/hello_library.dir/flags.make

CMakeFiles/hello_library.dir/src/hello.c.o: CMakeFiles/hello_library.dir/flags.make
CMakeFiles/hello_library.dir/src/hello.c.o: /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib/src/hello.c
CMakeFiles/hello_library.dir/src/hello.c.o: CMakeFiles/hello_library.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/media/dom/Wkspce/GitRepos/algorithms/L3_DynLib/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/hello_library.dir/src/hello.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/hello_library.dir/src/hello.c.o -MF CMakeFiles/hello_library.dir/src/hello.c.o.d -o CMakeFiles/hello_library.dir/src/hello.c.o -c /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib/src/hello.c

CMakeFiles/hello_library.dir/src/hello.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/hello_library.dir/src/hello.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib/src/hello.c > CMakeFiles/hello_library.dir/src/hello.c.i

CMakeFiles/hello_library.dir/src/hello.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/hello_library.dir/src/hello.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib/src/hello.c -o CMakeFiles/hello_library.dir/src/hello.c.s

# Object files for target hello_library
hello_library_OBJECTS = \
"CMakeFiles/hello_library.dir/src/hello.c.o"

# External object files for target hello_library
hello_library_EXTERNAL_OBJECTS =

libhello_library.so: CMakeFiles/hello_library.dir/src/hello.c.o
libhello_library.so: CMakeFiles/hello_library.dir/build.make
libhello_library.so: CMakeFiles/hello_library.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/media/dom/Wkspce/GitRepos/algorithms/L3_DynLib/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C shared library libhello_library.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/hello_library.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/hello_library.dir/build: libhello_library.so
.PHONY : CMakeFiles/hello_library.dir/build

CMakeFiles/hello_library.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/hello_library.dir/cmake_clean.cmake
.PHONY : CMakeFiles/hello_library.dir/clean

CMakeFiles/hello_library.dir/depend:
	cd /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib/build /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib/build /media/dom/Wkspce/GitRepos/algorithms/L3_DynLib/build/CMakeFiles/hello_library.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/hello_library.dir/depend

