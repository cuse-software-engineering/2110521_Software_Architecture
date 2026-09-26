# Introduction to Microservice Architecture

**Wiwat Vatanawood, Duangdao Wichadakul, Nuengwong Tuaycharoen, Pittipol Kantavat**
Ref: Chris Richardson, *Microservices Patterns: With examples in Java*, Manning, 2019 — https://microservices.io/

> Transcribed from `Intro_to_Microservice_Patterns-360766-17550117624043.pdf` (60 slides). Page images are in [png/](png/).

---

## Slide 2 — References

![Slide 2](png/page-02.png)

Cover of the Manning book *Microservices Patterns* by Chris Richardson.

- Book
  - Chris Richardson, Microservices Patterns: With examples in Java, Manning, 2019
- Website
  - https://microservices.io/

## Slide 3 — The Chapter covers

- The symptoms of monolithic hell and how to escape it by adopting the microservice architecture
- The essential characteristics of the microservice architecture and its benefits and drawbacks
- How microservices enable the DevOps style of development of large, complex applications
- The microservice architecture pattern language and why you should use it

---

# Part 1 — A brief refresher on software architecture

## Slide 4 — Agenda

- **A brief refresher on software architecture** (current section)
- From monolith to microservices
- Microservices != silver bullet
- Applying the microservice pattern language

## Slide 5 — What is software architecture?

> "The software architecture of a computing system is the set of structures needed to reason about the system, which comprise software **elements**, **relations** among them, and **properties** of both."

*Documenting Software Architectures, Bass et. al.*

## Slide 6 — What is software architecture?

Architecture is multi-dimensional

e.g. Structural, electrical, plumbing, mechanical

⇒

Described by multiple views

View = (elements, relations, properties)

## Slide 7 — Why architecture matters?

- Enables an application to satisfy the second category of requirements: its quality-of-service requirements
- Non-functional requirements
- Also known as quality attributes and are the so-called –ilities

## Slide 8 — Development velocity

![Slide 8](png/page-08.png)

- Maintainability
- Testability
- Deployability
- Evolvability
- Scalability
- Security
- Reliability
- …

A red box groups the first three -ilities (Maintainability, Testability, Deployability), with an arrow from a yellow **Development velocity** callout pointing at them.

*https://en.wikipedia.org/wiki/Non-functional_requirement*

## Slide 9 — Businesses must innovate faster

Businesses must innovate faster

⇒

Build better software faster

- **Reducing** lead time
- **Increasing** deployment frequency

## Slide 10 — Modern software development: moving fast and *not* breaking things!

![Slide 10](png/page-10.png)

Table 2 ("2017 IT performance by cluster") from the *2017 State of DevOps Report*, presented by Puppet + DORA, with the high-performer multipliers annotated in red:

| Survey question | High IT performers | Medium IT performers | Low IT performers |
|---|---|---|---|
| **Deployment frequency** — how often does your organization deploy code? | On demand (multiple deploys per day) — **46x** | Between once per week and once per month | Between once per week and once per month* |
| **Lead time for changes** — how long does it take to go from code commit to code successfully running in production? | Less than one hour — **440x** (Netflix: 16 minutes) | Between one week and one month | Between one week and one month* |
| **Mean time to recover (MTTR)** — how long does it generally take to restore service when a service incident occurs? | Less than one hour — **24x** | Less than one day | Between one day and one week |
| **Change failure rate** — what percentage of changes results in degraded service or requires remediation? | 0–15% — **5x lower** (Amazon: ~0.001%) | 0–15% | 31–45% |

## Slide 11 — Modern software development

![Slide 11](png/page-11.png)

Triangle diagram with one concern at each vertex:

- **Process:** DevOps/Continuous delivery/deployment
- **Organization:** Small, autonomous teams
- **Architecture:** ??

---

# Part 2 — From monolith to microservices

## Slide 12 — Agenda

- A brief refresher on software architecture
- **From monolith to microservices** (current section)
- Microservices != silver bullet
- Applying the microservice pattern language

## Slide 13 — The monolithic architecture

![Slide 13](png/page-13.png)

> The monolithic architecture is an **architectural style** that structures the **application** as a **single executable component**

A green **Implementation View** box points up at the definition.

## Slide 14 — Traditional: Monolithic architecture

![Slide 14](png/page-14.png)

