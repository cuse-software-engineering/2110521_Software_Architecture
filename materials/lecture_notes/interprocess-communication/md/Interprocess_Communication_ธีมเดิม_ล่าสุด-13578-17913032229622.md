# Interprocess Communication

**Wiwat Vatanawood, Duangdao Wichadakul, Nuengwong Tuaycharoen, Pittipol Kantavat**
RPI, service discovery and messaging

> Transcribed from `Interprocess_Communication_ธีมเดิม_ล่าสุด-13578-17913032229622.pdf` (77 slides). Page images are in [png/](../png/).

---

## Slide 2 — Patterns in this chapter

INTERPROCESS COMMUNICATION

- Remote procedure invocation
- Circuit breaker
- Client-side discovery
- Self registration
- Server-side discovery
- Third-party registration
- Asynchronous messaging
- Message broker

## Slide 3 — Agenda

1. **01** Overview of IPC
2. **02** REST and gRPC
3. **03** Handling partial failure
4. **04** Service discovery
5. **05** Asynchronous messaging

---

# Part 1 — Overview of IPC

## Slide 4 — 01 Overview of IPC

Technologies, interaction styles, APIs and message formats

Section navigation: **Overview** · REST & gRPC · Partial failure · Discovery · Messaging

## Slide 5 — Many IPC technologies

- **Synchronous** — Request/response: REST or gRPC over HTTP
- **Asynchronous** — Messaging: AMQP or STOMP
- **Text formats** — Human-readable: JSON, XML
- **Binary formats** — Compact: Avro, Protocol Buffers

## Slide 6 — Two dimensions of interaction style

- **How many services?**
  - One-to-one: exactly one service
  - One-to-many: several services
- **Does the client wait?**
  - Synchronous: expects a timely reply
  - Asynchronous: doesn't block

## Slide 7 — Interaction styles

| | One-to-one | One-to-many |
|---|---|---|
| **Synchronous** | Request/response (Need to wait for the response) | — |
| **Asynchronous** | Asynchronous request/response; One-way notifications | Publish/subscribe; Publish/async responses |

## Slide 8 — Asynchronous interactions

| Interaction style | Meaning | Example |
|---|---|---|
| Asynchronous request/response | A sender sends a request to one receiver, which sends a response later. | You request a report. The report service generates it and later sends you a "Report ready" message. |
| One-way notifications | A sender sends a message to one receiver, with no application-level reply expected. | An application sends a log entry to a logging service and continues its work. |
| Publish/subscribe | A sender publishes an event to a topic | receivers subscribe to that topic receives it. |
| Publish/async responses | A sender publishes a request to multiple receivers, which can each respond later, independently. | A travel application asks several airlines for prices. Each airline returns its quote when ready. |

> Callout: A one-way notification may still receive a technical acknowledgment such as "message delivered." That is different from an application response containing a result.

## Slide 9 — Asynchronous interactions

| | Publish/subscribe | Publish/async responses |
|---|---|---|
| **Purpose** | Announce an event: "Something happened." | Ask multiple receivers: "Please provide a result." |
| **Replies expected?** | No | Yes, arriving independently later |
| **Example** | Announce an order to inventory, email, and shipping services | Ask several airlines for price quotes |

> Callout: **Async does not mean "no response."** It means the sender does not have to wait for that response before continuing.

## Slide 10 — Defining APIs

- **Hide the implementation** — Expose useful functionality only
- **Change freely** — The implementation can change without hurting clients
- **Use an IDL (Interface Definition Language)** — Define the API precisely with an interface definition language

**Today:** OpenAPI for REST, Protocol Buffers for gRPC, AsyncAPI for messaging.

## Slide 11 — Message formats

- **Text** — JSON, XML — *Human-readable, self-describing*
- **Binary** — Protocol Buffers, Avro — *Compact and efficient*

---

# Part 2 — REST and gRPC

## Slide 12 — 02 REST and gRPC

Synchronous remote procedure invocation

Section navigation: Overview · **REST & gRPC** · Partial failure · Discovery · Messaging

