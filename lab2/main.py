from kubernetes import client, config


def create_deployment(api_instance):
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(
            name="deployment",
            labels={"app": "lab2-web-app"}
        ),
        spec=client.V1DeploymentSpec(
            replicas=2,
            selector=client.V1LabelSelector(
                match_labels={"app": "lab2-web-app"}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={"app": "lab2-web-app"}
                ),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="http",
                            image="ifilyaninitmo/itdt-contained-frontend:master",
                            ports=[client.V1ContainerPort(container_port=3000)],
                            env=[
                                client.V1EnvVar(name="REACT_APP_USERNAME", value="progML"),
                                client.V1EnvVar(name="REACT_APP_COMPANY_NAME", value="Lab2")
                            ]
                        )
                    ]
                )
            )
        )
    )

    api_instance.create_namespaced_deployment(
        namespace="default",
        body=deployment
    )
    print("Deployment created.")


def create_service(api_instance):
    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name="lab2-service"
        ),
        spec=client.V1ServiceSpec(
            selector={"app": "lab2-web-app"},
            type="LoadBalancer",
            ports=[
                client.V1ServicePort(protocol="TCP", port=3000, target_port="http")
            ]
        )
    )

    api_instance.create_namespaced_service(
        namespace="default",
        body=service
    )
    print("Service created.")


def main():
    config.load_kube_config()
    api_instance = client.AppsV1Api()
    api = client.CoreV1Api()

    create_deployment(api_instance)
    create_service(api)


if __name__ == "__main__":
    main()
