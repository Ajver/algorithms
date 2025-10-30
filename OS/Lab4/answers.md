# Pytania:

## Co stanie się z procesem wnuka, jeśli zabijesz (kill -9) proces rodzica, wujka lub dziadka?

1. Rodzica - nic. Za to Rodzic staje sie zombie (defunct)
2. Wujka - nic. Za to Wujek staje sie zombie (defunct)
3. Dziadka - Wszyscy zostają zabici

## Jak zmienia się PPID osieroconych procesów (adopcja przez init/systemd)?

Zmienia się na proces systemd

## Wskaż, który proces przejmuje rolę rodzica (np. init/systemd) i potwierdź w /proc/<PID>/status.
 
```sh
ps -o pid,state,ppid,cmd -p <pid-dziecka>  # wyswietli ppid
kill -9 <pid-rodzica>
ps -o pid,state,ppid,cmd -p <pid-dziecka>  # wyswietli nowe ppid
ps -o pid,state,ppid,cmd -p <nowe-ppid>  # wyswietli proces systemd
cat /proc/<PID>/status  # wyswietli wszystkie dane
```

## Co się stanie z procesem zombie, jeśli rodzic nie wywoła wait()?

Bedzie wisiec w otchlani nicosci... - nie zajmuje CPU ale widnieje ciagle na liscie procesow

## Jak wygląda jego stan w ps (STAT=Z) i w /proc/<PID>/status?

```sh
# np zabijajac Proces rodzica:
kill -9 <pid-rodzica>
```

```sh
$ ps -o pid,state,ppid,cmd -p <pid-rodzica>
    PID S    PPID CMD
  34879 Z   34878 [Rodzic] <defunct>

```

Wiecej danych:

```sh
$ cat /proc/<pid-rodzica>/status
Name:	Rodzic
State:	Z (zombie)
...
```

## Jak można usunąć zombie bez restartu systemu?

Np. zabijajac rodzica Zombie (np. Dziadka)

## Jak zmienia się drzewo procesów po wysłaniu sygnału SIGSTOP do rodzica?

```sh
$ pstree -p
```

Przed:
```
├─bash(31536)───Dziadek(35378)─┬─Rodzic(35379)─┬─Brat(35382)
│                              │               └─Dziecko(35381)
│                              └─Wujek(35380)
```

Po
```
├─bash(31536)───Dziadek(35378)─┬─Rodzic(35379)─┬─Brat(35382)
│                              │               └─Dziecko(35381)
│                              └─Wujek(35380)
```

Nie zmienia się


## Czy dzieci nadal działają?

Tak

## Jak to widać w pstree i w polu STAT?

W pstree wygląda "normalnie"

Ale rodzic dostaje flage T (TASK_STOPPED)
```sh
$ $ ps -o pid,state,ppid,cmd -p 35379
    PID S    PPID CMD
  35379 T   35378 ./pokolenia.out
```

```sh
$ cat /proc/35379/status
Name:	Rodzic
Umask:	0022
State:	T (stopped)
...
```

## Czy proces „Brat” i „Wujek” mają wspólnego rodzica?

Nie

## Jak wygląda ich PPID w ps?

```sh
$ ps -eo pid,state,ppid,comm
    PID S    PPID COMMAND
...
  35378 S   31536 Dziadek
  35379 T   35378 Rodzic
  35380 S   35378 Wujek
  35381 S   35379 Dziecko
  35382 S   35379 Brat
...
```

## Jak można potwierdzić relacje w /proc/<PID>/status?

```sh
$ cat /proc/36047/status
Name:	Brat
Umask:	0022
State:	S (sleeping)
Tgid:	36047
Ngid:	0
Pid:	36047
PPid:	36044
...
```

```sh
$ cat /proc/36045/status
Name:	Wujek
Umask:	0022
State:	S (sleeping)
Tgid:	36045
Ngid:	0
Pid:	36045
PPid:	36043
...
```

Maja rozne PPid

## Jak zmienia się nazwa procesu w ps po użyciu prctl(PR_SET_NAME)?

Zmienia sie kolumna COMMAND

Np.
```
36044 S   36043 Potomek -> 36044 S   36043 Rodzic
```

## Czy zmiana wpływa na /proc/<PID>/cmdline?

```sh
$ cat /proc/36044/cmdline
./pokolenia.out
```

Wyswietla zawsze komende, z ktorej program byl uruchomiony. Np.:

```sh
$ gcc pokolenia.c -o pokolenia.out && ./pokolenia.out
```

## Jakie pole w ps pokazuje nową nazwę (comm vs args)?

```sh
$ ps -eo pid,state,ppid,comm,args
    PID S    PPID COMMAND         COMMAND
...
  36298 S   31536 Dziadek         ./pokolenia.out
  36299 S   36298 Rodzic          ./pokolenia.out
  36300 S   36298 Wujek           ./pokolenia.out
  36301 S   36299 Dziecko         ./pokolenia.out
  36302 S   36299 Brat            ./pokolenia.out
...
```

-> comm.

Z jakiegos powodu obie kolumny sa tak samo nazwane w outpucie `ps`. Ale nowa nazwe pokazuje ta z polcenia `comm`.