## Slide 13 — Remote procedure invocation (RPI)

- **Request and response** — The client sends a request; the service processes it and replies
- **Blocking or reactive** — Some clients block; others are reactive and non-blocking
- **Timely reply** — The client assumes the response arrives quickly

> Callout: RPI is a *request/response* pattern — a reply is always expected.

> Callout (on "reactive"): client **reacts to the response when it arrives**, instead of keeping a thread blocked while waiting

## Slide 14 — Patterns map: communication style

![Slide 14](../png/page-14.png)

Diagram: Richardson's IPC pattern map — Transactional messaging (Polling publisher, Transaction log tailing, Transactional outbox), Communication style (Messaging, Remote procedure invocation, Domain-specific), Reliability (Circuit breaker), Discovery (Client-side discovery, Self registration, Service registry, Server-side discovery, 3rd-party registration) and External API (API gateway, Backend for frontend). The Communication style group is boxed in red and *Remote procedure invocation* is circled.

- **Communication style** — Remote procedure invocation or messaging
- **Reliability** — Circuit breaker
- **Discovery** — Four patterns around a service registry

## Slide 15 — How RPI works

![Slide 15](../png/page-15.png)

Diagram: a Client hexagon whose Business logic invokes a *Proxy interface* implemented by an **RPI proxy**; the proxy sends a *Request* to the **RPI server** in the Service hexagon and receives a *Reply*; the RPI server calls the Service's Business logic through the *Service interface*.

1. Business logic calls an **RPI proxy interface**
2. The RPI proxy sends the request
3. The **RPI server adapter** calls the business logic

## Slide 16 — REST

![Slide 16](../png/page-16.png)

> Callout: REST is an architectural style

Roy Fielding, who created REST, defines it as:

> *REST provides a set of architectural constraints that, when applied as a whole, emphasizes scalability of component interactions, generality of interfaces, independent deployment of components, and intermediary components to reduce interaction latency, enforce security, and encapsulate legacy systems.*

(In the quote image, "architectural constraints" is underlined in red; "scalability of component interactions", "generality of interfaces", "independent deployment" and "intermediary components" are underlined in green.)

Source: Fielding's dissertation, ics.uci.edu/~fielding/pubs/dissertation

Web grows → HTTP designed → Fielding observes why it works well → Fielding formalizes those principles as REST

## Slide 17 — REST & HTTP

| | HTTP | REST over HTTP |
|---|---|---|
| Protocol | ✓ | ✓ |
| Stateless requests | ✓ (built in) | ✓ (inherited) |
| Uniform resource URLs | not required | required |
| Correct verb semantics (GET for retrieval, POST for creation, etc.) | not required | required |
| Cacheable responses | supported but not required | required |
| Hypermedia links (HATEOAS) | not required | required (by Fielding) |

## Slide 18 — Using REST

- **Resource** — A business object, or a collection: Customer, Product
- **HTTP verbs + URLs** — Manipulate resources referenced by URLs
- **Representation** — GET returns the resource, often as JSON

## Slide 19 — Specifying REST APIs

- **Use an IDL** — Define your APIs precisely
- **REST had none at first** — Unlike CORBA and SOAP
- **OpenAPI Specification** — The most popular REST IDL; evolved from Swagger

**Today:** OpenAPI 3.1 is current, and fully aligned with JSON Schema.

## Slide 20 — REST: trade-offs

**Benefits**

- Simple and familiar
- Easy to test: Postman, curl
- Request/response built in
- Firewall friendly
- No broker needed

**Drawbacks**

- Request/response only
- Both sides must be running
- Clients must find instances
- Many resources = many calls

## Slide 21 — gRPC

- **Cross-language** — A framework for clients and servers in many languages
- **Protocol Buffers IDL** — Google's language-neutral serialization
- **Request/response and streaming** — Binary messages over HTTP/2

## Slide 22 — gRPC API for Order Service (excerpt)

