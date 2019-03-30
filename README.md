# Configuration Server

## background

When i going to find a way to provide configuration, there are lots and lots of solutions. But, they have different of limitations, especially in cloud native environments.

Idea comes from spring boot config server, but it's not suitable for non-spring system, so i write a new one,
for best fit my case.

## Target

What this project aims to , is to provide a **cloud native**, **version based**, **http based**, **CI/CD friendly** configuration project.

## Usage

```bash

# Run Instruction

docker run --rm -v $PWD/config_server:/config carwestsam/python-config-server

# Build Instruction

./bin/build.sh 

```

## TODO

version 0.1

- [x] file based configration server
- [x] packed in docker image
- [ ] automatically push to docker hub
- [ ] a brief introduction