Diagram of the FTGO application as a single hexagon. Courier and Consumer (mobile applications) invoke the **REST API**; the Restaurant (browser) uses the **Web UI**. Inside the application are the Restaurant management, Order management, Delivery management, Payments, Notification and Billing modules. Adapters (Twilio adapter, Amazon SES adapter, Stripe adapter, MySQL adapter) invoke the cloud services (Twilio messaging service, AWS SES email service, Stripe payment service) and the MySQL database. Two callouts: **Logical View** (pointing at the inner modules) and **Implementation View** (pointing at the hexagon as a whole).

## Slide 15 — -ilities of *small* monoliths

![Slide 15](png/page-15.png)

- Maintainability
- Testability
- Deployability
- …

Illustrated with a happy, dancing cat.

## Slide 16 — But successful applications keep growing ....

![Slide 16](png/page-16.png)

One **Development Team** box beside a tall **Application** box.

## Slide 17 — … and growing ....

![Slide 17](png/page-17.png)

**Development Team A**, **Development Team B** and **Development Team C** beside an even taller **Application** box.

## Slide 18 — Eventually: monolithic hell

![Slide 18](png/page-18.png)

Photo of a person climbing the enormous stone blocks of a pyramid.

Eventually: agile development and deployment becomes impossible = monolithic hell

## Slide 19 — -ilities of *large* monoliths

![Slide 19](png/page-19.png)

- Maintainability
- Testability
- Deployability
- …

Illustrated with a crying cat.

## Slide 20 — The slow march toward monolithic hell

![Slide 20](png/page-20.png)

Diagram: FTGO development (Order management team, Restaurant management team, Delivery management team) all commit to a single **Source code repository**, which feeds one **Deployment pipeline** (Jenkins CI → Backlog → Manual testing) that deploys the **FTGO application** to Production. Callouts:

- Large development organization
- Single code base creates communication and coordination overhead.
- The path from code commit to production is arduous. Changes sit in a queue until they can be manually tested.
- Large, complex unreliable, difficult to maintain

## Slide 21 — Living in monolithic hell (1)

- Complexity intimidates developers
  - Fixing bugs and correctly implementing new features become difficult and time consuming
  - Deadline are missed
- Development is slow
  - The large application overload and slow down developer's IDE
  - The application takes a long time to start up

## Slide 22 — Living in monolithic hell (2)

- Path from commit to deployment is long and arduous
  - The build is frequently in an unreleasable state
  - Painful merges
- Scaling is difficult
  - Data consume a lot of memory
  - CPU is intensively used

## Slide 23 — Living in monolithic hell (3)

- Delivering a reliable monolith is challenging
  - There are frequent production outages
  - Due to lack of testability
- Locked into increasing obsolete technology stack
  - Difficult to adopt new frameworks and languages
  - Difficult to upgrade version for each components

## Slide 24 — The microservice architecture

> The microservice architecture is an **architectural style** that **structures** an application as a **set of loosely coupled, services** organized around **business capabilities**

## Slide 25 — Scale cube and microservices

![Slide 25](png/page-25.png)

The scale cube: the X-axis runs from *One instance* to *Many instances*, the Y-axis from *Monolith* to *Microservices*, and the Z-axis from *One partition* to *Many partitions*.

- **X-axis scaling**, a.k.a. horizontal duplication — Scale by cloning.
- **Y-axis scaling**, a.k.a. functional decomposition — Scale by splitting things that are different, such as by function.
- **Z-axis scaling**, a.k.a. data partitioning — Scale by splitting similar things, such as by customer ID.

## Slide 26 — X-axis :- scaling load balances requests across multiple instances (1)

![Slide 26](png/page-26.png)

- X-axis scaling is a common way to scale a monolithic application
- Running multiple instances of the application behind a **load balancer**
- The load balancer distributes requests among the N identical instances of the application

Callout: X-axis scaling, a.k.a. horizontal duplication. Scale by cloning.

## Slide 27 — X-axis :- scaling load balances requests across multiple instances (2)

![Slide 27](png/page-27.png)

Diagram: a **Client** sends a Request to a **Load balancer**, which routes requests using a load balancing algorithm to *N identical application instances* (Application instance 1, 2, 3).

- X-axis is great way of improving the capacity and availability of an application.

## Slide 28 — Z-axis :- scaling routes requests based on an attribute of the request (1)

![Slide 28](png/page-28.png)