```proto
service OrderService {
    rpc createOrder(CreateOrderRequest) returns (CreateOrderReply) {}
    rpc cancelOrder(CancelOrderRequest) returns (CancelOrderReply) {}
    rpc reviseOrder(ReviseOrderRequest) returns (ReviseOrderReply) {}
    ...
}
message CreateOrderRequest {
    int64 restaurantId = 1;
    int64 consumerId = 2;
    repeated LineItem lineItems = 3;
    ...
}
message LineItem {
    string menuItemId = 1;
    int32 quantity = 2;
}
message CreateOrderReply {
    int64 orderId = 1;
}
...
```

## Slide 23 — gRPC: trade-offs

**Benefits**

- Rich set of update operations
- Efficient, compact messages
- Bidirectional streaming
- Many languages

**Drawbacks**

- More work for JavaScript clients
- Older firewalls may block HTTP/2

**Today:** Browsers use gRPC-Web or Connect; HTTP/2 is now widely supported.

## Slide 24 — Backend for Frontend (BFF)

A BFF typically:

- **Combines data** from multiple services.
- **Shapes responses** for its frontend.
- **Reduces network calls**, especially useful on mobile connections.
- Handles frontend-specific concerns, such as session management.

The trade-off is an extra service to maintain. A BFF is most useful when different frontends have substantially different needs; a simple application may work well with one shared backend.

## Slide 25 — API gateway & BFF

| Aspect | API gateway | BFF |
|---|---|---|
| **Main purpose** | Provide a controlled entry point to services | Make backend data convenient for a particular frontend |
| **Who it serves** | Usually many types of clients | A particular frontend, such as a mobile app or website |
| **Typical responsibilities** | Routing, authentication checks, rate limits, request logging | Combining service results, selecting fields, formatting responses |
| **Example** | Route `/orders` to the order service and enforce request limits | Combine orders and delivery updates into one mobile screen response |

---

# Part 3 — Handling partial failure

## Slide 26 — 03 Handling partial failure

The circuit breaker pattern

Section navigation: Overview · REST & gRPC · **Partial failure** · Discovery · Messaging

## Slide 27 — The risk of partial failure

![Slide 27](../png/page-27.png)

Diagram: a Mobile app sends `POST /orders` to the *Create order endpoint* inside the **API gateway**, which forwards it via the *Order Service proxy* as `POST /orders` to the **Order Service**, labelled "Unresponsive remote service".

- **Synchronous calls** — Risk partial failure
- **The API gateway** — Must protect itself from unresponsive services

## Slide 28 — Patterns map: reliability

![Slide 28](../png/page-28.png)

Diagram: the same IPC pattern map as slide 14, with the Reliability group (*Circuit breaker*) boxed in red.

- **Circuit breaker** — The reliability pattern for synchronous calls

## Slide 29 — Preventing partial failure

- **Part 1** — Design RPI proxies to handle unresponsive services
- **Part 2** — Decide how to recover from a failed service

## Slide 30 — Part 1: robust RPI proxies

- **Timeouts** — Never block forever; always use a timeout
- **Limit requests** — Cap outstanding requests to each service
- **Circuit breaker** — Trip when the error rate passes a threshold; fail fast

**Today:** Use Resilience4j (Hystrix is in maintenance mode) or a service mesh.

## Slide 31 — Example tools for robust RPI proxies

| Option | What it is | Where protection happens |
|---|---|---|
| **Resilience4j** | A Java library providing circuit breakers, concurrency limits, and timeout handling | Inside your application |
| **Service mesh**, such as Istio | Infrastructure that manages communication between services through proxies | In the network layer between services |

## Slide 32 — Amazon: timeouts, retries and jitter

03 · PARTIAL FAILURE · INDUSTRY

- **Timeouts** — Pick an acceptable false-timeout rate, e.g. 0.1%, and set the timeout from it
- **Capped exponential backoff** — Wait longer between retries, up to a maximum
- **Jitter** — Add randomness so clients don't all retry at the same moment

**Read more:** Amazon Builders' Library: Timeouts, retries and backoff with jitter

**Lesson:** Retry safely: backoff, jitter and idempotent APIs.

