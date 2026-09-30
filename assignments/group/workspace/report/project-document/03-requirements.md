# 3 Requirements

The functional and non-functional requirements below are those that the four use cases of Section 2 need. The Increment column refers to Section 1.3, and the business rules that the requirements and the use cases refer to (BRULE-nn) are listed in Appendix B.

## 3.1 Functional Requirements

### 3.1.1 User Authentication & Login System

*Table 3.1 User authentication and login*

| ID | Requirement | Use case | Increment |
|---|---|---|---|
| FR-01 | The system shall allow customers to authenticate using LINE Login; the LINE user id is the customer identity and there is no separate registration. | UC-01 | MVP |
| FR-02 | If LINE Login fails or is cancelled, the system shall explain that a LINE account is required and return to the **Rich Menu**. | UC-01 | MVP |
| FR-40 | The system shall allow customers to access only their own reservations and **e-tickets**: My Bookings lists each booking with its round, table, status and **e-ticket**. | UC-01 | MVP |
| FR-65 | The system shall authenticate all internal role accounts (**Manager**, **Front Staff**, and the **Owner** with read-only access) with a username and password issued by the venue, separately from customer LINE Login; the **Manager** creates and disables the accounts and assigns their roles. | UC-02 to UC-04 | MVP |
| FR-66 | The system shall give each role access only to the functions it owns; the **Owner** can read everything. | UC-02 to UC-04 | MVP |
| FR-73 | The system shall allow all users to log out securely. | all | MVP |

### 3.1.2 Venue Zone Map & Concert Round Management System

*Table 3.2 Venue zone map and concert round management*

| ID | Requirement | Use case | Increment |
|---|---|---|---|
| FR-37 | The system shall allow the **Manager** to define **zones**, **table types** (capacity, **package** content and price) and table numbers. | UC-04, UC-03 | MVP |
| FR-39 | The system shall allow the **Manager** to upload the image of the venue's **zone map** and place each table on it. | UC-04 | MVP |
| FR-74 | The system shall validate a **zone map** before activation: every **zone** named and non-empty, table numbers unique, and every table with a **table type** and a seating capacity. | UC-04 | MVP |
| FR-34 | The system shall allow the **Manager** to create and edit a **concert round** with its artist, date, start time, **booking-open time** and status (not yet open, open, sold out, finished, cancelled). | UC-03 | MVP |
| FR-35 | The system shall assign a **zone map** to each round and lock it once the **booking-open time** has passed. | UC-03 | MVP |
| FR-75 | The system shall validate a **concert round** before publishing and prevent overlapping published rounds. | UC-03 | MVP |
| FR-36 | The system shall allow the **Manager** to withdraw a round that has no Confirmed booking. | UC-03 | Increment 2 |
| FR-38 | The system shall keep the **business parameters** (**hold period**, **grace period**, **check-in window**, **extra-person fee**) as settings that change without a code change and apply to rounds that open for booking afterwards. | UC-03 | MVP |
| FR-03 | The system shall list the upcoming rounds with artist, date, start time, **booking-open time** and status (not yet open, open, sold out). | UC-01 | MVP |
| FR-04 | The system shall let customers select the tables of a round only from its **booking-open time**. | UC-01 | MVP |
| FR-05 | The system shall display the **zone map** of a published round with each table's number, **zone**, **table type**, **package price** and status (available, held, booked). | UC-01 | MVP |
| FR-06 | The system shall show a table status change on every open map within 2 seconds. | UC-01, UC-02 | MVP (polling, ADR-09) |

### 3.1.3 Table Reservation System

*Table 3.3 Table reservation*

| ID | Requirement | Use case | Increment |
|---|---|---|---|
| FR-07 | The system shall hold an available table for the **hold period** (15 minutes, BRULE-02) and show the remaining time. | UC-01 | MVP |
| FR-08 | The system shall allow at most one hold or booking per table per round; a later selection is refused and the map refreshed (**first lock wins**). | UC-01 | MVP |
| FR-09 | The system shall ask for the **party size** and compute the **full table fee**: the **package price** plus the **extra-person fee** for each person above the capacity of the **table type**. | UC-01 | MVP |
| FR-10 | On the first booking, the system shall show the purpose of data collection and obtain consent before collecting name and phone into a **customer profile**, which is pre-filled for later bookings; without consent the booking is cancelled. | UC-01 | MVP |
| FR-11 | The system shall let the customer cancel a **hold**; the table becomes available at once and nothing is charged. | UC-01 | MVP |
| FR-12 | The system shall display the **booking terms** (full payment confirms the booking, **check-in window**, **grace period**, no refund for a **no-show**) and require their acceptance before payment. | UC-01 | MVP |
| FR-23 | The system shall release the table when the **hold** ends (±5 seconds), set the booking to Expired and notify the customer, except while a **transfer slip** awaits the **Manager**'s decision. | UC-01 | MVP |

### 3.1.4 Payment

*Table 3.4 Payment*

