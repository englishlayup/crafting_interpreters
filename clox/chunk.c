#include "chunk.h"
#include "memory.h"
#include <stddef.h>
#include <stdlib.h>

void initChunk(Chunk *chunk) {
  chunk->capacity = 0;
  chunk->count = 0;
  chunk->code = NULL;
  chunk->lineCapacity = 0;
  chunk->lineCount = 0;
  chunk->lines = NULL;
  initValueArray(&chunk->constants);
}

void writeChunk(Chunk *chunk, uint8_t byte, int line) {
  if (chunk->capacity < chunk->count + 1) {
    int oldCapacity = chunk->capacity;
    chunk->capacity = GROW_CAPACITY(oldCapacity);
    chunk->code =
        GROW_ARRAY(uint8_t, chunk->code, oldCapacity, chunk->capacity);
  }
  chunk->code[chunk->count] = byte;
  chunk->count++;

  if (chunk->lineCount > 0 && chunk->lines[chunk->lineCount - 1].line == line) {
    return;
  }

  if (chunk->lineCapacity < chunk->lineCount + 1) {
    int oldCapacity = chunk->lineCapacity;
    chunk->lineCapacity = GROW_CAPACITY(oldCapacity);
    chunk->lines =
        GROW_ARRAY(LineStart, chunk->lines, oldCapacity, chunk->lineCapacity);
  }

  LineStart *lineStart = &chunk->lines[chunk->lineCount++];
  lineStart->line = line;
  lineStart->offset = chunk->count - 1;
}

int getLine(const Chunk *chunk, int instruction) {
  int start = 0;
  int end = chunk->lineCount - 1;

  for (;;) {
    int mid = (end + start) / 2;
    LineStart *line = &chunk->lines[mid];
    if (instruction < line->offset) {
      end = mid - 1;
    } else if (line->offset == chunk->lines[chunk->lineCount - 1].offset ||
               instruction < chunk->lines[mid + 1].offset) {
      return line->line;
    } else {
      start = mid + 1;
    }
  }
}

int addConstant(Chunk *chunk, Value value) {
  writeValueArray(&chunk->constants, value);
  return chunk->constants.count - 1;
}

void freeChunk(Chunk *chunk) {
  FREE_ARRAY(uint8_t, chunk->code, chunk->capacity);
  FREE_ARRAY(uint8_t, chunk->lines, chunk->lineCapacity);
  freeValueArray(&chunk->constants);
  initChunk(chunk);
}