## Slide 33 — Part 2: recovering from failure

![Slide 33](../png/page-33.png)

Diagram: a Mobile app calls `GET /orders/xyz` on the *Get order endpoint* in the API gateway, which fans out through the Order Service proxy (`GET /orders/xyz`), Kitchen Service proxy (`GET /tickets?orderId=xyz`), Delivery Service proxy (`GET /deliveries?orderId=xyz`) and further proxies to the respective services; annotated "How to handle each unresponsive service?" and "Unresponsive service".

- **Option 1** — Return an error to the client
- **Option 2** — Return a fallback value
- **Plan per service** — A strategy for each service you call

## Slide 34 — Example of Fallback values

| Fallback type | Example |
|---|---|
| **Previously saved data** | Show the last known delivery location, labeled with its update time |
| **Default value** | Show popular products when personalized recommendations are unavailable |
| **Partial result** | Return order details without delivery information |
| **Explicit "unknown" value** | Return `deliveryStatus: "unknown"` so the app can display an appropriate message |

---

# Part 4 — Service discovery

## Slide 35 — 04 Service discovery

Finding service instances in a dynamic environment

Section navigation: Overview · REST & gRPC · Partial failure · **Discovery** · Messaging

## Slide 36 — Why we need service discovery

- **Calling a service** — Needs the IP address and port of an instance
- **Traditional apps** — Network locations are usually static
- **Cloud microservices** — Locations are dynamic and keep changing

## Slide 37 — Locations change constantly

![Slide 37](../png/page-37.png)

Diagram: a *Service client* (marked "?") pointing at three Order service instances at `10.232.23.1`, `10.232.23.2` and `10.232.23.3`, annotated "Dynamically assigned IP" and "Dynamically created and destroyed".

- **Dynamic IPs** — Instances get dynamically assigned addresses
- **Created and destroyed** — Autoscaling, failures and upgrades

## Slide 38 — The service registry

The key component is a **service registry**: a database of instance locations.

- **Application-level** — Services and clients interact with the registry directly
- **Platform-provided** — The deployment infrastructure handles discovery

## Slide 39 — Patterns map: discovery

![Slide 39](../png/page-39.png)

Diagram: the IPC pattern map with the Discovery group (Client-side discovery, Self registration, Service registry, Server-side discovery, 3rd-party registration) boxed in red.

- **Application-level** — client-side discovery + self registration
- **Platform-provided** — server-side discovery + 3rd-party registration

## Slide 40 — Option 1: application-level discovery

![Slide 40](../png/page-40.png)

Diagram: a Service client (RPC/rest client + Service discovery library) sends `Query("order-service")` to the Service registry's *Query API*, gets back `10.232.23.1/2/3`, and sends a load-balanced request to one Order service instance. Each instance's Service discovery library calls `Register("order-service", "10.232.23.1")` on the *Registration API* (Self registration pattern). The registry table maps `order-service` to the three IP addresses.

- **Client-side discovery** — Clients query the registry and load-balance
- **Self registration** — Instances register themselves with the registry

## Slide 41 — Option 2: platform-provided discovery

![Slide 41](../png/page-41.png)

Diagram: the Service client issues `GET http://order-service/...`; the service DNS name resolves to the service virtual IP `10.232.24.99` of a *Platform router* in the Deployment platform, which queries the Service registry and forwards to one Order service instance (server-side discovery). A *Registrar* observes the instances and updates the registry (3rd party registration).

- **3rd-party registration** — The platform registers instances
- **Server-side discovery** — A platform router resolves a service DNS name to the service virtual IP address (VIP)

**Today:** Kubernetes Services and DNS do this for you.

## Slide 42 — Client side & Service side discovery

| Approach | Pros | Cons |
|---|---|---|
| **Client-side discovery** | Client can customize load balancing and choose instances based on its needs. Can call instances directly without a separate routing hop. | Each client needs discovery and balancing logic, often through a library. Clients must handle stale instance lists and discovery failures. Supporting multiple programming languages adds maintenance. |
| **Server-side discovery** | Simpler clients: they use a stable address. Discovery and routing work across programming languages. The platform centrally tracks instances and manages routing. | Requires routing infrastructure to operate and troubleshoot. A separate proxy may add latency and become a bottleneck unless scaled. Clients have less direct control over instance selection. |

