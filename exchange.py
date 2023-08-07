#!/bin/env python3

from videocore6.assembler import qpu
from videocore6.driver import Driver


@qpu
def kernel(asm):
    # in_* and out_* are aliases for rf*.
    g = globals()
    g['in_a'] = g['rf0']
    g['in_b'] = g['rf1']
    g['out_a'] = g['rf2']
    g['out_b'] = g['rf3']

    nop(sig=ldunifrf(in_a))
    nop(sig=ldunifrf(in_b))
    nop(sig=ldunifrf(out_a))
    nop(sig=ldunifrf(out_b))

    eidx(r0)
    shl(r0, r0, 2)
    add(in_a, in_a, r0)
    add(in_b, in_b, r0)
    add(out_a, out_a, r0)
    add(out_b, out_b, r0)

    # H->D: in_b0,r11
    mov(tmua, in_a, sig=thrsw)
    nop()
    nop()
    nop(sig=ldtmu(rf10))

    mov(tmua, in_b, sig=thrsw)
    nop()
    nop()
    nop(sig=ldtmu(rf11))

    # D->H: in_b1,in_b0(swapped)
    mov(tmud, rf11)
    mov(tmua, out_a)
    tmuwt()

    mov(tmud, rf10)
    mov(tmua, out_b)
    tmuwt()

    # epilogue for sync
    nop(sig=thrsw)
    nop(sig=thrsw)
    nop()
    nop()
    nop(sig=thrsw)
    nop()
    nop()
    nop()


def main():
    with Driver() as drv:
        in_a = drv.alloc(16, 'float32')
        in_b = drv.alloc(16, 'float32')
        out_a = drv.alloc(16, 'float32')
        out_b = drv.alloc(16, 'float32')

        in_a[:] = 2.0
        in_b[:] = 3.0
        out_a[:] = 0.0
        out_b[:] = 0.0

        unif = drv.alloc(4, 'uint32')
        unif[0] = in_a.addresses()[0]
        unif[1] = in_b.addresses()[0]
        unif[2] = out_a.addresses()[0]
        unif[3] = out_b.addresses()[0]

        kernel_code = drv.program(kernel)
        nqpus = 1
        drv.execute(kernel_code, uniforms=unif.addresses()[0], thread=nqpus)

        print(' in_a, in_b '.center(80, '='))
        print(in_a)
        print(in_b)
        print(' out_a, out_b '.center(80, '='))
        print(out_a)
        print(out_b)


if __name__ == '__main__':
    main()