- Also runs multiple instances of the monolith application
- But each instance is responsible for only a subset of the data
- The router in front of the instances uses a request attribute to route it to the appropriate instance
- for example, route requests using *userId*.

Callout: Z-axis scaling, a.k.a. data partitioning. Scale by splitting similar things, such as by customer ID.

## Slide 29 — Z-axis :- scaling routes requests based on an attribute of the request (2)

![Slide 29](png/page-29.png)

Diagram: a **Client** sends `GET /...` with `Authorization: userId:password` to a **Router**, which uses the userId to decide where to route requests among *N identical application instances*: Application instance 1 (Users: a–h), instance 2 (Users: i–p), instance 3 (Users: r–z). Each instance is responsible for a subset of the users.

- Z-axis scaling is a great way to scale an application to handle increasing transaction and data volumes.

## Slide 30 — Y-axis :- scaling functionally decomposes an application into services (1)

![Slide 30](png/page-30.png)

- Y-axis scaling, or **functional decomposition**, solves the problem of increasing development and application complexity.
- Splitting a monolithic application into a set of **services**
  - for examples, order management, customer management, and so on

Callout: Y-axis scaling, a.k.a. functional decomposition. Scale by splitting things that are different, such as by function.

## Slide 31 — Y-axis :- scaling functionally decomposes an application into services (2)

![Slide 31](png/page-31.png)

Diagram: a **Client** sends Order requests, Customer requests and Review requests to the Application, which Y-axis scaling decomposes into an **Order Service**, **Customer Service** and **Review Service**. The Order Service is itself scaled behind a **Load balancer** into Order Service instance 1, 2 and 3 — each service is typically scaled using X-axis and possibly Z-axis scaling.

- A service can be scaled using X-axis scaling and, possibly, Z-axis scaling.

## Slide 32 — Service = independently deployable component

![Slide 32](png/page-32.png)

Diagram of a service drawn as a hexagon, split into a **Consumer facing** half and an **Implementation** half:

- Consumer facing: a **Command / Query API** (Synchronous: REST, gRPC, …; Asynchronous: Command/Reply, Notification), an **Event Publisher** that emits Events, and an **SLA** sticky note.
- Implementation: an **API Client** (Synchronous: REST, gRPC, …; Asynchronous: Command/Reply, Notification), an **Event Subscriber** that consumes Events, and a **Service database** holding data owned by the service and data replicated from elsewhere.

## Slide 33 — Solution: microservice architecture

![Slide 33](png/page-33.png)

The FTGO application as microservices. Courier and Consumer mobile applications call REST APIs through an **API Gateway** ("The API Gateway routes requests from the mobile applications to services."); the Restaurant uses the **Restaurant Web UI**. Each service exposes its own REST API and owns a private database: **Order Service**, **Restaurant Service**, **Kitchen Service**, **Delivery Service**, **Accounting Service** (with a Stripe Adapter) and **Notification Service** (with Twilio and Amazon SES Adapters). Callouts: "Services corresponding to business capabilities / domain-driven design (DDD) subdomains", "Services have APIs.", "A service's data is private."

## Slide 34 — -ilities of *microservice architecture*

![Slide 34](png/page-34.png)

- Maintainability
- Testability
- Deployability
- …

Illustrated with the happy, dancing cat again.

## Slide 35 — Modern software development (completed)

![Slide 35](png/page-35.png)

The triangle from Slide 11 with the architecture vertex filled in; each vertex **Enables** the others:

- **Process:** DevOps/Continuous delivery/deployment
- **Organization:** Small, autonomous teams
- **Architecture:** Microservice architecture

Callouts: "Services improve testability and deployability" (architecture enables process) and "Teams own services" (architecture enables organization).

## Slide 36 — Microservices ⇒ Evolve the technology stack

- Pick a new technology when
  - Writing a new service
  - Make major changes to an existing service
- Let you experiment and fail safely

---

# Part 3 — Microservices != silver bullet

## Slide 37 — Agenda

- A brief refresher on software architecture
- From monolith to microservices
- **Microservices != silver bullet** (current section)
- Applying the microservice pattern language

## Slide 38 — No silver bullet

![Slide 38](png/page-38.png)

Photo of Fred Brooks speaking, beside the header of his paper:

> **No Silver Bullet — Essence and Accident in Software Engineering**
> Frederick P. Brooks, Jr., University of North Carolina at Chapel Hill
>
> *There is no single development, in either technology or management technique, which by itself promises even one order-of-magnitude improvement within a decade in productivity, in reliability, in simplicity.*