---

# Part 5 — Asynchronous messaging

## Slide 43 — 05 Asynchronous messaging

Messages, channels and message brokers

Section navigation: Overview · REST & gRPC · Partial failure · Discovery · **Messaging**

## Slide 44 — Asynchronous messaging

- **Send a message** — The client sends a request as a message
- **Don't block** — The client doesn't wait for the reply
- **Two architectures** — Brokerless or broker-based

## Slide 45 — Patterns map: messaging

![Slide 45](../png/page-45.png)

Diagram: the IPC pattern map with the Communication style group boxed in red and *Messaging* circled.

- **Messaging** — The asynchronous communication style

## Slide 46 — Messages and channels

Senders write messages to **channels**; receivers read them.

- **Document** — Contains only data
- **Command** — Like an RPC request
- **Event** — Something notable happened

## Slide 47 — Messaging architecture

![Slide 47](../png/page-47.png)

Diagram: the Sender's Business logic invokes a *Sending port* implemented by a **Message sender**, which sends a Message (Header + Body) onto a *Message channel* in the Messaging infrastructure; a **Message handler** receives it and invokes the Receiver's Business logic through the *Receiving port*.

1. Sender's logic calls a **sending port of the Message sender**
2. The message travels on a **channel**
3. A **Message handler** calls the receiver's logic

## Slide 48 — Two kinds of channels

- **Point-to-point** — Delivers to exactly one consumer — e.g. command messages
- **Publish-subscribe** — Delivers to all attached consumers — e.g. event messages

## Slide 49 — Interaction styles with messaging

- **Async request/response** — Asynchronous by nature, the receiver responds later
- **One-way notification** — The sender sends message to a service, no wait; the service consumes the message; no reply
- **Publish/subscribe** — The sender publishes a message to a pub-sub channel, many consumers, no reply
- **Publish/async responses** — The sender publishes a request to multiple receivers, which can each respond later, independently.

## Slide 50 — Asynchronous request/response

![Slide 50](../png/page-50.png)

Diagram: (1) the Client sends a Request message (`MessageId: msgId`, `ReturnAddress: ReplyChannel`, Body) to the *Request channel*; the Service reads it and (2) sends a Reply (`CorrelationId: msgId`, Body) to the specified *Reply channel*, which the Client reads. Captions: "Client sends message containing msgId and a reply channel." and "Service sends reply to the specified reply channel. The reply contains a correlationId, which is the request's msgId."

- **Request** — Includes a reply channel and a message ID
- **Reply** — Sent to the reply channel, carrying a correlation ID

## Slide 51 — Brokerless vs broker-based

![Slide 51](../png/page-51.png)

Diagram: *Brokerless architecture* — three Service hexagons exchanging messages directly with each other; vs. *Broker-based architecture* — three Services all connected through a central **Message broker**.

- **Brokerless** — Services exchange messages directly
- **Broker-based** — All messages flow through a broker
- **Our focus** — Broker-based messaging

## Slide 52 — Brokerless messaging: trade-offs

**Benefits**

- Less traffic, lower latency
- No broker bottleneck or single point of failure

**Drawbacks**

- Needs service discovery
- Both sides must be available

## Slide 53 — Broker-based messaging

A **message broker** is an intermediary that all messages flow through.

- **Location-free** — The sender needn't know where consumers are
- **Buffering** — Messages wait until consumers can process them

**Brokers:** ActiveMQ, RabbitMQ, Kafka · cloud: Amazon SQS/Kinesis, Google Cloud Pub/Sub

## Slide 54 — Broker-based messaging: trade-offs

**Benefits**

- Loose coupling: no discovery
- Message buffering
- Supports several interaction styles
- Explicit IPC

> Callout (on "Explicit IPC"): code makes communication between separate processes obvious