| ID | Requirement | Use case | Increment |
|---|---|---|---|
| FR-13 | The system shall create a payment request for the **full table fee** and present the gateway's payment methods in its **hosted checkout** inside the web app. | UC-01 | MVP (simulated gateway, ADR-11) |
| FR-14 | After a declined or failed payment, the system shall allow a retry while the **hold** remains. | UC-01 | MVP |
| FR-16 | The system shall verify the signature and the amount of every payment result, process it exactly once, record the payment and confirm the booking. | UC-01 | MVP |
| FR-17 | A successful payment result that arrives after the **hold** expired shall confirm the booking if the table is still free; otherwise the system refunds it through the gateway and informs the customer. | UC-01 | Increment 2 |
| FR-18 | If no payment result arrives within 60 seconds of checkout completion, the system shall poll the payment status every 10 seconds until a result is known or until 10 minutes after the **hold** ends. | UC-01 | Increment 2 |
| FR-69 | If the gateway does not answer within 30 seconds, the system shall switch new payments to **degraded mode** (bank transfer, slip, **Manager** confirmation) and return to gateway mode within 1 minute after it answers again. | UC-01 | Increment 2 |
| FR-15 | In **degraded mode** the system shall keep the **hold**, show the shop's bank account, accept a **transfer slip**, extend the **hold** until the **Manager** decides and notify the **Manager**. | UC-01 | Increment 2 |
| FR-44 | The system shall queue the slip bookings for the **Manager** to confirm or reject; a confirmed slip continues the booking as a gateway payment would. | UC-01 | Increment 2 |
| FR-71 | The system shall accept cards only through the gateway's **hosted checkout**; no card data is entered in or stored by the system. | UC-01 | Increment 2 |

### 3.1.5 E-Ticket & Check-In System

*Table 3.5 E-ticket and check-in*

| ID | Requirement | Use case | Increment |
|---|---|---|---|
| FR-19 | The system shall issue one **e-ticket** per Confirmed booking, with a signed **booking reference** valid only for that round and table, shown on screen and under My Bookings. | UC-01 | MVP |
| FR-24 | The system shall let **Front Staff** scan the QR code with the phone camera and decode the signed **booking reference**. | UC-02 | MVP |
| FR-25 | The system shall accept a **booking reference** typed by hand. | UC-02 | MVP |
| FR-26 | The system shall verify in real time that the booking exists, is Confirmed, is for tonight's round and not yet checked in, and that the **check-in window** is open, and show the result within 2 seconds with table, **zone**, **package**, **party size**, name and payment status. | UC-02 | MVP |
| FR-27 | On a failed verification the system shall give the reason: already checked in (with time and staff account), invalid signature, wrong round, transferred, cancelled, window not open, or **grace period** passed. | UC-02 | MVP |
| FR-28 | The system shall set the booking to Checked-in with the time and the staff account and update the **live view**. | UC-02 | MVP |
| FR-42 | The system shall give the **Manager** a **live view** of the current round's bookings and tables with their status; the **Owner** reads the same view. | UC-02 | MVP |
| FR-30 | The system shall find tonight's Confirmed bookings by name, phone or **booking reference** and allow check-in from the result. | UC-02 | Increment 2 |
| FR-31 | The system shall let **Front Staff** escalate an invalid or duplicate ticket to the **Manager** with the scanned data, the reason and the staff account, and apply the **Manager**'s decision. | UC-02 | Increment 2 |
| FR-48 | The system shall present escalated tickets to the **Manager**, who accepts (with a note) or refuses; the decision is recorded and returned to **Front Staff**. | UC-02 | Increment 2 |
| FR-33 | After the **grace period** the system shall let **Front Staff** mark a **no-show**, or mark it automatically; the table is shown as free, the forfeited fee is recorded, and the table is never offered to a **waitlist**. | UC-02 | Increment 2 |
| FR-72 | The system shall let **Front Staff** mark a freed **no-show** table as occupied by **walk-in** guests, who are seated and paid by hand at the venue. | UC-02 | Increment 2 |

### 3.1.6 Notification System

*Table 3.6 Notification*

| ID | Requirement | Use case | Increment |
|---|---|---|---|
| FR-20 | The system shall send the booking confirmation with the **e-ticket** and the **booking terms** through the LINE Messaging API within 1 minute. | UC-01 | MVP |
| FR-21 | The system shall send a LINE message when a **hold** expires, when a payment fails and, from Increment 2, when a late payment is refunded. | UC-01 | MVP |
| FR-22 | If a message cannot be delivered, the system shall retry 3 times within 5 minutes, record the outcome and keep the **e-ticket** available in the web app. | UC-01 | MVP |

### 3.1.7 Out of Scope

