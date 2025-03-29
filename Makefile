
build_test_image: docker/Dockerfile
	cd docker && docker build -t craftinginterpreters .


test:
	docker run \
		-u tester \
		-w /home/tester/craftinginterpreters \
		--rm \
		-v $(PWD):/home/tester/src craftinginterpreters \
		bash -c "dart tool/bin/test.dart chap13_inheritance --interpreter /home/tester/src/bin/pylox" \
		| tee test_output.log

generate_ast.pylox:
	python3 ./pylox/tool/generate_ast.py ./pylox/pylox/

generate_ast.golox:
	python3 ./golox/script/generate_ast.py ./golox
	go fmt ./golox/internal/expr/expr.go
	go fmt ./golox/internal/stmt/stmt.go
