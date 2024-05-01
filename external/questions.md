# Why Django?

That's the first question comes to your mind before going into codebase. Why not Flask, FastAPI, or any other?

Reason is very intuitive. As you said in task requirements, rather than focusing on perfection, I focused on problem solving approach. With Flask, FastAPI, or any other, we have to worry about lot of bottlenecks, such as choosing an ORM, implementing database migration framework(e.g. alembic), worrying about security, and etc.

Django provides production-ready project structure. Some of the advantages of Django over other frameworks are the built-in ORM, migration tool supporting most of the SQL/NoSQL databases, and it also gives you very secure environment for you to not worry about SQL-injection, CSRF attacks, and other web-related cyber attacks.

# Guidance

**Q: How the code will be deployed?**

**A: There are lots of ways to deploy our application. These are the few ways to do that:**

- ***Containers.*** I already dockerized this application by creating Dockerfile and docker-compose file, so one way to deploy it, is using container orchestration tools like Kubernetes, Docker Swarm, or even platform like Google Kubernetes Engine (GKE) on GCP.
- ***PaaS.*** There are PaaS solutions out there to offer easy deployments that fits most of the frameworks, such as: Heroku, GCP App Engine, AWS Elastic Beanstalk.
- ***Serverless Functions.*** Services like AWS Lambda, Google Cloud Functions allow us to deploy our application without managing servers directly.
- ***MicroVMs.*** These are lightweight virtualization units designed to provide isolation and security for running individual workloads or applications. Unlike traditional virtual machines (VMs) that emulate full hardware, MicroVMs are optimized for specific tasks and have minimal overhead. These are the some services that provide practical microvm deployment structure: firecracker, fly.io, and etc.

Tools and technologies I mentioned above are the way to host our application. If we want to host our application in standart VPS(Virtual Private Server) As we come to deployment, we should use `gunicorn` or `uvicorn` as our WSGI/ASGI HTTP server to serve it to users if we use standart VPS(AWS EC2 or GCP Compute Engine)

---

**Q: How the code will be scalable?**

**A:** When more and more users/developers will send request to our simple endpoints deployed on let's say GCP Compute Engine, there will be bottlenecks because of overloading of server. There are few ways to overcome this problem and scale our application:

- Using message brokers like RabbitMQ/Redis with Celery(asynchronous task queue).
	- Celery workers can run in parallel, processing multiple tasks simultaneously. This parallelism allows our server to handle more requests concurrently.
	- When our application experiences high traffic, distributing tasks across multiple workers helps balance the load.
- We can also implement monitoring software like Prometheus/Grafana to track application performance and identify areas for improvement.
- Horizontal Scaling. Deploying our django application across multiple servers and distribute incoming traffic using a load balancer(e.g. Ngnix, AWS Elastic Load Balancer, and etc.)
- Microservices Architecture(I mentioned below).

---

**Q: What is the approach you have taken?**

**A:** My approach is monolithic to this task, due to simplicity of it. Let's say we have to scale our application, we can use microservices architecture, where we can separate our application into multiple services, such as: filtering character quotes, finding specific quotes from movies, and etc. This way, we can split our application into multiple services, and deploy them separately, which will make our application more scalable. Creating movie, character, and book application separately will help us to scale application more as microservices.

If we come to the project architecture, as this is Django project, it follows MVT (Model-View-Template) pattern. I have created a single app called `character` which contains all the models, views, and serializers.

---

**Q: How would you explain the code to another developer?**

**A:** In my opinion everything is self-explanatory. As a developer I used best-practices to write application, such as: naming conventions, docstrings, comments, RESTful principles, and etc.

But if I have to explain it to another developer(technically), I would say:

- `character` app contains all the models, views, and serializers.
- `character/utils` We just need to call some functions only when we need, not everytime when we call our endpoint. So this folder contains utility functions, such as: `get_character_by_id` to not repeat the code on multiple places.
- `lotr_rest_api` project contains configuration files, such as: settings, swagger urls, and etc.
- `.env.example` contains environment variables, which should be copied to `.env` file.

---

**Q: How have you documented the code?**

**A:** I documented the API using three ways:
- Docstrings. I used docstrings to document the functions, classes, and modules.
- Swagger. I used drf-yasg to generate swagger documentation for the API.
- Redoc. I used redoc to render the swagger documentation in a more user-friendly way.
- API Flowchart. I created a flowchart using draw.io to show the API flow.