**Drawbacks**

- Possible bottleneck
- Possible single point of failure
- More operations work

**Today:** Kafka 4.0 (2025) runs without ZooKeeper, which simplifies operations.

## Slide 55 — Competing receivers and ordering

- **Competing receivers** — Three instances read the same point-to-point channel
- **Out of order** — Created, Updated, Cancelled may be processed in the wrong order
- **Solution** — Sharded (partitioned) channels: Kafka, Kinesis, RabbitMQ Stream (Super Streams)

## Slide 56 — Sharded channels preserve order

![Slide 56](../png/page-56.png)

Diagram: a Sender emits a *Create order request* with `Shard-key: orderId`; a **Router** "routes based on a hash of the shard-key" into Shard 0, Shard 1, Shard … of the Channel; shard assignment maps each shard to one instance of Logical receiver A (Receiver A instance 1, instance 2, Receiver …).

- **Shard key** — Each Order event uses orderId
- **Same shard** — All events for one order go to one shard
- **One consumer** — Each shard is read by a single instance

## Slide 57 — Handling duplicate messages

- **Duplicates happen** — Client, network or broker failures can redeliver a message
- **Example** — Authorizing a credit card must not happen twice
- **Solution** — Discard duplicates by tracking message IDs

## Slide 58 — Tracking processed messages

![Slide 58](../png/page-58.png)

Diagram: a Message with `id: xyz` reaches a **Consumer**, which in one Transaction does `INSERT` into the `PROCESSED_MESSAGE` table (`MSG_ID = xyz`) and `UPDATE` on the Application table; annotated "INSERT will fail for duplicate messages."

- **Record IDs** — Store processed message IDs in a table
- **Duplicate?** — The INSERT fails, so the message is skipped

## Slide 59 — Kafka: messaging built at LinkedIn

05 · MESSAGING · RESEARCH

- **Built for volume** — Collects and delivers high volumes of log data with low latency
- **Partitions** — Each topic partition is a log: the sharded channels you just saw
- **At-least-once delivery** — So consumers must be ready for duplicate messages

**Read more:** Kafka paper (Kreps et al., NetDB 2011)

**Lesson:** Partitions keep order; at-least-once means consumers dedupe.

## Slide 60 — Kafka 101: concepts

![Slide 60](../png/page-60.png)

Diagram: the ByteByteGo "Kafka 101 — 8 steps to learn the fundamentals of Kafka" infographic (1 What is Kafka, 2 What is a message — record with headers, key, value, 3 Topics & partitions, 4 Advantages of Kafka, 5 Kafka producer, 6 Kafka consumer / consumer group, 7 Kafka cluster with brokers and replicated partitions, 8 Kafka use cases: log analysis, data streaming, change data capture, system monitoring and alerting).

Source: https://assets.bytebytego.com/diagrams/0246-kafka-101-8-steps-to-learn-the-fundamentals-of-kafka.png

| Concept | What it is |
|---|---|
| Broker | A server in the cluster |
| Topic | A logical category of messages |
| Partition | The physical unit of storage and distribution |
| Broker's role | Hosts partitions from potentially many topics |

**Each partition also has replicas across brokers for fault tolerance:**

```
Partition 0:
Broker 1 → Leader (handles reads/writes)
Broker 2 → Follower replica
Broker 3 → Follower replica
```

## Slide 61 — What Brokers in Kafka do

1. **Store messages** — The most fundamental job. Each broker stores its assigned partitions as **append-only log files** on disk. (Messages are never deleted immediately — they are retained for a configured period)
2. **Accept writes from producers** — When a producer sends a message, it connects to the broker that is the **leader** for that partition and writes to it. The broker acknowledges the write once it is stored.
3. **Serve reads to consumers** — A consumer connects to the broker hosting the partition and fetches messages starting from a given **offset**. The broker does not push messages — consumers **pull** from brokers.
4. **Manage replication** — Each partition has one **leader broker** and one or more **follower brokers**. The leader handles all reads and writes / follower(s) just continuously replicate from the leader

