
build_test_image: docker/Dockerfile
	cd docker && docker build -t craftinginterpreters .


test:
	docker run \
		-u tester \
		-w /home/tester/craftinginterpreters \
		--rm \
		-v $(PWD):/home/tester/src craftinginterpreters \
		bash -c "dart tool/bin/test.dart chap10_functions --interpreter /home/tester/src/bin/pylox" \
		| tee test_output.log

generate_ast:
	python3 ./pylox/tool/generate_ast.py ./pylox/pylox/
