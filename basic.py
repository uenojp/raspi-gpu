#!/bin/env python3

from videocore6.assembler import qpu
from videocore6.driver import Driver


@qpu
def kernel(asm):
    nop()
    exit()


def main():
    with Driver() as drv:
        kernel_code = drv.program(kernel)
        nqpus = 1
        drv.execute(kernel_code, thread=nqpus)


if __name__ == '__main__':
    main()
