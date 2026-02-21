#include "chunk.h"
#include "munit.h"
#include "string.h"

MunitResult test_rle_line(const MunitParameter params[], void *fixture) {
  Chunk chunk;
  initChunk(&chunk);
  int constant = addConstant(&chunk, 1.2);
  writeChunk(&chunk, OP_CONSTANT, 123);
  writeChunk(&chunk, constant, 123);
  writeChunk(&chunk, OP_RETURN, 123);
  munit_assert_int(chunk.lineCount, ==, 1);
  munit_assert_int(chunk.count, ==, 3);
  writeChunk(&chunk, OP_RETURN, 1);
  writeChunk(&chunk, OP_RETURN, 1);
  writeChunk(&chunk, OP_RETURN, 1);
  writeChunk(&chunk, OP_RETURN, 1);
  munit_assert_int(chunk.lineCount, ==, 2);
  munit_assert_int(chunk.count, ==, 7);
  return MUNIT_OK;
}

MunitTest tests[] = {
    {
        "/test run length encoding",
        test_rle_line,
        NULL,
        NULL,
        MUNIT_TEST_OPTION_NONE,
        NULL,
    },
    {NULL, NULL, NULL, NULL, MUNIT_TEST_OPTION_NONE, NULL},
};

const MunitSuite suite = {
    "/chunk-tests", tests, NULL, 1, MUNIT_SUITE_OPTION_NONE,
};

int main(int argc, char *argv[]) {
  return munit_suite_main(&suite, NULL, argc, argv);
}
