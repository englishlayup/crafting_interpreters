.PHONY: all stage test

all:
	mkdir -p build
	cmake build -G Ninja
	cmake --build build/

stage: all
	cp ./build/clox ../bin/

test:
	dart ~/personal/craftinginterpreter_book/tool/bin/test.dart clox --interpreter ./build/clox \
	| tee test_output.log