*https://en.wikipedia.org/wiki/Fred_Brooks*

## Slide 39 — Benefits of the microservice architecture (1)

- It enables the continuous delivery and deployment of large, complex applications
  - continuous delivery/deployment is part of DevOps (a set of practices for the rapid, frequent, and reliable delivery of software)
  - 3 ways that the microservice architecture enables CD
    - It has the **testability** required by continuous delivery/deployment
    - It has the **deployability** required by continuous delivery/deployment
    - It enables development teams to be **autonomous** and **loosely coupled**

## Slide 40 — Benefits of the microservice architecture (2)

- Services are small and easily maintained
  - The code is easier for a developer to understand
  - The small code base doesn't slow down the IDE, making developers more productive
  - Each service typically starts a lot faster than a large monolith does

## Slide 41 — Deployment pipeline per service

![Slide 41](png/page-41.png)

Diagram: in FTGO development, the Order management team, Restaurant management team and Delivery management team each own a service. Each service has its own source code repository (Order Service / Restaurant Service / Delivery Service source code repository) and its own automated **Deployment pipeline** (Jenkins CI), deploying the **Order Service**, **Restaurant Service** and **Delivery Service** independently to Production. Callouts: "Small, autonomous, loosely coupled teams", "Each service has its own source code repository.", "Each service has its own automated deployment pipeline.", "Small, simple, reliable, easy to maintain services".

## Slide 42 — Benefits of the microservice architecture (3)

- Services are independently deployable
  - Each service in a microservice architecture can be scaled independently
  - CPU-intensive vs. memory-intensive no need to be deployed together
- It enables teams to be autonomous
- It has better fault isolation
- It allows easy experimenting and adoption of new technologies

## Slide 43 — Drawback of the microservice architecture (1)

- Finding the right set of services is challenging
  - If you decompose a system incorrectly, you'll build a distributed monolith
  - It has the drawbacks of both the monolithic and the microservice architecture.

## Slide 44 — Drawback of the microservice architecture (2)

- Distributed systems are complex
  - Makes development, testing, and deployment difficult
  - Requires the use of unfamiliar techniques
    - Must use *sagas* to maintain data consistency across services
    - Must implement queries using either **API composition** or **CQRS views**

## Slide 45 — Drawback of the microservice architecture (3)

- Deploying features that span multiple services requires careful coordination
  - Need to create a rollout plan that orders service deployments based on the dependencies between services

## Slide 46 — Drawback of the microservice architecture (4)

- Deciding when to adopt the microservice architecture is difficult
  - A startup should begin with a monolithic application
  - When the problem is how to handle complexity → It makes sense to decompose the application into microservices

---

# Part 4 — Applying the microservice pattern language

## Slide 47 — Agenda

- A brief refresher on software architecture
- From monolith to microservices
- Microservices != silver bullet
- **Applying the microservice pattern language** (current section)

## Slide 48 — Patterns and Pattern Language

- A pattern is a reusable solution to a problem that occurs in a particular context.
- The **pattern language** guides you when developing an architecture.
- What architectural decisions you must make for each decision:
  - Available options
  - Trade-offs of each option

## Slide 49 — A high-level view of the Microservice architecture pattern language

![Slide 49](png/page-49.png)

Map of the pattern language. On the left, the **Application architecture** choice (Monolithic architecture ↔ Microservice architecture) leads into the **Microservice patterns**, arranged in three layers:

- **Application patterns:** Decomposition; Database architecture (Querying, Maintaining data consistency); Testing
- **Application infrastructure patterns:** Cross-cutting concerns; Security; Transactional messaging; Communication style; Reliability; Observability
- **Infrastructure patterns:** Deployment; Discovery; External API

Transactional messaging, Communication style, Reliability, Discovery and External API together form the **Communication patterns** group. Key: Predecessor → Successor; Alternative A ⇠·⇢ Alternative B; General ◁— Specific; dotted box = Problem area.

- **Application patterns** — These solve problems faced by developers.
- **Application infrastructure** — These are for infrastructure issues that also impact development.
- **Infrastructure patterns** — These solve problems that are mostly infrastructure issues outside of development.

## Slide 50 — Issue: What's the deployment architecture?

![Slide 50](png/page-50.png)

- Force :-
  - Maintainability
  - Testability
  - Deployability

