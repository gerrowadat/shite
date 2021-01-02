#!/usr/bin/python3

class Machine(object):
  def __init__(self):
    # memory, registers, stack
    self._m = {}
    self._r = [0,0,0,0,0,0,0,0]
    self._s = []
    # Executing Program
    self._prog = []
    # Instruction pointer
    self._ptr = 0
    # Terminal output
    self._output = ''

  @property
  def output(self):
    return self._output

  def _next(self):
    # return dereferenced next value, incrementing pointer
    self._ptr += 1
    return self._Value(self._m[self._ptr])

  def _next_reg(self):
    # Return register denoted by next value (assuming it is one).
    self._ptr += 1
    return self._m[self._ptr] % 32768

  def _jump(self, loc):
    # actually set pointer to previous position, as we increment before reading.
    self._ptr = loc - 1

  def _Value(self, val):
    # Returns either the value, or the register.
    if val < 32768:
      return val
    if val > 32775:
      raise ValueError('Invalid value %d' % (val, ))
    return self._r[val % 32768]

  def Execute(self, program):
    self._prog = program
    # Load Program into memory
    for i in range(0, len(program)):
      self._m[i] = program[i]
    self._ptr = 0
    instr = self._m[self._ptr]
    while instr != 0:
      method = getattr(self, 'op_%d' % (instr), None)
      if method is None:
        print('[%d] Encountered unknown instruction %d' % (self._ptr, instr))
        return
      ret = method()
      if ret == False:
        return
      self._ptr += 1
      instr = self._m[self._ptr]

  def op_1(self):
    # set: 1 a b : Set reg a to value of b
    a = self._next_reg()
    b = self._next()
    print('[%d] SET a(reg %d) b(%d: %d)' % (self._ptr - 2, a, self._m[self._ptr], b))
    self._r[a] = b

  def op_2(self):
    # push: 2 a: push a onto stack
    a = self._next()
    print('[%d] PUSH %d' % (self._ptr - 1, a))
    self._s.append(a)
    print(' - Stack: %s' % (self._s))

  def op_3(self):
    # pop: 3, a:  remove the top element from the stack and write it into <a>; empty stack = error
    a = self._next_reg()
    elem = self._s.pop()
    print('[%d] POP %d -> reg:%d' % (self._ptr - 1, elem, a))
    self._r[a] = elem
    print(' - Stack: %s' % (self._s))
 
  def op_4(self):
    # eq: 4 a b c: set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
    a = self._next_reg()
    b = self._next()
    c = self._next()
    print('[%d] EQ a(reg %d) b(%d) c(%d)' % (self._ptr - 3, a, b, c))
    if b == c:
      self._r[a] = 1
    else:
      self._r[a] = 0

  def op_5(self):
    # gt: 5 a b c: set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
    a = self._next_reg()
    b = self._next()
    c = self._next()
    print('[%d] GT %d %d -> reg:%d' % (self._ptr - 3, b, c, a))
    if b > c:
      self._r[a] = 1
    else:
      self._r[a] = 0

  def op_6(self):
    loc = self._next()
    print('[%d] JMP %d' % (self._ptr, loc))
    self._jump(loc)

  def op_7(self):
    # jt: 7 a b : If a is nonzero jump to b
    a = self._next()
    b = self._next()
    print('[%d] JT a(%d: %d) b(%d: %d)' % (self._ptr - 2, self._m[self._ptr-1], a, self._m[self._ptr], b))
    if a != 0:
      self._jump(b)

  def op_8(self):
    # jf: 7 a b : If a is zero jump to b
    a = self._next()
    b = self._next()
    print('[%d] JF a(%d: %d) b(%d: %d)' % (self._ptr - 2, self._m[self._ptr-1], a, self._m[self._ptr], b))
    if a == 0:
      self._jump(b)

  def op_9(self):
    # add: 9 a b c : assign into <a> the sum of <b> and <c> (modulo 32768)
    a = self._next_reg()
    b = self._next()
    c = self._next()
    result = (b + c) % 32768
    print('[%d] ADD a(reg %d) b(%d), c(%d) [%d]' % (self._ptr - 3, a, b, c, result))
    self._r[a] = result

  def op_10(self):
    # mult: 10 a b c: store into <a> the product of <b> and <c> (modulo 32768)
    a = self._next_reg()
    b = self._next()
    c = self._next()
    result = (b * c) % 32768
    print('[%d] MULT a(reg %d) b(%d), c(%d) [%d]' % (self._ptr - 3, a, b, c, result))
    self._r[a] = result

  def op_11(self):
    # mod: 11 a b c: store into <a> the remainder of <b> divided by <c>
    a = self._next_reg()
    b = self._next()
    c = self._next()
    result = b % c
    print('[%d] MOD a(reg %d) b(%d), c(%d) [%d]' % (self._ptr - 3, a, b, c, result))
    self._r[a] = result

  def op_12(self):
    # and: 12 a b c: stores into <a> the bitwise and of <b> and <c>
    a = self._next_reg()
    b = self._next()
    c = self._next()
    result = (b & c) % 32768
    print('[%d] AND %d %d (%d) -> reg:%d' % (self._ptr - 3, b, c, result, a))
    self._r[a] = result

  def op_13(self):
    # or: 13 a b c: stores into <a> the bitwise or of <b> and <c>
    a = self._next_reg()
    b = self._next()
    c = self._next()
    result = (b | c) % 32768
    print('[%d] OR %d %d (%d) -> reg:%d' % (self._ptr - 3, b, c, result, a))
    self._r[a] = result

  def op_14(self):
    # not: 14 a b: stores 15-bit bitwise inverse of <b> in <a>
    a = self._next_reg()
    b = self._next()
    result = ~ b

    # wrap around below 0
    if result < 0:
      result = 32768 + result

    result = result % 32768

    print('[%d] NOT %d (%d) -> reg:%d' % (self._ptr - 2, b, result, a))
    self._r[a] = result

  def op_15(self):
    # rmem: 15 a b: read memory at address <b> and write it to <a>
    a = self._next_reg()
    b = self._next()
    print('[%d] RMEM %d (%d) -> reg:%d' % (self._ptr - 2, b, self._m[b], a))
    self._r[a] = self._m[b]

  def op_16(self):
    # wmem: 16 a b:  write the value from <b> into memory at address <a>
    a = self._next()
    b = self._next()
    if b not in self._m:
      self._m[b] = 0
    print('[%d] WMEM %d (%d) -> mem:%d' % (self._ptr - 2, b, self._m[b], a))
    self._m[a] = b

  def op_17(self):
    # call: 17 a : write the address of the next instruction to the stack and jump to <a>
    a = self._next()
    print('[%d] CALL %d (next: %d)' % (self._ptr - 1, a, self._ptr + 1))
    self._s.append(self._ptr + 1)
    self._jump(a)

  def op_18(self):
    # ret: 18 : pop stack and jump to it, halt on empty stack.
    if len(self._s) == 0:
      print ('[%d] RET (empty stack)' % (self._ptr))
      return False
    elem = self._s.pop()
    print('[%d] RET %d' % (self._ptr, elem))
    self._jump(elem)

  def op_19(self):
    self._ptr += 1
    output = chr(self._Value(self._m[self._ptr]))
    self._output = self._output + str(output)
    print('[%d] OUT %s' % (self._ptr, str(output)))
    
  def op_21(self):
    print('[%d] NOOP' % (self._ptr))




def main():
  raw = []
  with open('challenge.bin', 'rb') as f:
    byte = f.read(1)
    while byte:
      raw.append(byte)
      byte = f.read(1)

  print ('Read %d bytes' % (len(raw)))

  program = []
  for i in range(0, len(raw)-1, 2):
    program.append(int.from_bytes(raw[i] + raw[i+1], byteorder='little', signed=False))

  print ('Instructions: %d' % (len(program)))

  m = Machine()

  m.Execute(program)

  print('Program Output: %s' % (m.output))
  
main()
