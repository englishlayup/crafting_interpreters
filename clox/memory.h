#ifndef clox_memory_h
#define clox_memory_h

#include "common.h"

#define GROW_CAPACITY(capacity) ((capacity) < 8 ? 8 : 2 * capacity)

#define GROW_ARRAY(type, pointer, oldCount, newCount)                          \
  (type *)reallocate(pointer, sizeof(type) * oldCount, sizeof(type) * newCount)

#define FREE_ARRAY(type, pointer, oldCount)                                    \
  (type *)reallocate(pointer, oldCount, 0)

void *reallocate(void *pointer, size_t oldSize, size_t newSize);

#endif // !clox_memory_h
