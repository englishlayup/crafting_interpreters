load("@rules_cc//cc:cc_binary.bzl", "cc_binary")
load("@rules_cc//cc:cc_library.bzl", "cc_library")

cc_library(
    name = "common",
    hdrs = [
        "common.h",
    ],
)

cc_library(
    name = "chunk",
    srcs = ["chunk.c"],
    hdrs = ["chunk.h"],
    deps = [
        ":common",
        ":memory",
        ":value",
    ],
)

cc_library(
    name = "memory",
    srcs = ["memory.c"],
    hdrs = ["memory.h"],
    deps = [":common"],
)

cc_library(
    name = "debug",
    srcs = ["debug.c"],
    hdrs = ["debug.h"],
    deps = [
        ":chunk",
        ":common",
    ],
)

cc_library(
    name = "value",
    srcs = ["value.c"],
    hdrs = ["value.h"],
    deps = [
        ":common",
        ":memory",
    ],
)

cc_binary(
    name = "clox",
    srcs = glob(["*.c"]),
    copts = [
        "-Wall",
        "-O0",
        "-g",
    ],
    deps = [
        ":chunk",
        ":debug",
        ":memory",
        ":value",
    ],
)