Options (the **Application architecture** area of the pattern map):

| Pattern | Meaning |
|---|---|
| Monolithic architecture | Single deployable/executable OR Tightly coupled services |
| Microservice architecture | Multiple loosely coupled services |

## Slide 51 — Issue: How to decompose an application into services?

![Slide 51](png/page-51.png)

- Force :-
  - Stability
  - Cohesive
  - Loosely couples
  - Not too large

Options (the **Decomposition** area of the pattern map):

| Pattern | Meaning |
|---|---|
| Decompose by business capability | Organize around business capabilities |
| Decompose by subdomain | Organize around DDD subdomains |

## Slide 52 — The five groups of communication patterns

![Slide 52](png/page-52.png)

The **Communication patterns** region of the pattern map, expanded:

- **Transactional messaging:** Transactional outbox, with Polling publisher and Transaction log tailing as its successors
- **Communication style:** Messaging ↔ Remote procedure invocation (alternatives), both generalizing Domain-specific
- **Reliability:** Circuit breaker
- **Discovery:** Client-side discovery ↔ Server-side discovery and Self registration ↔ 3rd-party registration, all centred on the Service registry
- **External API:** API gateway ↔ Backend for frontend

Key: Predecessor → Successor; Alternative A ⇠·⇢ Alternative B; General ◁— Specific.

## Slide 53 — Issue: How do services communicate?

![Slide 53](png/page-53.png)

- Force :-
  - Services must communicate
  - Usually processes on different machines

Options (the **Communication style** area of the pattern map): **Messaging** ↔ **Remote procedure invocation** as alternatives, with **Domain-specific** as a specific form of either.

## Slide 54 — Issue: How to discover a service instance's network location?

![Slide 54](png/page-54.png)

- Force :-
  - Client needs IP address of service instance
  - Dynamic IP addresses
  - Dynamically provisioned instances

Options (the **Discovery** area of the pattern map): **Client-side discovery** ↔ **Server-side discovery**, **Self registration** ↔ **3rd-party registration**, all built around a **Service registry**.

## Slide 55 — Issue: how to maintain data consistency?

![Slide 55](png/page-55.png)

- Context :-
  - Each service has its own database
  - Data is private to a service
- Forces :-
  - Transactional data consistency must be maintained across multiple services
  - 2PC (two-phase commit) is not an option

Options (the **Maintaining data consistency** area of the pattern map): **Database per service** → **Saga**, which leads to **Domain event** and **Aggregate**, both of which lead to **Event sourcing**.

## Slide 56 — Issue: How to perform queries?

![Slide 56](png/page-56.png)

- Context :-
  - Each service has its own database
- Force :-
  - Queries must join data from multiple services
  - Data is private to a service

Options (the **Querying** area of the pattern map): **Database per service** → **API composition** ↔ **CQRS** (alternatives).

## Slide 57 — Issue: How to handle cross cutting concerns?

![Slide 57](png/page-57.png)

- Force :-
  - Every service must implement logging; externalize configuration; health check endpoint; metrics; ...

Solution (the **Cross-cutting concerns** area of the pattern map): **Microservice Chassis**.

## Slide 58 — Issue: How to deploy an application's services?

![Slide 58](png/page-58.png)

- Force :-
  - Multiple languages
  - Isolated
  - Constrained
  - Monitor-able
  - Reliable
  - Efficient

Options (the **Deployment** area of the pattern map):

| Pattern | Note on the diagram |
|---|---|
| Multiple services per host | Traditional approach of deploying services using their language-specific packaging, such as WAR files |
| Single service per host | A modern approach, which encapsulates a service's technology stack; specialised as **Service-per-container** and **Service-per-VM** |
| Serverless deployment | A modern approach, which runs your code without you having to worry about managing the infrastructure |
| Service deployment platform | Automated, self-service platform for deploying and managing services |

## Slide 59 — Issue: how to monitor the behavior of your application?

![Slide 59](png/page-59.png)

Patterns in the **Observability** area of the pattern map:

- Audit logging
- Application metrics
- Distributed tracing
- Health check API
- Exception tracking
- Log aggregation

---

## Slide 60 — Summary

- The goal of architecture is to satisfy non-functional requirements
- For continuous delivery/deployment use the appropriate architectural style
  - Small applications ⇒ Monolithic architecture
  - Complex applications ⇒ Microservice architecture
- Use the pattern language to guide your decision making
