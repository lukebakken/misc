.PHONY: build run-java

RMQ_HOST ?= localhost
export RMQ_HOST

build:
	mvn compile

run-java: build
	mvn exec:java '-Dexec.mainClass=io.bakken.basic_publish.App'