## Slide 62 — What Brokers in Kafka do

5. **Handle consumer group coordination**

   ```
   Consumer Group: order-processors
     Instance 1 → reads Partition 0
     Instance 2 → reads Partition 1
     Instance 3 → reads Partition 2
   ```

   When an instance joins or leaves, the broker triggers a **rebalance** — reassigning partitions among the remaining instances.

6. **Cluster coordination (KRaft mode)** — Brokers handle broker metadata such as which brokers are alive, who is the leader for each partition, etc. using KRaft protocol

## Slide 63 — RabbitMQ

RabbitMQ is a **message broker** built around the **AMQP protocol** (Advanced Message Queuing Protocol). It was originally developed by **Rabbit Technologies** in 2007 and is now maintained by **Broadcom** (previously VMware, previously Pivotal).

**Core architecture differences**

```
Kafka:    Producer → Broker (partition/log) → Consumer pulls
RabbitMQ: Producer → Exchange → Queue → Broker pushes to Consumer
```

## Slide 64 — The hierarchy in RabbitMQ

```
RabbitMQ Node (server)
└── Virtual Hosts (vhosts) — isolated environments
    └── Exchanges — receive messages from producers
        └── Bindings — rules connecting exchanges to queues
            └── Queues — store messages for consumers
```

## Slide 65 — What Brokers in RabbitMQ do

1. **Accept messages from producers** — Producer → connects to broker → publishes to exchange with routing key
2. **Route messages to queues** — Broker → applies binding rules → copies message to matching queues
3. **Store messages in queues** — Messages wait in queues until consumers are ready. The broker manages queue storage in memory and/or disk depending on configuration.
4. **Push messages to consumers** — Broker → pushes message → Consumer; Consumer → sends acknowledgment → Broker removes message
5. **Handle acknowledgments**
   - **ack** — consumer processed successfully, broker removes message
   - **nack** — consumer failed, broker can requeue or discard
   - **reject** — similar to nack

## Slide 66 — What Brokers in RabbitMQ do

6. **Cluster coordination** — In a RabbitMQ cluster, nodes share metadata about exchanges, bindings, and queues. Queues can be:
   - **Classic queues** — live on one node, replicated optionally
   - **Quorum queues** — replicated across multiple nodes using Raft consensus (recommended for reliability)
   - **Streams** — append-only log similar to Kafka partitions (added in RabbitMQ 3.9)
7. **Dead letter handling** — When a message cannot be processed (expired, rejected, queue full), the broker can route it to a **dead letter exchange** for separate handling. Failed message → Dead Letter Exchange → Dead Letter Queue → inspection/retry

## Slide 67 — RabbitMQ vs Kafka key differences

| Aspect | RabbitMQ | Kafka |
|---|---|---|
| Primary model | Message broker (push) | Distributed log (pull) |
| Message retention | Deleted after consumption | Retained for configured period |
| Replay messages | Not by default | Yes — consumers can re-read |
| Routing | Flexible — exchanges and bindings | Simple — topic and partition |
| Ordering | Per queue | Per partition |
| Throughput | High but lower than Kafka | Very high |
| Best for | Complex routing, task queues | High volume streaming, event log |
| Consumer model | Push to consumer | Consumer pulls |
| Protocol | AMQP (also STOMP, MQTT) | Custom binary protocol |

## Slide 68 — When to use RabbitMQ vs Kafka

| Use RabbitMQ when | Use Kafka when |
|---|---|
| You need complex message routing | You need very high throughput |
| Messages should be deleted after processing | You need message replay |
| You need per-message acknowledgement | You need event streaming |
| Task queues (one worker processes each task) | Event sourcing |
| Lower volume, lower latency needed | Multiple consumers reading same data |

## Slide 69 — Sync vs async interactions

![Slide 69](../png/page-69.png)

