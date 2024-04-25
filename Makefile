version=0.1.18
local_registry=192.168.0.100:5555
docker_registry=192.168.0.100:5555
aliyun_registry_bestqa=registry.cn-shanghai.aliyuncs.com/bestqa
github_pkg_registry_surveyresearch=docker.pkg.github.com/swuecho/surveyresearch
PYPI=http://192.168.0.135:3141//root/pypi/+simple/
TRUSTED_HOST=192.168.0.135

static:
	rm -rf staticfiles
	mkdir staticfiles
	# cp -rf templates/components staticfiles/components
	python manage.py collectstatic --noinput
	cp -rf  ../ecomm-ui/dist/* staticfiles

tag:
	git tag release-v$(version)
	git push origin tag release-v$(version)

build:
	docker build --build-arg PYPI=$(PYPI)  --build-arg TRUSTED_HOST=$(TRUSTED_HOST) --build-arg docker_registry=192.168.0.100:5555  -t $(local_registry)/bestqa_django:$(version) -f Dockerfile .
push:
	docker push $(local_registry)/bestqa_django:$(version)
	docker tag  $(local_registry)/bestqa_django:$(version) $(aliyun_registry_bestqa)/bestqa_django:$(version)
	docker push $(aliyun_registry_bestqa)/bestqa_django:$(version)

init:
	python manage.py migrate
	# 对应 01_auth_init
	python manage.py runscript auth_init 
