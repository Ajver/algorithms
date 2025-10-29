#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <linux/prctl.h>
#include <sys/prctl.h>
#include <stdarg.h>

enum {
    GRANDPA,
    PARENT,
    CHILD,
};

int hierarchy_level = GRANDPA;
int indends = 0;


void printf_ind(const char* text, ...) {
    va_list valist;
    va_start(valist, text);

    char *formatted;

    for (int i=0; i<indends; i++) printf(" ");

    vprintf(text, valist);
    va_end(valist);
}


char* read_file(char filepath[]) {
    const size_t length = 15;
    char* buffer = malloc(length);
    FILE* f = fopen (filepath, "r");

    if (f) {
        fread(buffer, 1, length, f);
        
        // Remove trailing line break
        for (char* ptr = buffer; ptr < buffer + length; ptr++) {
            if (*ptr == '\n') {
                *ptr = '\0';
            }
        }
        fclose(f);
    } else {
        printf_ind("cant open a file: %s", filepath);
        buffer[length-1] = '\0';
    }

    return buffer;
}


void print_info() {
    int pid = getpid();
    int ppid = getppid();
    char* proc_comm = read_file("/proc/self/comm");
    char* proc_cmdline = read_file("/proc/self/cmdline");

    printf_ind("pid=%d, ppid=%d, name=%s, cmdline=%s\n", pid, ppid, proc_comm, proc_cmdline);
}


int main() {
    print_info();

    int fork_pid = fork();
    
    if (fork_pid != 0) {
        // It's the parent process!
        prctl(PR_SET_NAME, "Rodzic");
        print_info();
    } else {
        // It's the child process!
        
        indends += 2;

        prctl(PR_SET_NAME, "Potomek");
        print_info();

        int grandchild_pid = fork();

        if (grandchild_pid != 0) {
            hierarchy_level = PARENT;
            prctl(PR_SET_NAME, "Rodzic");
        }else {
            indends += 2;
            hierarchy_level = CHILD;

            prctl(PR_SET_NAME, "Dziecko");
        }
    }

    if (fork_pid != 0) {
        prctl(PR_SET_NAME, "Dziadek");
    }

    print_info();


    if (hierarchy_level == GRANDPA) {
        int fork_id = fork();
        if (fork_id == 0) {
            indends += 2;
            hierarchy_level = PARENT;
            prctl(PR_SET_NAME, "Wujek");
            print_info();
        }
    }else if (hierarchy_level == PARENT) {
        int fork_id = fork();
        if (fork_id == 0) {
            indends += 2;
            hierarchy_level = CHILD;
            prctl(PR_SET_NAME, "Brat");
            print_info();
        }
    }

    // const char proc_name[16];
    // prctl(PR_GET_NAME, proc_name);
    // printf_ind("process name: %s\n", proc_name);

    getchar();

    return 0;
}
