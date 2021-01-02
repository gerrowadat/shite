#!/usr/bin/python3

class Machine(object):
  def __init__(self):
    # memory, registers, stack
    self._m = []
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

  def _Value(self, val):
    # Returns either the value, or the register.
    if val < 32768:
      return val
    if val > 32775:
      raise ValueError('Invalid value %d' % (val, ))
    return self._r[val % 32768]


  def Execute(self, program):
    self._prog = program
    self._ptr = 0
    instr = self._prog[self._ptr]
    while instr != 0:
      method = getattr(self, 'op_%d' % (instr), None)
      if method is None:
        print('[%d] Encountered unknown instruction %d' % (self._ptr, instr))
        return
      method()
      self._ptr += 1
      instr = program[self._ptr]
    print('[%d] 0 HALT')

  def op_19(self):
    self._ptr += 1
    output = chr(self._Value(self._prog[self._ptr]))
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
