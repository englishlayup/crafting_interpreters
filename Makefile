
build_test_image: docker/Dockerfile
	cd docker && docker build -t craftinginterpreters .


test:
	docker run \
		-u tester \
		-w /home/tester/craftinginterpreters \
		--rm \
		-v $(PWD):/home/tester/src craftinginterpreters \
		bash -c "dart tool/bin/test.dart chap09_control --interpreter /home/tester/src/bin/pylox" \
		| tee test_output.log
