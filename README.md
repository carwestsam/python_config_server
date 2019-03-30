# Configuration Server

## background

When i going to find a way to provide configuration, there are lots and lots of solutions. But, they have different of limitations, especially in cloud native environments.

Idea comes from spring boot config server, but it's not suitable for non-spring system, so i write a new one,
for best fit my case.

## Target

What this project aims to , is to provide a **cloud native**, **version based**, **http based**, **CI/CD friendly** configuration project.


## Attention!!!

This project is not well documented, and developing in progess, treat it as an example. don't use it.

## Usage

```bash

# Run Instruction

docker run --rm -v $PWD/sample_config:/config -p 8088:80 carwestsam/python-config-server

# get specific version of configuration

curl localhost:8088/config/account-service/20181002/development
# result should be
# {"version":"20181002","config":{"name":"account_service_app_old"}}

# or you can just curl the latest version which has development configuration
curl localhost:8088/config/account-service/latest/development
# result should be
# {"version":"20190329","config":{"name":"account_service_app"}}

```

development

```bash
# Build Instruction

./bin/build.sh 

```

## explain 

file tree organized as

```
.
|____account-service        # 2. name of service, it could have multiple services
| |____20181002             # 3. version of configuration file, sorted as string dict, not restrict to number
| | |____development.json   # 4. ${env_name}.json,  
| |____20190329
| | |____development.json
|____config.json            # 1. config file for config server
```

## TODO

**version 0.2 - TODO**

- [ ] support git as backend
- [ ] support aws s3 as backend
- [ ] better version tracking
 
**version 0.1 - DONE**

- [x] file based configration server
- [x] packed in docker image
- [x] automatically push to docker hub
- [x] a brief introduction
