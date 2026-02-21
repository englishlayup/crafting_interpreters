#include "vm.h"
#include "chunk.h"
#include "debug.h"
#include "value.h"
#include <stdint.h>
#include <stdio.h>

VM vm;

void initVM() {}

void freeVM() {}

InterpretResult run() {
#define READ_BYTE() (*vm.ip++)
#define READ_CONSTANT() (vm.chunk->constants.values[READ_BYTE()])
  for (;;) {
    uint8_t instruction = READ_BYTE();
#ifdef DEBUG_TRACE_EXECUTION
    disassembleInstruction(vm.chunk, (int)(vm.ip - vm.chunk->code));
#endif /* ifdef DEBUG_TRACE_EXECUTION */
    switch (instruction) {
    case OP_RETURN: {
      return INTERPRET_OK;
    }
    case OP_CONSTANT: {
      Value constant = READ_CONSTANT();
      printValue(constant);
      printf("\n");
      break;
    }
    }
  }
#undef READ_BYTE
#undef READ_CONSTANT
}

InterpretResult interpret(Chunk *chunk) {
  vm.chunk = chunk;
  vm.ip = chunk->code;
  return run();
}
