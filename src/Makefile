OPT_FLAGS := -O2
WARN_FLAGS := -Wall -Wextra -Werror -pedantic -Wconversion

all: libclpsolve.so
.PHONY: all

libclpsolve.so:	clp_solve.o
	$(CC) $(OPT_FLAGS) $(WARN_FLAGS) -shared -Wl,-soname,$@ -o $@ $^

%.o:	%.cpp
	$(CC) $(OPT_FLAGS) $(WARN_FLAGS) -fPIC -c $^

clean:
	rm -f libclpsolve.so
	rm -f clp_solve.o
.PHONY: clean