The following are planned for a later release, and this project does not build them: scheduled LINE reminders, the "on my way" grace extension (pending the owner's decision), the **waitlist**, booking transfer, and reports and analytics. Seat-view photographs of the tables are a future feature.

## 3.2 Non-functional Requirements

### 3.2.1 Operational

*Table 3.7 Operational requirements*

| ID | Requirement |
|---|---|
| NFR-03 | The customer web app shall work in the current LINE in-app browser on iOS and Android; the **back-office** in the last two versions of Chrome, Safari and Edge and in the staff's phone browsers. |
| NFR-34 | The customer web app shall open from the **Rich Menu** of the **LINE Official Account**, and the payment checkout shall run inside the same **LIFF** session. |
| NFR-06 | The system shall back up reservation and venue data daily; a restore loses at most 24 hours of data. |
| NFR-31 | Test and production shall be separated (simulated or sandbox payment gateway, LINE test channel); no production key is kept in the source code. |
| NFR-32 | The operating cost shall stay within 1,000 THB per month at 60 bookings per concert night. |

### 3.2.2 Performance

*Table 3.8 Performance requirements*

| ID | Requirement |
|---|---|
| NFR-01 | The system shall accept at least 5 hold requests per second at booking open. |
| NFR-04 | Page loads, holds and ticket verification shall complete within 2 seconds at the 95th percentile under the load of NFR-01. |
| NFR-25 | A table status change shall be visible on every open map within 2 seconds. |
| NFR-26 | A booking shall be Confirmed with its **e-ticket** within 10 seconds of the payment result, and the LINE confirmation sent within 60 seconds of the confirmation. |
| NFR-27 | The system shall serve 200 customers browsing at once and rounds of up to 60 tables, with 50 % headroom. |
| NFR-05 | Check-in from the scan to Checked-in shall take at most 15 seconds per table. |

### 3.2.3 Reliability

*Table 3.9 Reliability requirements*

| ID | Requirement |
|---|---|
| NFR-19 | The system shall be available at least 99.5 % of the opening hours (17:00 to 02:00) of concert nights, over a rolling 12 months. |
| NFR-02 | The system shall recover within 2 hours of a failure during opening hours. |
| NFR-20 | Of concurrent holds on one table exactly one shall succeed, tested with at least 50 simultaneous attempts. |
| NFR-21 | An unpaid hold shall be released within 10 seconds of the end of its 15 minutes, with a timer accuracy of ±5 seconds. |
| NFR-22 | Duplicate or out-of-order payment results shall be processed exactly once; unknown or already settled results are logged and ignored. |
| NFR-23 | Every payment shall reach a final state (paid, failed, expired, refunded) within the **hold period** plus 10 minutes, through the webhook or, from Increment 2, the status query. |

### 3.2.4 Security

*Table 3.10 Security requirements*

| ID | Requirement |
|---|---|
| NFR-36 | The identity tokens of LINE Login (OpenID Connect) shall be validated on the server. |
| NFR-38 | The payment webhook shall verify the signature of every call and reject calls older than 5 minutes or with a reused id. |
| NFR-39 | All traffic shall use HTTPS with TLS 1.2 or later; there is no plain-text endpoint. |
| NFR-44 | The system shall protect customer information and authentication credentials; access to reservations and **e-tickets** follows FR-40 and FR-66. |
| NFR-42 | No card data shall pass through the system; the PCI DSS scope stays with the gateway (Increment 2, real gateway). |

### 3.2.5 Cultural and Legal

*Table 3.11 Cultural and legal requirements*

| ID | Requirement |
|---|---|
| NFR-15 | The interface shall be in Thai and English, following the LINE language setting and switchable. |
| NFR-45 | The system shall display booking and check-in times in Thailand's local time **zone**. |
| NFR-40 | The system shall handle personal information in accordance with Thailand's PDPA: purpose, consent, access and correction, retention and deletion, and breach handling, with a privacy notice. |
| NFR-33 | Personal data shall be kept for at most 24 months by default and then deleted or anonymised. |
| NFR-41 | Package displays, prices and messages shall be factual and shall not advertise alcohol (Alcoholic Beverage Control Act B.E. 2551). |

### 3.2.6 Usability

*Table 3.12 Usability requirements*

| ID | Requirement |
|---|---|
| NFR-13 | The customer web app shall fit a 360 × 640 px viewport in the LINE in-app browser without horizontal scrolling, with touch targets of at least 44 px. |
| NFR-14 | A first-time customer shall get from the **Rich Menu** to the start of payment within 3 minutes, tested with 5 users. |
| NFR-16 | Table status shall be shown by colour plus a label or pattern, with a contrast of at least 4.5:1. |
| NFR-17 | The **back-office** shall work on a desktop and on the staff's phone; the verification result is one tap after the scan. |
| NFR-18 | Every customer-facing failure message shall say what happened and what to do next. |

### 3.2.7 Interfaces

*Table 3.13 Interface requirements*

| ID | Requirement |
|---|---|
| NFR-37 | The payment gateway shall sit behind one payment-service interface (create payment, receive result, query status, refund) so that the gateway can be replaced without changing the reservation logic. |
| NFR-35 | The QR code shall be read by the phone camera in the browser, with no dedicated scanner. |
