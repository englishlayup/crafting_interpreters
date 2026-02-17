#ifndef clox_chunk_h
#define clox_chunk_h

#include "common.h"
#include "value.h"
#include <stddef.h>

typedef enum {
  OP_CONSTANT,
  OP_RETURN,
} OpCode;

typedef struct {
  int line;
  int offset;
} LineStart;

typedef struct {
  int count;
  int capacity;
  uint8_t *code;
  ValueArray constants;
  int lineCount;
  int lineCapacity;
  LineStart *lines;
} Chunk;

void initChunk(Chunk *chunk);
void writeChunk(Chunk *chunk, uint8_t byte, int line);
void freeChunk(Chunk *chunk);
int addConstant(Chunk *chunk, Value value);
int getLine(const Chunk *chunk, int instruction);

#endif // !clox_chunk_h