Diagram: a sequence diagram with Client, Order Service, Consumer Service, Restaurant Service and "…" lifelines (key: solid arrow = Synchronous, open arrow = Asynchronous). The Client's `createOrder` call to Order Service (which does `create order` and replies) is boxed as **Synchronous**; the subsequent `ValidateConsumerInfo`, `ValidateOrderDetails`, `ConsumerValidated`, `update order`, `OrderDetailsValidated`, `update order`, … exchanges with the other services are marked **Asynchronous**.

## Slide 70 — Messaging in a saga: Create Order

![Slide 70](../png/page-70.png)

Diagram: the Order Service's *Create order saga orchestrator* sends command messages through a Message broker — (1) Verify consumer on the Consumer Service request channel, (3) Create ticket on the Kitchen Service request channel, (5) Authorize card on the Accounting Service request channel, (7) Approve restaurant order, (8) Approve order on the Order Service request channel — and receives reply messages (2) Consumer verified, (4) Ticket created, (6) Card authorized on the *Create order saga reply channel*. Key: command message (circle), reply message (hexagon).

Saga is a design pattern for managing a business transaction across multiple services.

Saga uses a Saga orchestrator to manage a **sequence of smaller, local transactions**.

For example, the business operation is **"Create Order"** includes:

1. Verify the customer — Consumer Service.
2. Create a kitchen ticket — Kitchen Service.
3. Authorize the payment card — Accounting Service.
4. Approve the kitchen order and the overall order.

## Slide 71 — Messaging in a saga: Create Order

![Slide 71](../png/page-71.png)

Diagram: the same Create Order saga diagram as slide 70.

```
Verify customer       → Success (committed)
Create kitchen ticket → Success (committed)
Authorize payment     → Failed
                          ↓
Compensate step 2: Cancel kitchen ticket
Compensate step 1: Reject order
```

**Compensation is not a normal database rollback.** Earlier steps have already committed.

Cancelling the ticket is a *new operation* that counteracts creating it. Compensation can also fail, so it may need retries.

> Callout: In a saga, each step is a **separate local transaction** that has already committed:

## Slide 72 — Messaging in a saga: styles

![Slide 72](../png/page-72.png)

Diagram: the same Create Order saga diagram, with the *Create order saga orchestrator* box highlighted in yellow.

| Style | How steps are coordinated |
|---|---|
| **Orchestration** — จากรูปด้านซ้ายเป็นแบบนี้ | A coordinator tells each service what to do next. |
| **Choreography** | Services react to events and publish events that trigger subsequent steps. |

## Slide 73 — Messaging in a saga: styles

![Slide 73](../png/page-73.png)

Diagram: the same Create Order saga diagram (orchestrator highlighted), with a large callout pointing at it.

> Callout: ถามไว้ให้คิด
> คำถามคือ ทำไมต้องมี Saga pattern ที่ใช้แนวคิด separate local transaction
> ใช้ distributed transaction ร่วมกับ 2PC (2-Phase Commit) แทนได้ไหม

---

# Summary

## Slide 74 — Summary (1)

- **IPC is key** — Microservices are a distributed architecture
- **Evolve APIs carefully** — Manage how each service's API changes
- **Many technologies** — Each with different trade-offs
- **Synchronous clients** — Must be designed to handle partial failure

## Slide 75 — Summary (2)

- **Service discovery** — Client side and service side
- **Messages and channels** — A good model for messaging, typically broker-based

## Slide 76 — Q&A

Questions?

Interprocess communication in a microservice architecture

## Slide 77 — Further reading

*Click a title to open it*

- **Timeouts, retries and backoff with jitter** — Amazon Builders' Library — aws.amazon.com/builders-library/timeouts-retries…
- **Kafka: a Distributed Messaging System for Log Processing** — Kreps et al., NetDB 2011 — people.csail.mit.edu/matei/courses/2015/6.S897/r…
- **Resilience4j** — Circuit breaker and retry library (successor to Hystrix) — resilience4j.readme.io
- **gRPC documentation** — Official documentation — grpc.io/docs
- **OpenAPI Initiative** — The REST API description standard — www.openapis.org
- **Microservice patterns** — Chris Richardson's pattern catalog — microservices.io/patterns
